"""
Mock Storage Service - Local file storage for testing without Supabase
This allows testing assessment creation without setting up Supabase
"""
import base64
import uuid
from pathlib import Path
from typing import List, Tuple

import httpx
from fastapi import HTTPException, UploadFile, status

from app.config import settings


class MockStorageService:
    """Mock service for handling file storage operations locally"""
    
    def __init__(self):
        # Create local storage directory
        self.storage_dir = Path("uploads")
        self.storage_dir.mkdir(exist_ok=True)
        print(f"[MockStorage] Using local storage at: {self.storage_dir.absolute()}")
    
    async def upload_images(self, files: List[UploadFile], assessment_id: str) -> List[str]:
        """
        Upload multiple images to local storage.
        
        Args:
            files: List of uploaded image files
            assessment_id: Assessment ID for organizing files
            
        Returns:
            List[str]: List of local file URLs
            
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
        
        # Create assessment directory
        assessment_dir = self.storage_dir / assessment_id
        assessment_dir.mkdir(exist_ok=True)
        
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
            filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = assessment_dir / filename
            
            try:
                # Save file locally
                with open(file_path, 'wb') as f:
                    f.write(content)
                
                # Generate mock URL (in production, this would be a CDN URL)
                # For local testing, we'll use a placeholder URL
                mock_url = f"http://localhost:8000/uploads/{assessment_id}/{filename}"
                uploaded_urls.append(mock_url)
                
                print(f"[MockStorage] Saved: {file_path}")
                
            except Exception as e:
                # Clean up any successfully uploaded files
                await self._cleanup_uploaded_files(uploaded_urls, assessment_id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Upload failed for {file.filename}: {str(e)}"
                )
        
        print(f"[MockStorage] Uploaded {len(uploaded_urls)} images for assessment {assessment_id}")
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
            # Check if it's a local mock URL
            if url.startswith("http://localhost:8000/uploads/"):
                # Extract file path from URL
                path_parts = url.replace("http://localhost:8000/uploads/", "")
                file_path = self.storage_dir / path_parts
                
                if not file_path.exists():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image not found: {url}"
                    )
                
                # Read file
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                
                # Determine media type from extension
                extension = file_path.suffix.lower()
                media_type_map = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.webp': 'image/webp'
                }
                media_type = media_type_map.get(extension, 'image/jpeg')
                
                # Encode to base64
                base64_string = base64.b64encode(image_data).decode('utf-8')
                
                return base64_string, media_type
            
            else:
                # Fetch from external URL
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
    
    async def delete_images(self, urls: List[str], assessment_id: str = None) -> bool:
        """
        Delete images from local storage.
        
        Args:
            urls: List of image URLs to delete
            assessment_id: Optional assessment ID for cleanup
            
        Returns:
            bool: True if all deletions successful
        """
        try:
            for url in urls:
                if url.startswith("http://localhost:8000/uploads/"):
                    # Extract file path from URL
                    path_parts = url.replace("http://localhost:8000/uploads/", "")
                    file_path = self.storage_dir / path_parts
                    
                    if file_path.exists():
                        file_path.unlink()
                        print(f"[MockStorage] Deleted: {file_path}")
            
            # Clean up empty assessment directory
            if assessment_id:
                assessment_dir = self.storage_dir / assessment_id
                if assessment_dir.exists() and not any(assessment_dir.iterdir()):
                    assessment_dir.rmdir()
                    print(f"[MockStorage] Removed empty directory: {assessment_dir}")
            
            return True
            
        except Exception as e:
            print(f"[MockStorage] Error deleting images: {e}")
            return False
    
    def _get_file_extension(self, content_type: str) -> str:
        """Get file extension from content type."""
        extension_map = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp'
        }
        return extension_map.get(content_type, 'jpg')
    
    async def _cleanup_uploaded_files(self, urls: List[str], assessment_id: str) -> None:
        """Clean up uploaded files in case of error."""
        if urls:
            await self.delete_images(urls, assessment_id)
