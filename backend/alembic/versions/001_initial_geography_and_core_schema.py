"""Initial geography and core platform schema

Revision ID: 001_initial_geography
Revises: 
Create Date: 2026-11-18 20:58:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.core.database import Base
import app.models.entities

# revision identifiers, used by Alembic.
revision: str = '001_initial_geography'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely create all tables that do not exist yet (compatible with PostgreSQL and SQLite)
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    pass
