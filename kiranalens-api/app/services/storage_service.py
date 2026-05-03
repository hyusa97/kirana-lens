"""
Storage service for handling image uploads and retrieval using Supabase Storage
"""
import base64
import uuid
from typing import List, Tuple

import httpx
from fastapi import HTTPException, UploadFile, status
from supabase import create_client, Client

from app.config import settings


class StorageService:
    """Service for handling file storage operations with Supabase"""
    
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket_name = settings.SUPABASE_BUCKET
    
    async def upload_images(self, files: List[UploadFile], assessment_id: str) -> List[str]:
        """
        Upload multiple images to Supabase Storage.
        
        Args:
            files: List of uploaded image files
            assessment_id: Assessment ID for organizing files
            
        Returns:
            List[str]: List of public CDN URLs
            
        Raises:
            HTTPException: If validation fails or upload errors occur
        """
        if not files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No files provided"
            )
        
        # Validate file count
        if len(files) < settings.MIN_IMAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum {settings.MIN_IMAGES} images required"
            )
        
        if len(files) > settings.MAX_IMAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum {settings.MAX_IMAGES} images allowed"
            )
        
        uploaded_urls = []
        
        for file in files:
            # Validate file type
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is not an image"
                )
            
            # Validate specific image types
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} must be JPEG, PNG, or WebP format"
                )
            
            # Read and validate file size
            content = await file.read()
            await file.seek(0)  # Reset file pointer
            
            size_mb = len(content) / (1024 * 1024)
            if size_mb > settings.MAX_IMAGE_SIZE_MB:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} exceeds {settings.MAX_IMAGE_SIZE_MB}MB limit"
                )
            
            # Generate unique filename
            file_extension = self._get_file_extension(file.content_type)
            filename = f"{assessment_id}/{uuid.uuid4()}.{file_extension}"
            
            try:
                # Upload to Supabase Storage
                response = self.supabase.storage.from_(self.bucket_name).upload(
                    path=filename,
                    file=content,
                    file_options={
                        "content-type": file.content_type,
                        "cache-control": "3600"
                    }
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to upload {file.filename}: {response.json()}"
                    )
                
                # Get public URL
                public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(filename)
                uploaded_urls.append(public_url)
                
            except Exception as e:
                # Clean up any successfully uploaded files
                await self._cleanup_uploaded_files(uploaded_urls)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Upload failed for {file.filename}: {str(e)}"
                )
        
        return uploaded_urls
    
    async def get_image_as_base64(self, url: str) -> Tuple[str, str]:
        """
        Fetch image from URL and return as base64 encoded string.
        
        Args:
            url: Image URL to fetch
            
        Returns:
            Tuple[str, str]: (base64_encoded_string, media_type)
            
        Raises:
            HTTPException: If image fetch fails
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Get content type
                media_type = response.headers.get('content-type', 'image/jpeg')
                
                # Validate it's an image
                if not media_type.startswith('image/'):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"URL does not point to an image: {media_type}"
                    )
                
                # Encode to base64
                image_data = response.content
                base64_string = base64.b64encode(image_data).decode('utf-8')
                
                return base64_string, media_type
                
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch image from URL: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing image: {str(e)}"
            )
    
    async def delete_images(self, urls: List[str]) -> bool:
        """
        Delete images from Supabase Storage.
        
        Args:
            urls: List of image URLs to delete
            
        Returns:
            bool: True if all deletions successful
        """
        try:
            # Extract file paths from URLs
            file_paths = []
            for url in urls:
                # Extract path from public URL
                # Format: https://xxx.supabase.co/storage/v1/object/public/bucket/path
                if '/storage/v1/object/public/' in url:
                    path = url.split('/storage/v1/object/public/')[1]
                    # Remove bucket name from path
                    path_parts = path.split('/', 1)
                    if len(path_parts) > 1:
                        file_paths.append(path_parts[1])
            
            if file_paths:
                response = self.supabase.storage.from_(self.bucket_name).remove(file_paths)
                return response.status_code == 200
            
            return True
            
        except Exception as e:
            print(f"Error deleting images: {e}")
            return False
    
    def _get_file_extension(self, content_type: str) -> str:
        """Get file extension from content type."""
        extension_map = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp'
        }
        return extension_map.get(content_type, 'jpg')
    
    async def _cleanup_uploaded_files(self, urls: List[str]) -> None:
        """Clean up uploaded files in case of error."""
        if urls:
            await self.delete_images(urls)