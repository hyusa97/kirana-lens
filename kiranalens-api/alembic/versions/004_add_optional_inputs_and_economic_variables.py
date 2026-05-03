"""Add optional inputs for economic sales estimation

Revision ID: 004
Revises: 003
Create Date: 2026-05-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("assessments", sa.Column("monthly_rent", sa.Float(), nullable=True))
    op.add_column("assessments", sa.Column("years_in_operation", sa.Integer(), nullable=True))
    op.add_column("assessments", sa.Column("shop_size", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("assessments", "shop_size")
    op.drop_column("assessments", "years_in_operation")
    op.drop_column("assessments", "monthly_rent")
