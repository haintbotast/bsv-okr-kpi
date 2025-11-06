"""add password reset fields

Revision ID: 20251106_0001
Revises: 20251105_1630
Create Date: 2025-11-06

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251106_0001'
down_revision = '20251105_1630'
branch_labels = None
depends_on = None


def upgrade():
    """Add password reset fields to users table."""
    # Add password reset token field
    op.add_column('users', sa.Column('reset_token', sa.String(length=500), nullable=True))

    # Add reset token expiration field
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True))

    # Add password history field (JSON stored as TEXT)
    op.add_column('users', sa.Column('password_history', sa.Text(), nullable=True))


def downgrade():
    """Remove password reset fields from users table."""
    op.drop_column('users', 'password_history')
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token')
