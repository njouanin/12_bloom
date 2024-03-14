"""create_dim_port

Revision ID: 4dda30a04da7
Revises: 6734d9afbba5
Create Date: 2024-03-10 15:15:31.848100

"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from bloom.config import settings
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "4dda30a04da7"
down_revision = "6734d9afbba5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dim_port",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True, index=True),
        sa.Column("port_name", sa.String, nullable=False),
        sa.Column("locode", sa.String),
        sa.Column("geometry", Geometry("GEOMETRY", srid=settings.srid)),
        sa.Column("latitude", sa.Double),
        sa.Column("longitude", sa.Double),
        sa.Column("country_iso3", sa.String),
        sa.Column("has_excursion", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=func.now()),
    )


def downgrade() -> None:
    op.drop_table("dim_port")
