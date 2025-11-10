"""add is_featured to objectives

Revision ID: 20251110_0820
Revises: 20251106_1400
Create Date: 2025-11-10 08:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20251110_0820"
down_revision: Union[str, None] = "20251106_1400"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_featured column to objectives table
    with op.batch_alter_table('objectives', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_featured', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove is_featured column from objectives table
    with op.batch_alter_table('objectives', schema=None) as batch_op:
        batch_op.drop_column('is_featured')
