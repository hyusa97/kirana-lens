"""
Assessments router
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, require_admin_and_api_key
from app.middleware.rate_limit import rate_limit_assessments, rate_limit_get_endpoints, rate_limit_general
from app.middleware.validation import sanitize_string_input, validate_india_coordinates
from app.models.assessment import AssessmentStatus
from app.models.user import User
from app.schemas.assessment import AssessmentListResponse, AssessmentResponse
from app.services.assessment_service import AssessmentService

router = APIRouter()


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
@rate_limit_assessments()
async def create_assessment(
    lat: float = Form(...),
    lng: float = Form(...),
    store_name: Optional[str] = Form(None),
    gps_accuracy_metres: Optional[float] = Form(None),
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    request: Request = None,
):
    """
    Create a new assessment with images.
    
    Args:
        lat: Latitude
        lng: Longitude
        store_name: Store name (optional)
        gps_accuracy_metres: GPS accuracy in metres (optional)
        images: List of image files (3-5 required)
        current_user: Current authenticated user
        db: Database session
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        AssessmentResponse: Created assessment
        
    Raises:
        HTTPException: If validation fails
    """
    # Validate coordinates are within India
    validate_india_coordinates(lat, lng)
    
    # Sanitize store name if provided
    if store_name:
        store_name = sanitize_string_input(store_name)
    
    assessment_service = AssessmentService(db)
    
    # Create assessment
    assessment = await assessment_service.create_assessment(
        user_id=current_user.id,
        files=images,
        lat=lat,
        lng=lng,
        store_name=store_name,
        gps_accuracy_metres=gps_accuracy_metres,
        background_tasks=background_tasks
    )
    
    return AssessmentResponse.from_orm(assessment)


@router.get("", response_model=AssessmentListResponse)
@rate_limit_get_endpoints()
async def get_assessments(
    page: int = 1,
    limit: int = 20,
    status_filter: Optional[str] = None,
    store_tier: Optional[str] = None,
    recommendation: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Get paginated list of assessments.
    
    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 20)
        status_filter: Filter by status (pending, processing, complete, error)
        store_tier: Filter by store tier (A, B, C, D, E)
        recommendation: Filter by recommendation type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        AssessmentListResponse: Paginated assessments
    """
    assessment_service = AssessmentService(db)
    
    # Convert string status to enum if provided
    status_enum = None
    if status_filter:
        try:
            status_enum = AssessmentStatus(status_filter)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}"
            )
    
    result = await assessment_service.get_assessments(
        user_id=current_user.id,
        page=page,
        limit=limit,
        status=status_enum,
        store_tier=store_tier,
        recommendation=recommendation,
    )
    
    return result


@router.get("/{assessment_id}", response_model=AssessmentResponse)
@rate_limit_get_endpoints()
async def get_assessment(
    assessment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Get single assessment by ID.
    
    Args:
        assessment_id: Assessment UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        AssessmentResponse: Assessment data
        
    Raises:
        HTTPException: If assessment not found
    """
    assessment_service = AssessmentService(db)
    
    assessment = await assessment_service.get_assessment(assessment_id, current_user.id)
    
    return AssessmentResponse.from_orm(assessment)


@router.get("/{assessment_id}/status")
@rate_limit_get_endpoints()
async def get_assessment_status(
    assessment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Get assessment status and progress for polling.
    
    Args:
        assessment_id: Assessment UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Status information with progress step
        
    Raises:
        HTTPException: If assessment not found
    """
    assessment_service = AssessmentService(db)
    
    return await assessment_service.get_assessment_status(assessment_id, current_user.id)


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assessment(
    assessment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an assessment.
    
    Args:
        assessment_id: Assessment UUID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If assessment not found
    """
    # Note: Delete functionality not implemented in service yet
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete assessment not yet implemented"
    )


@router.post("/{assessment_id}/reprocess", response_model=AssessmentResponse)
async def reprocess_assessment(
    assessment_id: UUID,
    current_user: User = Depends(require_admin_and_api_key),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Reprocess an existing assessment.
    
    Requires both admin role and valid API key.
    
    Args:
        assessment_id: Assessment UUID
        current_user: Current authenticated admin user
        db: Database session
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        AssessmentResponse: Updated assessment
        
    Raises:
        HTTPException: If assessment not found or access denied
    """
    assessment_service = AssessmentService(db)
    
    assessment = await assessment_service.reprocess_assessment(
        assessment_id, current_user.id, background_tasks
    )
    
    return AssessmentResponse.from_orm(assessment)


@router.get("/{assessment_id}/report")
@rate_limit_general()
async def download_report(
    assessment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Download assessment report as PDF.
    
    Args:
        assessment_id: Assessment UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        FileResponse: PDF report
        
    Raises:
        HTTPException: If assessment not found or report generation fails
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="PDF report generation not yet implemented"
    )
