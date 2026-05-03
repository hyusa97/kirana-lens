"""
Background task for processing assessments
"""
import asyncio
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.assessment import Assessment, RiskFlag
from app.utils.ai_processor import process_assessment_images
from app.utils.geocoding import get_address_from_coordinates


async def process_assessment_async(assessment_id: UUID):
    """
    Background task to process assessment with AI analysis.
    
    Args:
        assessment_id: Assessment UUID to process
    """
    async with AsyncSessionLocal() as db:
        try:
            # Get assessment
            result = await db.execute(
                select(Assessment).where(Assessment.id == assessment_id)
            )
            assessment = result.scalar_one_or_none()
            
            if not assessment:
                print(f"❌ Assessment {assessment_id} not found")
                return
            
            print(f"🔄 Processing assessment {assessment_id}...")
            
            # Get address from coordinates
            if not assessment.address:
                address = await get_address_from_coordinates(
                    assessment.lat,
                    assessment.lng
                )
                if address:
                    assessment.address = address
            
            # Get image URLs
            image_urls = [img.image_url for img in assessment.images]
            
            # Process with AI
            analysis = await process_assessment_images(
                assessment_id=assessment_id,
                image_urls=image_urls,
                store_name=assessment.store_name,
                address=assessment.address,
            )
            
            # Update assessment with results
            assessment.csqs = analysis["csqs"]
            assessment.store_tier = analysis["store_tier"]
            assessment.confidence_score = analysis["confidence_score"]
            assessment.daily_sales_min = analysis["daily_sales_min"]
            assessment.daily_sales_max = analysis["daily_sales_max"]
            assessment.monthly_revenue_min = analysis["monthly_revenue_min"]
            assessment.monthly_revenue_max = analysis["monthly_revenue_max"]
            assessment.monthly_income_min = analysis["monthly_income_min"]
            assessment.monthly_income_max = analysis["monthly_income_max"]
            assessment.recommendation = analysis["recommendation"]
            assessment.signal_breakdown = analysis["signal_breakdown"]
            assessment.status = "completed"
            assessment.completed_at = datetime.utcnow()
            
            # Add risk flags
            for flag_data in analysis["risk_flags"]:
                risk_flag = RiskFlag(
                    assessment_id=assessment_id,
                    type=flag_data["type"],
                    message=flag_data["message"],
                    severity=flag_data["severity"],
                )
                db.add(risk_flag)
            
            await db.commit()
            
            print(f"✅ Assessment {assessment_id} processed successfully")
            print(f"   CSQS: {assessment.csqs}")
            print(f"   Tier: {assessment.store_tier}")
            print(f"   Recommendation: {assessment.recommendation}")
            
        except Exception as e:
            print(f"❌ Error processing assessment {assessment_id}: {e}")
            await db.rollback()
            
            # Mark as failed
            try:
                result = await db.execute(
                    select(Assessment).where(Assessment.id == assessment_id)
                )
                assessment = result.scalar_one_or_none()
                if assessment:
                    assessment.status = "failed"
                    await db.commit()
            except Exception:
                pass


def start_assessment_processing(assessment_id: UUID):
    """
    Start background processing for an assessment.
    
    Args:
        assessment_id: Assessment UUID to process
    """
    # In a real application, you would use a task queue like Celery or RQ
    # For now, we'll use asyncio to run the task in the background
    asyncio.create_task(process_assessment_async(assessment_id))