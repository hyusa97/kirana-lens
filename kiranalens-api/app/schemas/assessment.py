"""
Assessment Pydantic schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.models.assessment import AssessmentStatus, InventoryValueBand, RefillSignal


class CreateAssessmentRequest(BaseModel):
    """Request schema for creating a new assessment"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    lng: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    store_name: Optional[str] = Field(None, max_length=200, description="Store name")
    gps_accuracy_metres: Optional[float] = Field(None, ge=0, description="GPS accuracy in metres")
    
    class Config:
        json_schema_extra = {
            "example": {
                "lat": 19.0760,
                "lng": 72.8777,
                "store_name": "Sharma General Store",
                "gps_accuracy_metres": 5.0
            }
        }


class SignalBreakdown(BaseModel):
    """Signal breakdown schema with all 12 signals"""
    # Visual signals
    shelf_density_index: float = Field(..., ge=0, le=100)
    sku_diversity_score: float = Field(..., ge=0, le=100)
    inventory_value_band: float = Field(..., ge=0, le=100)
    refill_signal: float = Field(..., ge=0, le=100)
    store_organization_score: float = Field(..., ge=0, le=100)
    counter_activity_proxy: float = Field(..., ge=0, le=100)
    exterior_quality_score: float = Field(..., ge=0, le=100)
    
    # Geographic signals
    road_type_score: float = Field(..., ge=0, le=100)
    catchment_density_score: float = Field(..., ge=0, le=100)
    footfall_proxy_index: float = Field(..., ge=0, le=100)
    competition_density_score: float = Field(..., ge=0, le=100)
    neighbourhood_quality_score: float = Field(..., ge=0, le=100)


class VisualFeaturesResponse(BaseModel):
    """Visual features response schema (excluding raw responses)"""
    id: UUID
    assessment_id: UUID
    shelf_density_index: int
    sku_diversity_score: int
    store_organization_score: int
    counter_activity_proxy: int
    exterior_quality_score: int
    inventory_value_band: InventoryValueBand
    refill_signal: RefillSignal
    image_quality_warnings: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class GeoFeaturesResponse(BaseModel):
    """Geographic features response schema (excluding raw responses)"""
    id: UUID
    assessment_id: UUID
    road_type_score: int
    catchment_density_score: int
    footfall_proxy_index: int
    competition_density_score: int
    neighbourhood_quality_score: int
    competitor_count: int
    poi_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssessmentResponse(BaseModel):
    """Complete assessment response schema"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    
    # Store information
    store_name: Optional[str]
    address: Optional[str]
    lat: Decimal
    lng: Decimal
    gps_accuracy_metres: Optional[float]
    
    # Image storage
    image_urls: List[str]
    
    # Assessment status
    status: AssessmentStatus
    error_message: Optional[str]
    
    # AI Analysis Results
    csqs: Optional[Decimal]
    store_tier: Optional[str]
    confidence_score: Optional[Decimal]
    
    # Financial metrics
    daily_sales_min: Optional[int]
    daily_sales_max: Optional[int]
    monthly_revenue_min: Optional[int]
    monthly_revenue_max: Optional[int]
    monthly_income_min: Optional[int]
    monthly_income_max: Optional[int]
    
    # Risk and recommendation
    risk_flags: List[str]
    recommendation: Optional[str]
    
    # Analysis breakdown
    signal_breakdown: Optional[Dict[str, float]]
    
    # Report
    pdf_report_url: Optional[str]
    
    # Related data (optional)
    visual_features: Optional[VisualFeaturesResponse]
    geo_features: Optional[GeoFeaturesResponse]
    
    class Config:
        from_attributes = True


class AssessmentListResponse(BaseModel):
    """Paginated list of assessments"""
    items: List[AssessmentResponse]
    total: int
    page: int
    limit: int
    pages: int
    
    @validator('pages', pre=True, always=True)
    def calculate_pages(cls, v, values):
        """Calculate total pages"""
        total = values.get('total', 0)
        limit = values.get('limit', 10)
        return (total + limit - 1) // limit if total > 0 else 0


class UpdateAssessmentStatus(BaseModel):
    """Schema for updating assessment status"""
    status: AssessmentStatus
    error_message: Optional[str] = None
    
    @validator('error_message')
    def error_message_required_for_error_status(cls, v, values):
        """Require error message when status is ERROR"""
        if values.get('status') == AssessmentStatus.ERROR and not v:
            raise ValueError('error_message is required when status is ERROR')
        return v


class AssessmentSummary(BaseModel):
    """Summary schema for dashboard and lists"""
    id: UUID
    created_at: datetime
    store_name: Optional[str]
    status: AssessmentStatus
    csqs: Optional[Decimal]
    store_tier: Optional[str]
    recommendation: Optional[str]
    confidence_score: Optional[Decimal]
    
    class Config:
        from_attributes = True


class AssessmentFilters(BaseModel):
    """Filters for assessment queries"""
    status: Optional[AssessmentStatus] = None
    store_tier: Optional[str] = Field(None, pattern=r'^[ABCDE]$')
    recommendation: Optional[str] = Field(None, pattern=r'^(pre_approve|needs_verification|reject)$')
    min_csqs: Optional[float] = Field(None, ge=0, le=100)
    max_csqs: Optional[float] = Field(None, ge=0, le=100)
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    
    @validator('max_csqs')
    def max_csqs_greater_than_min(cls, v, values):
        """Ensure max_csqs is greater than min_csqs"""
        min_csqs = values.get('min_csqs')
        if min_csqs is not None and v is not None and v < min_csqs:
            raise ValueError('max_csqs must be greater than or equal to min_csqs')
        return v