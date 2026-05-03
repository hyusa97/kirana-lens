"""Create assessments, visual_features, and geo_features tables

Revision ID: 003
Revises: 002
Create Date: 2026-04-15 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enums explicitly first
    op.execute("CREATE TYPE assessmentstatus AS ENUM ('pending', 'processing', 'complete', 'error')")
    op.execute("CREATE TYPE inventoryvalueband AS ENUM ('low', 'medium', 'high', 'very_high')")
    op.execute("CREATE TYPE refillsignal AS ENUM ('partially_empty', 'normal', 'overfilled')")

    # Use create_type=False so SQLAlchemy doesn't try to emit CREATE TYPE again
    status_type = postgresql.ENUM('pending', 'processing', 'complete', 'error',
                                  name='assessmentstatus', create_type=False)
    ivb_type = postgresql.ENUM('low', 'medium', 'high', 'very_high',
                               name='inventoryvalueband', create_type=False)
    refill_type = postgresql.ENUM('partially_empty', 'normal', 'overfilled',
                                  name='refillsignal', create_type=False)

    # Create assessments table
    op.create_table('assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_name', sa.String(length=200), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('lat', sa.Numeric(precision=10, scale=7), nullable=False),
        sa.Column('lng', sa.Numeric(precision=10, scale=7), nullable=False),
        sa.Column('gps_accuracy_metres', sa.Float(), nullable=True),
        sa.Column('image_urls', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', status_type, nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('csqs', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('store_tier', sa.String(length=5), nullable=True),
        sa.Column('confidence_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('daily_sales_min', sa.Integer(), nullable=True),
        sa.Column('daily_sales_max', sa.Integer(), nullable=True),
        sa.Column('monthly_revenue_min', sa.Integer(), nullable=True),
        sa.Column('monthly_revenue_max', sa.Integer(), nullable=True),
        sa.Column('monthly_income_min', sa.Integer(), nullable=True),
        sa.Column('monthly_income_max', sa.Integer(), nullable=True),
        sa.Column('risk_flags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('recommendation', sa.String(length=30), nullable=True),
        sa.Column('signal_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('pdf_report_url', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessments_id'), 'assessments', ['id'], unique=False)
    op.create_index(op.f('ix_assessments_status'), 'assessments', ['status'], unique=False)

    # Create visual_features table
    op.create_table('visual_features',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('shelf_density_index', sa.Integer(), nullable=False),
        sa.Column('sku_diversity_score', sa.Integer(), nullable=False),
        sa.Column('store_organization_score', sa.Integer(), nullable=False),
        sa.Column('counter_activity_proxy', sa.Integer(), nullable=False),
        sa.Column('exterior_quality_score', sa.Integer(), nullable=False),
        sa.Column('inventory_value_band', ivb_type, nullable=False),
        sa.Column('refill_signal', refill_type, nullable=False),
        sa.Column('image_quality_warnings', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('raw_claude_response', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('assessment_id')
    )
    op.create_index(op.f('ix_visual_features_id'), 'visual_features', ['id'], unique=False)

    # Create geo_features table
    op.create_table('geo_features',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('road_type_score', sa.Integer(), nullable=False),
        sa.Column('catchment_density_score', sa.Integer(), nullable=False),
        sa.Column('footfall_proxy_index', sa.Integer(), nullable=False),
        sa.Column('competition_density_score', sa.Integer(), nullable=False),
        sa.Column('neighbourhood_quality_score', sa.Integer(), nullable=False),
        sa.Column('competitor_count', sa.Integer(), nullable=False),
        sa.Column('poi_count', sa.Integer(), nullable=False),
        sa.Column('raw_places_response', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_overpass_response', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('assessment_id')
    )
    op.create_index(op.f('ix_geo_features_id'), 'geo_features', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_geo_features_id'), table_name='geo_features')
    op.drop_table('geo_features')
    op.drop_index(op.f('ix_visual_features_id'), table_name='visual_features')
    op.drop_table('visual_features')
    op.drop_index(op.f('ix_assessments_status'), table_name='assessments')
    op.drop_index(op.f('ix_assessments_id'), table_name='assessments')
    op.drop_table('assessments')
    op.execute('DROP TYPE IF EXISTS refillsignal')
    op.execute('DROP TYPE IF EXISTS inventoryvalueband')
    op.execute('DROP TYPE IF EXISTS assessmentstatus')
