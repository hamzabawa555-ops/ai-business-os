"""Alembic Initial Migration"""

from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Create initial tables"""
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('company_name', sa.String(255), nullable=True),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table(
        'workflows',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('trigger_type', sa.String(50), nullable=False),
        sa.Column('trigger_config', sa.JSON(), nullable=False),
        sa.Column('steps', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_workflows_user_id', 'workflows', ['user_id'])

    op.create_table(
        'workflow_executions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('workflow_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('logs', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_workflow_executions_workflow_id', 'workflow_executions', ['workflow_id'])
    op.create_index('ix_workflow_executions_user_id', 'workflow_executions', ['user_id'])

def downgrade() -> None:
    """Drop tables"""
    op.drop_table('workflow_executions')
    op.drop_table('workflows')
    op.drop_table('users')
