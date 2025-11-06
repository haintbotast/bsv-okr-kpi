"""add notification preferences to users

Revision ID: 20251105_1630
Revises: 20251105_0001
Create Date: 2025-11-05 16:30:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251105_1630'
down_revision = '20251105_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add notification preference columns to users table."""
    # Add notification preference columns
    op.add_column('users', sa.Column('email_notifications', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('notify_kpi_submitted', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('notify_kpi_approved', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('notify_kpi_rejected', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('notify_comment_mention', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('users', sa.Column('weekly_digest', sa.Boolean(), nullable=True, server_default='1'))


def downgrade() -> None:
    """Remove notification preference columns from users table."""
    op.drop_column('users', 'weekly_digest')
    op.drop_column('users', 'notify_comment_mention')
    op.drop_column('users', 'notify_kpi_rejected')
    op.drop_column('users', 'notify_kpi_approved')
    op.drop_column('users', 'notify_kpi_submitted')
    op.drop_column('users', 'email_notifications')
