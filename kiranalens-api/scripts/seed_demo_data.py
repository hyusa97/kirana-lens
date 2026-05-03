#!/usr/bin/env python3
"""
Demo data seeding script for KiranaLens

Creates 3 fully-processed demo assessments with realistic data:
1. Sharma General Store (Mumbai) - High-performing store
2. Gupta Kirana (Nagpur) - Medium-performing store with risk flags
3. Lal Dukan (Rural UP) - Low-performing store

Also creates a demo admin user for testing.

Usage:
    python scripts/seed_demo_data.py
"""
import asyncio
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import AsyncSessionLocal, engine
from app.models.assessment import Assessment, AssessmentStatus, VisualFeatures, GeoFeatures, InventoryValueBand, RefillSignal
from app.models.user import User, UserRole
from app.services.auth_service import AuthService


from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_demo_user(db: AsyncSession) -> User:
    """Create demo admin user"""
    print("🔧 Creating demo user...")
    
    # Check if demo user already exists
    result = await db.execute(
        select(User).where(User.email == "demo@kiranalens.com")
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        print("   ✅ Demo user already exists")
        return existing_user
    
    # Create demo user
    demo_user = User(
        id=uuid4(),
        email="demo@kiranalens.com",
        name="Demo Admin",
        organisation="KiranaLens Demo",
        hashed_password=_pwd_context.hash("Demo@1234"),
        role="admin",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    
    db.add(demo_user)
    await db.flush()
    
    print(f"   ✅ Created demo user: {demo_user.email}")
    return demo_user


async def create_demo_assessment_1(db: AsyncSession, user: User) -> Assessment:
    """Create Demo 1: Sharma General Store (High-performing)"""
    print("🏪 Creating Demo 1: Sharma General Store...")
    
    # Create main assessment
    assessment = Assessment(
        id=uuid4(),
        user_id=user.id,
        store_name="Sharma General Store",
        address="Shop 15, Andheri West, Mumbai, Maharashtra 400058",
        lat=Decimal("19.1136"),
        lng=Decimal("72.8697"),
        gps_accuracy_metres=3.2,
        image_urls=[
            "https://example.com/demo/sharma_exterior.jpg",
            "https://example.com/demo/sharma_interior.jpg",
            "https://example.com/demo/sharma_shelves.jpg"
        ],
        status=AssessmentStatus.COMPLETE,
        csqs=Decimal("82.1"),
        store_tier="A",
        confidence_score=Decimal("0.87"),
        daily_sales_min=8000,
        daily_sales_max=15000,
        monthly_revenue_min=240000,
        monthly_revenue_max=450000,
        monthly_income_min=36000,
        monthly_income_max=67500,
        risk_flags=[],
        recommendation="pre_approve",
        signal_breakdown={
            "shelf_density_index": 88.5,
            "sku_diversity_score": 92.3,
            "inventory_value_band": 85.7,
            "refill_signal": 78.9,
            "store_organization_score": 91.2,
            "counter_activity_proxy": 84.6,
            "exterior_quality_score": 89.1,
            "road_type_score": 95.2,
            "catchment_density_score": 87.4,
            "footfall_proxy_index": 93.8,
            "competition_density_score": 76.3,
            "neighbourhood_quality_score": 88.7
        },
        created_at=datetime.utcnow() - timedelta(days=2),
        updated_at=datetime.utcnow() - timedelta(days=2)
    )
    
    db.add(assessment)
    await db.flush()
    
    # Create visual features
    visual_features = VisualFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        shelf_density_index=89,
        sku_diversity_score=92,
        store_organization_score=91,
        counter_activity_proxy=85,
        exterior_quality_score=89,
        inventory_value_band=InventoryValueBand.HIGH,
        refill_signal=RefillSignal.NORMAL,
        image_quality_warnings=[],
        raw_claude_response={
            "model": "claude-3-haiku-20240307",
            "analysis": "Well-organized store with high inventory density",
            "confidence": 0.87
        },
        created_at=datetime.utcnow() - timedelta(days=2)
    )
    
    db.add(visual_features)
    
    # Create geo features
    geo_features = GeoFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        road_type_score=95,
        catchment_density_score=87,
        footfall_proxy_index=94,
        competition_density_score=76,
        neighbourhood_quality_score=89,
        competitor_count=3,
        poi_count=12,
        raw_places_response={
            "status": "OK",
            "results": [
                {"name": "Andheri West Market", "types": ["shopping_mall"]},
                {"name": "Local Bank", "types": ["bank"]},
                {"name": "Bus Stop", "types": ["transit_station"]}
            ]
        },
        raw_overpass_response={
            "elements": [
                {"tags": {"shop": "convenience"}, "lat": 19.1140, "lon": 72.8700},
                {"tags": {"amenity": "bank"}, "lat": 19.1130, "lon": 72.8690}
            ]
        },
        created_at=datetime.utcnow() - timedelta(days=2)
    )
    
    db.add(geo_features)
    
    print(f"   ✅ Created assessment: {assessment.store_name} (CSQS: {assessment.csqs})")
    return assessment


async def create_demo_assessment_2(db: AsyncSession, user: User) -> Assessment:
    """Create Demo 2: Gupta Kirana (Medium-performing with risk flags)"""
    print("🏪 Creating Demo 2: Gupta Kirana...")
    
    # Create main assessment
    assessment = Assessment(
        id=uuid4(),
        user_id=user.id,
        store_name="Gupta Kirana",
        address="Near Sitabuldi Fort, Nagpur, Maharashtra 440012",
        lat=Decimal("21.1458"),
        lng=Decimal("79.0882"),
        gps_accuracy_metres=8.1,
        image_urls=[
            "https://example.com/demo/gupta_exterior.jpg",
            "https://example.com/demo/gupta_interior.jpg",
            "https://example.com/demo/gupta_shelves.jpg",
            "https://example.com/demo/gupta_counter.jpg"
        ],
        status=AssessmentStatus.COMPLETE,
        csqs=Decimal("52.4"),
        store_tier="C",
        confidence_score=Decimal("0.61"),
        daily_sales_min=2000,
        daily_sales_max=4000,
        monthly_revenue_min=60000,
        monthly_revenue_max=120000,
        monthly_income_min=9000,
        monthly_income_max=18000,
        risk_flags=["competitor_saturation", "refill_signal_overfilled"],
        recommendation="needs_verification",
        signal_breakdown={
            "shelf_density_index": 45.2,
            "sku_diversity_score": 58.7,
            "inventory_value_band": 62.1,
            "refill_signal": 35.8,  # Low due to overfilled flag
            "store_organization_score": 51.3,
            "counter_activity_proxy": 48.9,
            "exterior_quality_score": 55.6,
            "road_type_score": 67.4,
            "catchment_density_score": 52.8,
            "footfall_proxy_index": 59.2,
            "competition_density_score": 28.5,  # Low due to saturation
            "neighbourhood_quality_score": 61.7
        },
        created_at=datetime.utcnow() - timedelta(days=5),
        updated_at=datetime.utcnow() - timedelta(days=5)
    )
    
    db.add(assessment)
    await db.flush()
    
    # Create visual features
    visual_features = VisualFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        shelf_density_index=45,
        sku_diversity_score=59,
        store_organization_score=51,
        counter_activity_proxy=49,
        exterior_quality_score=56,
        inventory_value_band=InventoryValueBand.MEDIUM,
        refill_signal=RefillSignal.OVERFILLED,
        image_quality_warnings=["slight_blur_detected"],
        raw_claude_response={
            "model": "claude-3-haiku-20240307",
            "analysis": "Moderate organization, some overstocking observed",
            "confidence": 0.61
        },
        created_at=datetime.utcnow() - timedelta(days=5)
    )
    
    db.add(visual_features)
    
    # Create geo features
    geo_features = GeoFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        road_type_score=67,
        catchment_density_score=53,
        footfall_proxy_index=59,
        competition_density_score=29,  # Low due to high competition
        neighbourhood_quality_score=62,
        competitor_count=8,  # High competition
        poi_count=6,
        raw_places_response={
            "status": "OK",
            "results": [
                {"name": "Sitabuldi Market", "types": ["shopping_mall"]},
                {"name": "Competitor Store 1", "types": ["grocery_or_supermarket"]},
                {"name": "Competitor Store 2", "types": ["grocery_or_supermarket"]}
            ]
        },
        raw_overpass_response={
            "elements": [
                {"tags": {"shop": "convenience"}, "lat": 21.1460, "lon": 79.0880},
                {"tags": {"shop": "convenience"}, "lat": 21.1455, "lon": 79.0885},
                {"tags": {"shop": "supermarket"}, "lat": 21.1450, "lon": 79.0890}
            ]
        },
        created_at=datetime.utcnow() - timedelta(days=5)
    )
    
    db.add(geo_features)
    
    print(f"   ✅ Created assessment: {assessment.store_name} (CSQS: {assessment.csqs})")
    return assessment


async def create_demo_assessment_3(db: AsyncSession, user: User) -> Assessment:
    """Create Demo 3: Lal Dukan (Low-performing rural store)"""
    print("🏪 Creating Demo 3: Lal Dukan...")
    
    # Create main assessment
    assessment = Assessment(
        id=uuid4(),
        user_id=user.id,
        store_name="Lal Dukan",
        address="Village Road, Near Lucknow, Uttar Pradesh 226010",
        lat=Decimal("26.8467"),
        lng=Decimal("80.9462"),
        gps_accuracy_metres=15.7,  # Poor GPS accuracy
        image_urls=[
            "https://example.com/demo/lal_exterior.jpg",
            "https://example.com/demo/lal_interior.jpg",
            "https://example.com/demo/lal_shelves.jpg"
        ],
        status=AssessmentStatus.COMPLETE,
        csqs=Decimal("18.7"),
        store_tier="E",
        confidence_score=Decimal("0.43"),
        daily_sales_min=200,
        daily_sales_max=800,
        monthly_revenue_min=6000,
        monthly_revenue_max=24000,
        monthly_income_min=900,
        monthly_income_max=3600,
        risk_flags=["gps_accuracy_low"],
        recommendation="reject",
        signal_breakdown={
            "shelf_density_index": 15.3,
            "sku_diversity_score": 22.1,
            "inventory_value_band": 18.9,
            "refill_signal": 25.4,
            "store_organization_score": 12.7,
            "counter_activity_proxy": 8.2,
            "exterior_quality_score": 19.6,
            "road_type_score": 35.8,
            "catchment_density_score": 14.2,
            "footfall_proxy_index": 11.5,
            "competition_density_score": 45.3,  # Higher due to less competition
            "neighbourhood_quality_score": 28.7
        },
        created_at=datetime.utcnow() - timedelta(days=7),
        updated_at=datetime.utcnow() - timedelta(days=7)
    )
    
    db.add(assessment)
    await db.flush()
    
    # Create visual features
    visual_features = VisualFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        shelf_density_index=15,
        sku_diversity_score=22,
        store_organization_score=13,
        counter_activity_proxy=8,
        exterior_quality_score=20,
        inventory_value_band=InventoryValueBand.LOW,
        refill_signal=RefillSignal.PARTIALLY_EMPTY,
        image_quality_warnings=["low_lighting", "image_quality_poor"],
        raw_claude_response={
            "model": "claude-3-haiku-20240307",
            "analysis": "Small rural store with limited inventory and organization",
            "confidence": 0.43
        },
        created_at=datetime.utcnow() - timedelta(days=7)
    )
    
    db.add(visual_features)
    
    # Create geo features
    geo_features = GeoFeatures(
        id=uuid4(),
        assessment_id=assessment.id,
        road_type_score=36,
        catchment_density_score=14,
        footfall_proxy_index=12,
        competition_density_score=45,  # Less competition in rural area
        neighbourhood_quality_score=29,
        competitor_count=1,
        poi_count=2,
        raw_places_response={
            "status": "OK",
            "results": [
                {"name": "Village School", "types": ["school"]},
                {"name": "Local Temple", "types": ["hindu_temple"]}
            ]
        },
        raw_overpass_response={
            "elements": [
                {"tags": {"shop": "general"}, "lat": 26.8470, "lon": 80.9465},
                {"tags": {"amenity": "school"}, "lat": 26.8460, "lon": 80.9450}
            ]
        },
        created_at=datetime.utcnow() - timedelta(days=7)
    )
    
    db.add(geo_features)
    
    print(f"   ✅ Created assessment: {assessment.store_name} (CSQS: {assessment.csqs})")
    return assessment


async def seed_demo_data():
    """Main seeding function"""
    print("🌱 Starting demo data seeding...")
    
    try:
        async with AsyncSessionLocal() as db:
            # Create demo user
            demo_user = await create_demo_user(db)
            
            # Create demo assessments
            assessment1 = await create_demo_assessment_1(db, demo_user)
            assessment2 = await create_demo_assessment_2(db, demo_user)
            assessment3 = await create_demo_assessment_3(db, demo_user)
            
            # Commit all changes
            await db.commit()
            
            print("\n✅ Demo data seeding completed successfully!")
            print("\n📊 Summary:")
            print(f"   👤 Demo user: demo@kiranalens.com (password: Demo@1234)")
            print(f"   🏪 {assessment1.store_name}: CSQS {assessment1.csqs} (Tier {assessment1.store_tier})")
            print(f"   🏪 {assessment2.store_name}: CSQS {assessment2.csqs} (Tier {assessment2.store_tier})")
            print(f"   🏪 {assessment3.store_name}: CSQS {assessment3.csqs} (Tier {assessment3.store_tier})")
            print("\n🚀 You can now run smoke tests with: python scripts/smoke_test.py")
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_demo_data())