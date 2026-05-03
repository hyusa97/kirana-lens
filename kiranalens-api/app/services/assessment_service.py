"""
Assessment service for business logic and pipeline orchestration
"""
import asyncio
from typing import List, Optional
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.assessment import Assessment, AssessmentStatus, GeoFeatures, VisualFeatures
from app.schemas.assessment import AssessmentListResponse, AssessmentResponse
from app.services.geo_service import GeoService
from app.services.storage_service import StorageService
from app.services.vision_service import VisionService
from app.utils.scoring import (
    compute_confidence, compute_csqs, csqs_to_revenue_ranges, csqs_to_tier,
    detect_fraud_flags, get_recommendation, inventory_band_to_score, refill_signal_to_score
)


class AssessmentService:
    """Service for assessment-related operations and AI pipeline"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self._storage_service = None
        self._vision_service = None
        self._geo_service = None
    
    @property
    def storage_service(self):
        if self._storage_service is None:
            # Try to use real Supabase storage, fall back to mock if invalid
            try:
                from app.services.storage_service import StorageService
                self._storage_service = StorageService()
            except Exception as e:
                # Fall back to mock storage for testing
                print(f"[WARNING] Supabase not configured ({str(e)}), using mock storage")
                from app.services.mock_storage_service import MockStorageService
                self._storage_service = MockStorageService()
        return self._storage_service
    
    @property
    def vision_service(self):
        if self._vision_service is None:
            self._vision_service = VisionService()
        return self._vision_service
    
    @property
    def geo_service(self):
        if self._geo_service is None:
            self._geo_service = GeoService()
        return self._geo_service
    
    async def create_assessment(
        self,
        user_id: UUID,
        files: List[UploadFile],
        lat: float,
        lng: float,
        store_name: Optional[str] = None,
        gps_accuracy_metres: Optional[float] = None,
        background_tasks: BackgroundTasks = None
    ) -> Assessment:
        """
        Create a new assessment and trigger processing pipeline.
        
        Args:
            user_id: ID of the user creating the assessment
            files: List of uploaded image files
            lat: Latitude coordinate
            lng: Longitude coordinate
            store_name: Optional store name
            gps_accuracy_metres: Optional GPS accuracy in metres
            background_tasks: FastAPI background tasks for async processing
            
        Returns:
            Assessment: Created assessment record
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate image count
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
        
        try:
            # Create assessment record with pending status
            assessment = Assessment(
                user_id=user_id,
                store_name=store_name,
                lat=lat,
                lng=lng,
                gps_accuracy_metres=gps_accuracy_metres,
                status=AssessmentStatus.PENDING,
                image_urls=[],  # Will be updated after upload
                risk_flags=[],
                signal_breakdown={}
            )
            
            self.db.add(assessment)
            await self.db.flush()  # Get the ID
            await self.db.refresh(assessment)
            
            # Upload images to storage
            image_urls = await self.storage_service.upload_images(files, str(assessment.id))
            
            # Update assessment with image URLs and set to processing
            assessment.image_urls = image_urls
            assessment.status = AssessmentStatus.PROCESSING
            await self.db.commit()
            
            # Trigger background processing pipeline
            if background_tasks:
                background_tasks.add_task(self.run_pipeline, str(assessment.id))
            else:
                # For testing or synchronous execution
                asyncio.create_task(self.run_pipeline(str(assessment.id)))
            
            return assessment
            
        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create assessment: {str(e)}"
            )
    
    async def run_pipeline(self, assessment_id: str) -> None:
        """
        Run the complete AI analysis pipeline for an assessment.
        
        Args:
            assessment_id: Assessment ID to process
        """
        try:
            # Fetch assessment
            result = await self.db.execute(
                select(Assessment).where(Assessment.id == assessment_id)
            )
            assessment = result.scalar_one_or_none()
            
            if not assessment:
                raise ValueError(f"Assessment {assessment_id} not found")
            
            print(f"🔄 Starting pipeline for assessment {assessment_id}")
            
            # Step 1: Vision analysis
            print("📸 Step 1: Analyzing images...")
            vision_result = await self.vision_service.analyze_images(assessment.image_urls)
            
            # Save visual features
            visual_features = VisualFeatures(
                assessment_id=assessment.id,
                shelf_density_index=vision_result["shelf_density_index"],
                sku_diversity_score=vision_result["sku_diversity_score"],
                store_organization_score=vision_result["store_organization_score"],
                counter_activity_proxy=vision_result["counter_activity_proxy"],
                exterior_quality_score=vision_result["exterior_quality_score"],
                inventory_value_band=vision_result["inventory_value_band"],
                refill_signal=vision_result["refill_signal"],
                image_quality_warnings=vision_result["image_quality_warnings"],
                raw_claude_response=vision_result["raw_claude_response"]
            )
            self.db.add(visual_features)
            
            # Step 2: Geographic analysis
            print("🗺️  Step 2: Analyzing location...")
            geo_result = await self.geo_service.analyze_location(
                float(assessment.lat), float(assessment.lng)
            )
            
            # Save geographic features
            geo_features = GeoFeatures(
                assessment_id=assessment.id,
                road_type_score=geo_result["road_type_score"],
                catchment_density_score=geo_result["catchment_density_score"],
                footfall_proxy_index=geo_result["footfall_proxy_index"],
                competition_density_score=geo_result["competition_density_score"],
                neighbourhood_quality_score=geo_result["neighbourhood_quality_score"],
                competitor_count=geo_result["competitor_count"],
                poi_count=geo_result["poi_count"],
                raw_places_response=geo_result["raw_places_response"],
                raw_overpass_response=geo_result["raw_overpass_response"]
            )
            self.db.add(geo_features)
            
            # Step 3: Compute CSQS score
            print("🧮 Step 3: Computing CSQS score...")
            visual_dict = {
                "shelf_density_index": vision_result["shelf_density_index"],
                "sku_diversity_score": vision_result["sku_diversity_score"],
                "inventory_value_band": inventory_band_to_score(vision_result["inventory_value_band"]),
                "refill_signal": refill_signal_to_score(vision_result["refill_signal"]),
                "store_organization_score": vision_result["store_organization_score"],
                "counter_activity_proxy": vision_result["counter_activity_proxy"],
                "exterior_quality_score": vision_result["exterior_quality_score"]
            }
            
            geo_dict = {
                "road_type_score": geo_result["road_type_score"],
                "catchment_density_score": geo_result["catchment_density_score"],
                "footfall_proxy_index": geo_result["footfall_proxy_index"],
                "competition_density_score": geo_result["competition_density_score"],
                "neighbourhood_quality_score": geo_result["neighbourhood_quality_score"]
            }
            
            csqs = compute_csqs(visual_dict, geo_dict)
            
            # Step 4: Determine store tier
            print("🏪 Step 4: Determining store tier...")
            store_tier = csqs_to_tier(csqs)
            
            # Step 5: Calculate revenue ranges
            print("💰 Step 5: Calculating revenue ranges...")
            revenue_ranges = csqs_to_revenue_ranges(csqs)
            
            # Step 6: Compute confidence score
            print("📊 Step 6: Computing confidence score...")
            confidence_score = compute_confidence(
                visual_dict,
                geo_dict,
                len(assessment.image_urls),
                assessment.gps_accuracy_metres
            )
            
            # Step 7: Detect fraud flags
            print("🚩 Step 7: Detecting fraud flags...")
            fraud_flags = detect_fraud_flags(visual_dict, geo_dict)
            
            # Step 8: Get recommendation
            print("✅ Step 8: Generating recommendation...")
            recommendation = get_recommendation(confidence_score, fraud_flags, csqs)
            
            # Update assessment with all results
            assessment.csqs = csqs
            assessment.store_tier = store_tier
            assessment.confidence_score = confidence_score
            assessment.daily_sales_min = revenue_ranges["daily_sales_min"]
            assessment.daily_sales_max = revenue_ranges["daily_sales_max"]
            assessment.monthly_revenue_min = revenue_ranges["monthly_revenue_min"]
            assessment.monthly_revenue_max = revenue_ranges["monthly_revenue_max"]
            assessment.monthly_income_min = revenue_ranges["monthly_income_min"]
            assessment.monthly_income_max = revenue_ranges["monthly_income_max"]
            assessment.risk_flags = fraud_flags
            assessment.recommendation = recommendation
            assessment.signal_breakdown = {**visual_dict, **geo_dict}
            assessment.status = AssessmentStatus.COMPLETE
            
            await self.db.commit()
            
            print(f"✅ Pipeline completed for assessment {assessment_id}")
            print(f"   CSQS: {csqs:.2f}")
            print(f"   Tier: {store_tier}")
            print(f"   Recommendation: {recommendation}")
            print(f"   Confidence: {confidence_score:.2f}")
            
        except Exception as e:
            print(f"❌ Pipeline failed for assessment {assessment_id}: {e}")
            
            # Update assessment with error status
            try:
                result = await self.db.execute(
                    select(Assessment).where(Assessment.id == assessment_id)
                )
                assessment = result.scalar_one_or_none()
                if assessment:
                    assessment.status = AssessmentStatus.ERROR
                    assessment.error_message = str(e)
                    await self.db.commit()
            except Exception:
                pass
            
            # Re-raise the exception for logging
            raise
    
    async def get_assessments(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        status: Optional[AssessmentStatus] = None,
        store_tier: Optional[str] = None,
        recommendation: Optional[str] = None
    ) -> AssessmentListResponse:
        """
        Get paginated list of assessments for a user.
        
        Args:
            user_id: User ID to filter assessments
            page: Page number (1-based)
            limit: Number of items per page
            status: Optional status filter
            store_tier: Optional tier filter
            recommendation: Optional recommendation filter
            
        Returns:
            AssessmentListResponse: Paginated assessment list
        """
        from sqlalchemy.orm import selectinload
        
        # Build query with eager loading of relationships
        query = select(Assessment).options(
            selectinload(Assessment.visual_features),
            selectinload(Assessment.geo_features)
        ).where(Assessment.user_id == user_id)
        
        # Apply filters
        if status:
            query = query.where(Assessment.status == status)
        if store_tier:
            query = query.where(Assessment.store_tier == store_tier)
        if recommendation:
            query = query.where(Assessment.recommendation == recommendation)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit).order_by(Assessment.created_at.desc())
        
        # Execute query
        result = await self.db.execute(query)
        assessments = result.scalars().all()
        
        # Convert to response objects
        assessment_responses = [
            AssessmentResponse.from_orm(assessment) for assessment in assessments
        ]
        
        # Calculate pages
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return AssessmentListResponse(
            items=assessment_responses,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
    
    async def get_assessment(self, assessment_id: UUID, user_id: UUID) -> Assessment:
        """
        Get a single assessment by ID.
        
        Args:
            assessment_id: Assessment ID
            user_id: User ID for authorization
            
        Returns:
            Assessment: Assessment record with related data
            
        Raises:
            HTTPException: If assessment not found or access denied
        """
        result = await self.db.execute(
            select(Assessment)
            .where(Assessment.id == assessment_id)
            .where(Assessment.user_id == user_id)
        )
        assessment = result.scalar_one_or_none()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        
        return assessment
    
    async def reprocess_assessment(self, assessment_id: UUID, user_id: UUID, background_tasks: BackgroundTasks) -> Assessment:
        """
        Reprocess an existing assessment.
        
        Args:
            assessment_id: Assessment ID to reprocess
            user_id: User ID for authorization
            background_tasks: FastAPI background tasks
            
        Returns:
            Assessment: Updated assessment record
            
        Raises:
            HTTPException: If assessment not found or access denied
        """
        assessment = await self.get_assessment(assessment_id, user_id)
        
        # Reset assessment status and clear previous results
        assessment.status = AssessmentStatus.PROCESSING
        assessment.csqs = None
        assessment.store_tier = None
        assessment.confidence_score = None
        assessment.recommendation = None
        assessment.risk_flags = []
        assessment.signal_breakdown = {}
        assessment.error_message = None
        
        await self.db.commit()
        
        # Trigger reprocessing
        background_tasks.add_task(self.run_pipeline, str(assessment_id))
        
        return assessment
    
    async def get_assessment_status(self, assessment_id: UUID, user_id: UUID) -> dict:
        """
        Get assessment status and progress for polling.
        
        Args:
            assessment_id: Assessment ID
            user_id: User ID for authorization
            
        Returns:
            dict: Status information with progress step
        """
        assessment = await self.get_assessment(assessment_id, user_id)
        
        # Determine progress step based on what's completed
        progress_step = 0
        
        if assessment.status == AssessmentStatus.PENDING:
            progress_step = 0
        elif assessment.status == AssessmentStatus.PROCESSING:
            # Check what data exists to determine progress
            # Query for related features to determine progress
            visual_result = await self.db.execute(
                select(VisualFeatures).where(VisualFeatures.assessment_id == assessment.id)
            )
            visual_features = visual_result.scalar_one_or_none()
            
            geo_result = await self.db.execute(
                select(GeoFeatures).where(GeoFeatures.assessment_id == assessment.id)
            )
            geo_features = geo_result.scalar_one_or_none()
            
            if visual_features:
                progress_step = 2  # Vision analysis complete
            if geo_features:
                progress_step = 4  # Geographic analysis complete
            if assessment.csqs is not None:
                progress_step = 6  # Scoring complete
        elif assessment.status == AssessmentStatus.COMPLETE:
            progress_step = 6
        elif assessment.status == AssessmentStatus.ERROR:
            progress_step = -1
        
        return {
            "id": str(assessment.id),
            "status": assessment.status.value,
            "progress_step": progress_step,
            "error_message": assessment.error_message
        }
