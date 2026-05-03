"""
AI processing utilities for assessment analysis
"""
import json
import random
from typing import Dict, List, Optional
from uuid import UUID

from anthropic import AsyncAnthropic

from app.config import settings


class AIProcessor:
    """AI processor for kirana store assessment analysis"""
    
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def analyze_store_images(
        self,
        image_urls: List[str],
        store_name: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Dict:
        """
        Analyze store images using Claude Vision API.
        
        Args:
            image_urls: List of image URLs
            store_name: Store name (optional)
            address: Store address (optional)
            
        Returns:
            Dict: Analysis results with scores and recommendations
        """
        # TODO: Implement actual Claude Vision API call
        # For now, return mock analysis
        
        return self._generate_mock_analysis()
    
    def _generate_mock_analysis(self) -> Dict:
        """Generate mock analysis for development"""
        
        # Generate random but realistic scores
        base_score = random.randint(30, 90)
        
        # Visual signals (7 features)
        visual_signals = {
            "shelfDensityIndex": max(20, min(100, base_score + random.randint(-15, 15))),
            "skuDiversityScore": max(20, min(100, base_score + random.randint(-15, 15))),
            "inventoryValueBand": max(20, min(100, base_score + random.randint(-15, 15))),
            "refillSignal": max(20, min(100, base_score + random.randint(-15, 15))),
            "storeOrganizationScore": max(20, min(100, base_score + random.randint(-15, 15))),
            "counterActivityProxy": max(20, min(100, base_score + random.randint(-15, 15))),
            "exteriorQualityScore": max(20, min(100, base_score + random.randint(-15, 15))),
        }
        
        # Geo signals (5 features)
        geo_signals = {
            "roadTypeScore": max(20, min(100, base_score + random.randint(-15, 15))),
            "catchmentDensity": max(20, min(100, base_score + random.randint(-15, 15))),
            "footfallProxyIndex": max(20, min(100, base_score + random.randint(-15, 15))),
            "competitionDensity": max(20, min(100, base_score + random.randint(-15, 15))),
            "neighbourhoodQuality": max(20, min(100, base_score + random.randint(-15, 15))),
        }
        
        # Calculate CSQS (weighted average)
        visual_avg = sum(visual_signals.values()) / len(visual_signals)
        geo_avg = sum(geo_signals.values()) / len(geo_signals)
        csqs = int((visual_avg * 0.6) + (geo_avg * 0.4))  # 60% visual, 40% geo
        
        # Determine tier and recommendation
        if csqs >= 80:
            tier = "A"
            recommendation = "pre_approve"
        elif csqs >= 65:
            tier = "B"
            recommendation = "pre_approve" if csqs >= 75 else "needs_verification"
        elif csqs >= 50:
            tier = "C"
            recommendation = "needs_verification"
        elif csqs >= 35:
            tier = "D"
            recommendation = "needs_verification" if csqs >= 45 else "reject"
        else:
            tier = "E"
            recommendation = "reject"
        
        # Generate financial estimates based on tier
        tier_multipliers = {
            "A": (8, 12),    # High range
            "B": (5, 8),     # Good range
            "C": (3, 5),     # Medium range
            "D": (1.5, 3),   # Low range
            "E": (0.5, 1.5), # Very low range
        }
        
        min_mult, max_mult = tier_multipliers[tier]
        daily_sales_min = int(random.uniform(2000, 5000) * min_mult)
        daily_sales_max = int(random.uniform(5000, 8000) * max_mult)
        
        monthly_revenue_min = daily_sales_min * 30
        monthly_revenue_max = daily_sales_max * 30
        
        # Income is typically 15-25% of revenue
        income_rate = random.uniform(0.15, 0.25)
        monthly_income_min = int(monthly_revenue_min * income_rate)
        monthly_income_max = int(monthly_revenue_max * income_rate)
        
        # Confidence score
        confidence_score = random.randint(60, 95)
        
        # Generate risk flags for lower scores
        risk_flags = []
        if csqs < 70:
            possible_flags = [
                {"type": "medium", "message": "High competition in catchment area", "severity": 2},
                {"type": "medium", "message": "Irregular inventory refill patterns detected", "severity": 2},
                {"type": "low", "message": "Limited SKU diversity compared to area requirements", "severity": 1},
            ]
            
            if csqs < 50:
                possible_flags.extend([
                    {"type": "high", "message": "Significantly low inventory levels for operational viability", "severity": 4},
                    {"type": "high", "message": "Poor store exterior condition affecting customer perception", "severity": 3},
                ])
            
            # Add 1-3 random flags
            num_flags = random.randint(1, min(3, len(possible_flags)))
            risk_flags = random.sample(possible_flags, num_flags)
        
        return {
            "csqs": csqs,
            "store_tier": tier,
            "confidence_score": confidence_score,
            "daily_sales_min": daily_sales_min,
            "daily_sales_max": daily_sales_max,
            "monthly_revenue_min": monthly_revenue_min,
            "monthly_revenue_max": monthly_revenue_max,
            "monthly_income_min": monthly_income_min,
            "monthly_income_max": monthly_income_max,
            "recommendation": recommendation,
            "signal_breakdown": {
                "visual": visual_signals,
                "geo": geo_signals,
            },
            "risk_flags": risk_flags,
        }


# Global processor instance
ai_processor = AIProcessor()


async def process_assessment_images(
    assessment_id: UUID,
    image_urls: List[str],
    store_name: Optional[str] = None,
    address: Optional[str] = None,
) -> Dict:
    """
    Process assessment images and return analysis results.
    
    Args:
        assessment_id: Assessment UUID
        image_urls: List of image URLs
        store_name: Store name (optional)
        address: Store address (optional)
        
    Returns:
        Dict: Analysis results
    """
    return await ai_processor.analyze_store_images(
        image_urls=image_urls,
        store_name=store_name,
        address=address,
    )