"""Initial database setup

Revision ID: 01_initial_setup
Revises: 
Create Date: 2025-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = '01_initial_setup'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create departments table
    op.create_table('departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create teams table
    op.create_table('teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create applications table
    op.create_table('applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('application_type', sa.String(length=50), nullable=False, server_default='web'),
        sa.Column('owner_id', sa.String(50), nullable=True),
        sa.Column('owner_email', sa.String(100), nullable=True),
        sa.Column('department_name', sa.String(100), nullable=True),
        sa.Column('team_name', sa.String(100), nullable=True),
        sa.Column('team_id', sa.Integer(), nullable=True),
        sa.Column('test_score', sa.Float(), nullable=True),
        sa.Column('test_score_date', sa.DateTime(), nullable=True),
        sa.Column('last_security_review', sa.DateTime(), nullable=True),
        sa.Column('next_security_review', sa.DateTime(), nullable=True),
        sa.Column('deployment_date', sa.DateTime(), nullable=True),
        sa.Column('last_update_date', sa.DateTime(), nullable=True),
        sa.Column('vendor_name', sa.String(100), nullable=True),
        sa.Column('vendor_contact', sa.String(100), nullable=True),
        sa.Column('contract_expiration', sa.DateTime(), nullable=True),
        sa.Column('data_classification', sa.String(50), nullable=True),
        sa.Column('authentication_method', sa.String(50), nullable=True),
        sa.Column('requires_2fa', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create user_teams table for many-to-many relationship
    op.create_table('user_teams',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'team_id')
    )

    # Create application_types table
    op.create_table(
        'application_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create application_states table
    op.create_table(
        'application_states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create control_families table
    op.create_table(
        'control_families',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create control_statuses table
    op.create_table(
        'control_statuses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create security_controls table
    op.create_table(
        'security_controls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['family_id'], ['control_families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create application_controls table
    op.create_table(
        'application_controls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('control_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.ForeignKeyConstraint(['control_id'], ['security_controls.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['control_statuses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create export_filter_presets table
    op.create_table(
        'export_filter_presets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filters', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Populate reference tables
    op.execute("""
        INSERT INTO application_types (name) VALUES
        ('web'),
        ('mobile'),
        ('desktop'),
        ('api'),
        ('service');
    """)

    op.execute("""
        INSERT INTO application_states (name) VALUES
        ('development'),
        ('testing'),
        ('staging'),
        ('production'),
        ('retired');
    """)

    op.execute("""
        INSERT INTO control_families (name) VALUES
        ('Access Control'),
        ('Authentication'),
        ('Data Protection'),
        ('Logging'),
        ('Network Security');
    """)

    op.execute("""
        INSERT INTO control_statuses (name) VALUES
        ('not_started'),
        ('in_progress'),
        ('implemented'),
        ('not_applicable'),
        ('failed');
    """)

    # Create admin user
    admin_password_hash = generate_password_hash('admin123', method='pbkdf2:sha256', salt_length=16)
    op.execute(f"""
        INSERT INTO users (username, email, password_hash, role, first_name, last_name, created_at, updated_at)
        VALUES ('admin', 'admin@example.com', '{admin_password_hash}', 'admin', 'System', 'Administrator', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """)


def downgrade():
    op.drop_table('export_filter_presets')
    op.drop_table('application_controls')
    op.drop_table('security_controls')
    op.drop_table('application_states')
    op.drop_table('application_types')
    op.drop_table('control_statuses')
    op.drop_table('control_families')
    op.drop_table('applications')
    op.drop_table('user_teams')
    op.drop_table('teams')
    op.drop_table('departments')
    op.drop_table('users')
