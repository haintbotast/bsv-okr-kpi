"""Initial database schema

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15 00:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables for KPI Management System."""

    # =========================================================================
    # Table 1: users
    # =========================================================================
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('role', sa.String(20), nullable=False, server_default='employee'),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('position', sa.String(100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Indexes for users table
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_role', 'users', ['role'])

    # =========================================================================
    # Table 2: kpi_templates
    # =========================================================================
    op.create_table(
        'kpi_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('role', sa.String(20), nullable=True),
        sa.Column('measurement_method', sa.String(50), nullable=True),
        sa.Column('target_type', sa.String(50), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for kpi_templates
    op.create_index('idx_templates_category', 'kpi_templates', ['category'])
    op.create_index('idx_templates_role', 'kpi_templates', ['role'])

    # =========================================================================
    # Table 3: kpis
    # =========================================================================
    op.create_table(
        'kpis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('quarter', sa.String(10), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('target_value', sa.String(100), nullable=True),
        sa.Column('current_value', sa.String(100), nullable=True),
        sa.Column('progress_percentage', sa.Float(), nullable=True),
        sa.Column('measurement_method', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['kpi_templates.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for kpis
    op.create_index('idx_kpis_user_id', 'kpis', ['user_id'])
    op.create_index('idx_kpis_year_quarter', 'kpis', ['year', 'quarter'])
    op.create_index('idx_kpis_status', 'kpis', ['status'])
    op.create_index('idx_kpis_user_year_quarter', 'kpis', ['user_id', 'year', 'quarter'])

    # Unique constraint to prevent duplicate KPIs
    op.create_index('idx_user_kpi_unique', 'kpis', ['user_id', 'year', 'quarter', 'title'], unique=True)

    # =========================================================================
    # Table 4: kpi_evidence
    # =========================================================================
    op.create_table(
        'kpi_evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kpi_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('file_type', sa.String(100), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['kpi_id'], ['kpis.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for kpi_evidence
    op.create_index('idx_evidence_kpi_id', 'kpi_evidence', ['kpi_id'])

    # =========================================================================
    # Table 5: kpi_comments
    # =========================================================================
    op.create_table(
        'kpi_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kpi_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['kpi_id'], ['kpis.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for kpi_comments
    op.create_index('idx_comments_kpi_id', 'kpi_comments', ['kpi_id'])

    # =========================================================================
    # Table 6: kpi_history
    # =========================================================================
    op.create_table(
        'kpi_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kpi_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['kpi_id'], ['kpis.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for kpi_history
    op.create_index('idx_history_kpi_id', 'kpi_history', ['kpi_id'])
    op.create_index('idx_history_created_at', 'kpi_history', ['created_at'])

    # =========================================================================
    # Table 7: notifications
    # =========================================================================
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('type', sa.String(20), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('link', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for notifications
    op.create_index('idx_notifications_user_id', 'notifications', ['user_id'])
    op.create_index('idx_notifications_is_read', 'notifications', ['is_read'])

    # =========================================================================
    # Table 8: system_settings
    # =========================================================================
    op.create_table(
        'system_settings',
        sa.Column('key', sa.String(100), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('key')
    )

    # =========================================================================
    # Insert default system settings
    # =========================================================================
    op.execute("""
        INSERT INTO system_settings (key, value, description) VALUES
        ('app_name', 'KPI Management System', 'Application name'),
        ('allow_registration', 'false', 'Allow public user registration'),
        ('max_file_size', '52428800', 'Maximum file upload size in bytes (50MB)'),
        ('notification_retention_days', '30', 'Days to keep read notifications'),
        ('backup_enabled', 'true', 'Enable automatic database backups'),
        ('backup_time', '02:00', 'Daily backup time (24-hour format)'),
        ('version', '1.0.0', 'Application version')
    """)


def downgrade() -> None:
    """Drop all tables in reverse order."""

    op.drop_table('system_settings')
    op.drop_index('idx_notifications_is_read', 'notifications')
    op.drop_index('idx_notifications_user_id', 'notifications')
    op.drop_table('notifications')
    op.drop_index('idx_history_created_at', 'kpi_history')
    op.drop_index('idx_history_kpi_id', 'kpi_history')
    op.drop_table('kpi_history')
    op.drop_index('idx_comments_kpi_id', 'kpi_comments')
    op.drop_table('kpi_comments')
    op.drop_index('idx_evidence_kpi_id', 'kpi_evidence')
    op.drop_table('kpi_evidence')
    op.drop_index('idx_user_kpi_unique', 'kpis')
    op.drop_index('idx_kpis_user_year_quarter', 'kpis')
    op.drop_index('idx_kpis_status', 'kpis')
    op.drop_index('idx_kpis_year_quarter', 'kpis')
    op.drop_index('idx_kpis_user_id', 'kpis')
    op.drop_table('kpis')
    op.drop_index('idx_templates_role', 'kpi_templates')
    op.drop_index('idx_templates_category', 'kpi_templates')
    op.drop_table('kpi_templates')
    op.drop_index('idx_users_role', 'users')
    op.drop_index('idx_users_username', 'users')
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')
