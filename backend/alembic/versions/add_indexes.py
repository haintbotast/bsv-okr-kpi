"""Add performance indexes

Revision ID: add_indexes
Revises: 001_initial
Create Date: 2025-01-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'add_indexes'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    """Add indexes for frequently queried columns."""
    # KPIs table indexes
    op.create_index('idx_kpis_user_year_quarter', 'kpis', ['user_id', 'year', 'quarter'])
    op.create_index('idx_kpis_status_year', 'kpis', ['status', 'year'])
    op.create_index('idx_kpis_created_at', 'kpis', ['created_at'])

    # Comments table indexes
    op.create_index('idx_kpi_comments_kpi_created', 'kpi_comments', ['kpi_id', 'created_at'])

    # Evidence table indexes
    op.create_index('idx_kpi_evidence_kpi_uploaded', 'kpi_evidence', ['kpi_id', 'uploaded_at'])

    # Notifications table indexes
    op.create_index('idx_notifications_user_read', 'notifications', ['user_id', 'is_read'])
    op.create_index('idx_notifications_created', 'notifications', ['created_at'])


def downgrade():
    """Remove indexes."""
    op.drop_index('idx_kpis_user_year_quarter', 'kpis')
    op.drop_index('idx_kpis_status_year', 'kpis')
    op.drop_index('idx_kpis_created_at', 'kpis')
    op.drop_index('idx_kpi_comments_kpi_created', 'kpi_comments')
    op.drop_index('idx_kpi_evidence_kpi_uploaded', 'kpi_evidence')
    op.drop_index('idx_notifications_user_read', 'notifications')
    op.drop_index('idx_notifications_created', 'notifications')
