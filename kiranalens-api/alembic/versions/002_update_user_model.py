"""Placeholder - user model already correct in 001

Revision ID: 002
Revises: 001
Create Date: 2026-04-15 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # No-op: users table is fully created in 001 with the correct schema
    pass


def downgrade() -> None:
    pass
