"""Create objectives tables

Revision ID: 20251106_1400
Revises: e442962f40bf
Create Date: 2025-11-06 14:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20251106_1400"
down_revision: Union[str, None] = "e442962f40bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create objectives table
    op.create_table(
        "objectives",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),

        # Hierarchy
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("level", sa.String(length=20), nullable=False),

        # Ownership
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=True),

        # Time period
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("quarter", sa.String(length=10), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),

        # Progress
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("progress_percentage", sa.Float(), nullable=False, server_default="0.0"),

        # Metadata
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["parent_id"], ["objectives.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
    )

    # Create indexes for objectives table
    op.create_index("idx_objectives_parent", "objectives", ["parent_id"])
    op.create_index("idx_objectives_owner", "objectives", ["owner_id"])
    op.create_index("idx_objectives_year_quarter", "objectives", ["year", "quarter"])
    op.create_index("idx_objectives_level", "objectives", ["level"])
    op.create_index("idx_objectives_status", "objectives", ["status"])

    # Create objective_kpi_links table
    op.create_table(
        "objective_kpi_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("objective_id", sa.Integer(), nullable=False),
        sa.Column("kpi_id", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["objective_id"], ["objectives.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["kpi_id"], ["kpis.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("objective_id", "kpi_id", name="uq_objective_kpi"),
    )

    # Create indexes for objective_kpi_links table
    op.create_index("idx_objective_kpi_links_objective", "objective_kpi_links", ["objective_id"])
    op.create_index("idx_objective_kpi_links_kpi", "objective_kpi_links", ["kpi_id"])

    # Add objective_id to kpis table (nullable for backward compatibility)
    # SQLite requires batch mode for adding foreign keys
    with op.batch_alter_table("kpis", schema=None) as batch_op:
        batch_op.add_column(sa.Column("objective_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_kpis_objective", "objectives", ["objective_id"], ["id"], ondelete="SET NULL")
        batch_op.create_index("idx_kpis_objective", ["objective_id"])


def downgrade() -> None:
    # Remove objective_id from kpis table
    with op.batch_alter_table("kpis", schema=None) as batch_op:
        batch_op.drop_index("idx_kpis_objective")
        batch_op.drop_constraint("fk_kpis_objective", type_="foreignkey")
        batch_op.drop_column("objective_id")

    # Drop objective_kpi_links table
    op.drop_index("idx_objective_kpi_links_kpi", table_name="objective_kpi_links")
    op.drop_index("idx_objective_kpi_links_objective", table_name="objective_kpi_links")
    op.drop_table("objective_kpi_links")

    # Drop objectives table
    op.drop_index("idx_objectives_status", table_name="objectives")
    op.drop_index("idx_objectives_level", table_name="objectives")
    op.drop_index("idx_objectives_year_quarter", table_name="objectives")
    op.drop_index("idx_objectives_owner", table_name="objectives")
    op.drop_index("idx_objectives_parent", table_name="objectives")
    op.drop_table("objectives")
