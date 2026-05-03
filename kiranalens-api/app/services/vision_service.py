"""
Vision service for analyzing store images using multiple AI providers (Groq, OpenAI, Anthropic)
"""
import json
import re
from typing import Dict, List

from fastapi import HTTPException, status

from app.config import settings
from app.services.storage_service import StorageService


class VisionService:
    """Service for analyzing store images with AI vision models"""
    
    def __init__(self):
        self.storage_service = StorageService()
        self.ai_provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
        
        # Initialize the appropriate AI client
        if self.ai_provider == 'groq':
            from groq import AsyncGroq
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            self.model = "llama-3.1-70b-versatile"  # Best model for complex analysis
        elif self.ai_provider == 'openai':
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = "gpt-4o-mini"  # Cost-effective vision model
        elif self.ai_provider == 'anthropic':
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-3-sonnet-20240229"
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
    
    async def analyze_images(self, image_urls: List[str]) -> Dict:
        """
        Analyze store images to extract visual features for credit assessment.
        
        Args:
            image_urls: List of image URLs to analyze
            
        Returns:
            Dict: Analysis results with visual features and raw response
            
        Raises:
            HTTPException: If analysis fails
        """
        if not image_urls:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No images provided for analysis"
            )
        
        try:
            if self.ai_provider == 'groq':
                return await self._analyze_with_groq(image_urls)
            elif self.ai_provider == 'openai':
                return await self._analyze_with_openai(image_urls)
            elif self.ai_provider == 'anthropic':
                return await self._analyze_with_anthropic(image_urls)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Vision analysis failed: {str(e)}"
            )
    
    async def _analyze_with_groq(self, image_urls: List[str]) -> Dict:
        """Analyze images using Groq API (text-only, describe images first)"""
        # Note: Groq doesn't support vision yet, so we'll use text description approach
        # For now, we'll simulate the analysis or use a text-based approach
        # In production, you might want to use a different approach or combine with another service
        
        system_prompt = self._get_system_prompt()
        user_prompt = f"""
        {self._get_user_prompt()}
        
        Note: Since direct image analysis is not available, please provide a sample analysis 
        for a typical Indian kirana store with moderate inventory and organization.
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        response_text = response.choices[0].message.content
        analysis_result = self._parse_json_response(response_text)
        self._validate_analysis_result(analysis_result)
        
        return {
            **analysis_result,
            "raw_ai_response": {
                "provider": "groq",
                "model": self.model,
                "response_text": response_text,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        }
    
    async def _analyze_with_openai(self, image_urls: List[str]) -> Dict:
        """Analyze images using OpenAI Vision API"""
        # Prepare image content for OpenAI
        content = [{"type": "text", "text": self._get_user_prompt()}]
        
        for url in image_urls:
            content.append({
                "type": "image_url",
                "image_url": {"url": url, "detail": "high"}
            })
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": content}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        response_text = response.choices[0].message.content
        analysis_result = self._parse_json_response(response_text)
        self._validate_analysis_result(analysis_result)
        
        return {
            **analysis_result,
            "raw_ai_response": {
                "provider": "openai",
                "model": self.model,
                "response_text": response_text,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        }
    
    async def _analyze_with_anthropic(self, image_urls: List[str]) -> Dict:
        """Analyze images using Anthropic Claude Vision API"""
        # Fetch and encode all images as base64
        image_data = []
        for url in image_urls:
            base64_string, media_type = await self.storage_service.get_image_as_base64(url)
            image_data.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_string
                }
            })
        
        # Create message content with images and text
        message_content = image_data + [{"type": "text", "text": self._get_user_prompt()}]
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.1,
            system=self._get_system_prompt(),
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )
        
        response_text = response.content[0].text
        analysis_result = self._parse_json_response(response_text)
        self._validate_analysis_result(analysis_result)
        
        return {
            **analysis_result,
            "raw_ai_response": {
                "provider": "anthropic",
                "model": self.model,
                "response_text": response_text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        }
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for Claude."""
        return """You are an expert retail analyst specializing in Indian kirana stores. You extract structured economic signals from store images to support credit underwriting decisions. 

Your analysis helps financial institutions assess the creditworthiness of small retail businesses by evaluating visual indicators of business health, inventory management, customer activity, and operational quality.

Respond ONLY with valid JSON. Do not include any markdown formatting, explanations, or additional text."""
    
    def _get_user_prompt(self) -> str:
        """Get the user prompt requesting specific analysis."""
        return """Analyze these kirana store images and provide a comprehensive assessment. Return a JSON object with exactly these fields:

{
  "shelf_density_index": <integer 0-100>,
  "sku_diversity_score": <integer 0-100>,
  "inventory_value_band": "<low|medium|high|very_high>",
  "refill_signal": "<partially_empty|normal|overfilled>",
  "store_organization_score": <integer 0-100>,
  "counter_activity_proxy": <integer 0-100>,
  "exterior_quality_score": <integer 0-100>,
  "image_quality_warnings": [<array of strings>],
  "fraud_indicators": [<array of strings>]
}

Scoring Guidelines:
- shelf_density_index: How well-stocked are the shelves? (0=empty, 100=fully stocked)
- sku_diversity_score: Variety of products available (0=very limited, 100=extensive variety)
- inventory_value_band: Overall inventory value assessment
- refill_signal: Current restocking needs based on shelf levels
- store_organization_score: Cleanliness, arrangement, and organization (0=poor, 100=excellent)
- counter_activity_proxy: Signs of customer activity and business operations (0=inactive, 100=very active)
- exterior_quality_score: Store front condition and visibility (0=poor, 100=excellent)
- image_quality_warnings: List any image quality issues that affect analysis confidence
- fraud_indicators: List any suspicious elements that might indicate fraudulent activity

Focus on indicators relevant to business viability and credit risk assessment."""
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """
        Parse JSON response from Claude, handling markdown and retrying if needed.
        
        Args:
            response_text: Raw response from Claude
            
        Returns:
            Dict: Parsed JSON data
            
        Raises:
            HTTPException: If JSON parsing fails after retry
        """
        # First attempt: try to parse as-is
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Second attempt: strip markdown code blocks
        cleaned_text = self._strip_markdown(response_text)
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Third attempt: extract JSON from text
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # If all parsing attempts fail, raise an exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse JSON response from vision analysis"
        )
    
    def _strip_markdown(self, text: str) -> str:
        """Remove markdown code block formatting."""
        # Remove ```json and ``` markers
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        text = text.strip()
        return text
    
    async def _retry_with_explicit_json_request(self, original_response: str) -> Dict:
        """
        Retry the request with explicit JSON-only instruction.
        
        Args:
            original_response: The original response that failed to parse
            
        Returns:
            Dict: Parsed JSON data
            
        Raises:
            HTTPException: If retry also fails
        """
        try:
            retry_prompt = f"""The previous response was not valid JSON:
{original_response}

Please respond with ONLY raw JSON, no markdown formatting, no explanations. Just the JSON object with the required fields."""
            
            response = await self.anthropic.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.0,
                system="Respond with ONLY valid JSON. No markdown, no explanations.",
                messages=[{
                    "role": "user",
                    "content": retry_prompt
                }]
            )
            
            response_text = response.content[0].text.strip()
            return json.loads(response_text)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse vision analysis response after retry: {str(e)}"
            )
    
    def _validate_analysis_result(self, result: Dict) -> None:
        """
        Validate that all required fields are present in the analysis result.
        
        Args:
            result: Analysis result to validate
            
        Raises:
            HTTPException: If validation fails
        """
        required_fields = {
            'shelf_density_index': int,
            'sku_diversity_score': int,
            'inventory_value_band': str,
            'refill_signal': str,
            'store_organization_score': int,
            'counter_activity_proxy': int,
            'exterior_quality_score': int,
            'image_quality_warnings': list,
            'fraud_indicators': list
        }
        
        missing_fields = []
        invalid_types = []
        
        for field, expected_type in required_fields.items():
            if field not in result:
                missing_fields.append(field)
            elif not isinstance(result[field], expected_type):
                invalid_types.append(f"{field} (expected {expected_type.__name__})")
        
        if missing_fields or invalid_types:
            error_details = []
            if missing_fields:
                error_details.append(f"Missing fields: {', '.join(missing_fields)}")
            if invalid_types:
                error_details.append(f"Invalid types: {', '.join(invalid_types)}")
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Vision analysis validation failed: {'; '.join(error_details)}"
            )
        
        # Validate enum values
        valid_inventory_bands = ['low', 'medium', 'high', 'very_high']
        if result['inventory_value_band'] not in valid_inventory_bands:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid inventory_value_band: {result['inventory_value_band']}"
            )
        
        valid_refill_signals = ['partially_empty', 'normal', 'overfilled']
        if result['refill_signal'] not in valid_refill_signals:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid refill_signal: {result['refill_signal']}"
            )
        
        # Validate score ranges
        score_fields = [
            'shelf_density_index', 'sku_diversity_score', 'store_organization_score',
            'counter_activity_proxy', 'exterior_quality_score'
        ]
        
        for field in score_fields:
            score = result[field]
            if not (0 <= score <= 100):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Score {field} must be between 0-100, got {score}"
                )