"""
Assessment models for the KiranaLens assessment pipeline
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column, DateTime, Enum as SQLEnum, Float, ForeignKey, 
    Integer, Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class AssessmentStatus(str, Enum):
    """Assessment status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"


class InventoryValueBand(str, Enum):
    """Inventory value band enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RefillSignal(str, Enum):
    """Refill signal enumeration"""
    PARTIALLY_EMPTY = "partially_empty"
    NORMAL = "normal"
    OVERFILLED = "overfilled"


class Assessment(Base):
    """Main assessment model"""
    __tablename__ = "assessments"
    
    # Primary key and timestamps
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # User relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Store information
    store_name = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    lat = Column(Numeric(10, 7), nullable=False)
    lng = Column(Numeric(10, 7), nullable=False)
    gps_accuracy_metres = Column(Float, nullable=True)
    
    # Image storage
    image_urls = Column(JSONB, nullable=False, default=list)
    
    # Assessment status and processing
    status = Column(SQLEnum(AssessmentStatus, values_callable=lambda x: [e.value for e in x]), default=AssessmentStatus.PENDING, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    
    # AI Analysis Results
    csqs = Column(Numeric(5, 2), nullable=True)  # 0.00 to 100.00
    store_tier = Column(String(5), nullable=True)  # A, B, C, D, E
    confidence_score = Column(Numeric(3, 2), nullable=True)  # 0.00 to 1.00
    
    # Financial metrics (in rupees)
    daily_sales_min = Column(Integer, nullable=True)
    daily_sales_max = Column(Integer, nullable=True)
    monthly_revenue_min = Column(Integer, nullable=True)
    monthly_revenue_max = Column(Integer, nullable=True)
    monthly_income_min = Column(Integer, nullable=True)
    monthly_income_max = Column(Integer, nullable=True)
    
    # Risk and recommendation
    risk_flags = Column(JSONB, nullable=False, default=list)
    recommendation = Column(String(30), nullable=True)  # pre_approve, needs_verification, reject
    
    # Analysis breakdown
    signal_breakdown = Column(JSONB, nullable=True)  # All 12 signal scores
    
    # Report generation
    pdf_report_url = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    visual_features = relationship("VisualFeatures", back_populates="assessment", uselist=False, cascade="all, delete-orphan")
    geo_features = relationship("GeoFeatures", back_populates="assessment", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, store_name={self.store_name}, status={self.status})>"


class VisualFeatures(Base):
    """Visual features extracted from store images"""
    __tablename__ = "visual_features"
    
    # Primary key and relationship
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Visual analysis scores (0-100)
    shelf_density_index = Column(Integer, nullable=False)
    sku_diversity_score = Column(Integer, nullable=False)
    store_organization_score = Column(Integer, nullable=False)
    counter_activity_proxy = Column(Integer, nullable=False)
    exterior_quality_score = Column(Integer, nullable=False)
    
    # Categorical features
    inventory_value_band = Column(SQLEnum(InventoryValueBand, values_callable=lambda x: [e.value for e in x]), nullable=False)
    refill_signal = Column(SQLEnum(RefillSignal, values_callable=lambda x: [e.value for e in x]), nullable=False)
    
    # Quality and audit data
    image_quality_warnings = Column(JSONB, nullable=False, default=list)
    raw_claude_response = Column(JSONB, nullable=True)  # Full API response for audit
    
    # Relationships
    assessment = relationship("Assessment", back_populates="visual_features")
    
    def __repr__(self):
        return f"<VisualFeatures(assessment_id={self.assessment_id}, shelf_density={self.shelf_density_index})>"


class GeoFeatures(Base):
    """Geographic and location-based features"""
    __tablename__ = "geo_features"
    
    # Primary key and relationship
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Geographic analysis scores (0-100)
    road_type_score = Column(Integer, nullable=False)
    catchment_density_score = Column(Integer, nullable=False)
    footfall_proxy_index = Column(Integer, nullable=False)
    competition_density_score = Column(Integer, nullable=False)
    neighbourhood_quality_score = Column(Integer, nullable=False)
    
    # Raw counts
    competitor_count = Column(Integer, nullable=False, default=0)
    poi_count = Column(Integer, nullable=False, default=0)
    
    # Audit data
    raw_places_response = Column(JSONB, nullable=True)  # Google Places API response
    raw_overpass_response = Column(JSONB, nullable=True)  # OpenStreetMap Overpass API response
    
    # Relationships
    assessment = relationship("Assessment", back_populates="geo_features")
    
    def __repr__(self):
        return f"<GeoFeatures(assessment_id={self.assessment_id}, road_type={self.road_type_score})>"