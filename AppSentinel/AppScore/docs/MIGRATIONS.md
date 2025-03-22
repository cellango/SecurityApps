# Database Migrations Guide

## Overview

This project uses Alembic for database migrations. Alembic is a lightweight database migration tool for SQLAlchemy.

## Setup

The migration configuration is already set up in:
- `backend/alembic.ini`: Main configuration file
- `backend/migrations/env.py`: Migration environment
- `backend/migrations/versions/`: Directory containing migration scripts

## Common Commands

### Initialize Database
```bash
cd backend
alembic upgrade head
```

### Create New Migration
```bash
# Generate a new migration script
alembic revision -m "description_of_changes"

# Generate a new migration script with autogenerate
alembic revision --autogenerate -m "description_of_changes"
```

### View Migration Status
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --indicate-current
```

### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply next migration
alembic upgrade +1

# Rollback last migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

## Migration Guidelines

### Writing Migrations

1. Always include both upgrade() and downgrade() operations
2. Make migrations atomic (one conceptual change per migration)
3. Don't modify existing migrations after they're committed
4. Test both upgrade and downgrade paths

Example:
```python
def upgrade():
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('new_table')
```

### Best Practices

1. **Naming Conventions**
   - Use descriptive names for migration files
   - Include the purpose of the change
   - Example: "add_user_role_column.py"

2. **Testing**
   - Test migrations on a copy of production data
   - Verify both upgrade and downgrade paths
   - Check data integrity after migration

3. **Data Migrations**
   - Keep data migrations separate from schema migrations
   - Handle NULL values and data type conversions carefully
   - Include data validation steps

4. **Performance**
   - Consider table size when adding columns or constraints
   - Use batch operations for large data migrations
   - Plan for migration duration in deployment

## Deployment

### Production Deployment Steps

1. **Backup Database**
```bash
pg_dump -U postgres security_score_card > backup.sql
```

2. **Apply Migrations**
```bash
alembic upgrade head
```

3. **Verify Migration**
```bash
alembic current
```

### Rollback Plan

1. **Revert Migration**
```bash
alembic downgrade -1
```

2. **Restore Backup** (if needed)
```bash
psql -U postgres security_score_card < backup.sql
```

## Troubleshooting

### Common Issues

1. **Migration Not Found**
   - Check if migration file is in versions directory
   - Verify migration is in alembic_version table

2. **Dependency Errors**
   - Ensure all required models are imported in env.py
   - Check for circular dependencies

3. **Failed Migrations**
   - Check database connection
   - Verify permissions
   - Review migration logs

### Recovery Steps

1. Manual fix in database if needed:
```sql
-- Reset alembic version
DELETE FROM alembic_version;
INSERT INTO alembic_version (version_num) VALUES ('desired_version');
```

2. Skip problematic migration:
```bash
alembic stamp head  # Mark as completed without running
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
