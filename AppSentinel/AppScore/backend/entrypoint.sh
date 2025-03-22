#!/bin/bash

set -e  # Exit on error

# Set working directory
cd /app

# Set PostgreSQL connection environment variables from environment or defaults
export DB_HOST=${DB_HOST:-postgres}
export DB_PORT=${DB_PORT:-5432}
export DB_NAME=${DB_NAME:-security_score_card}
export DB_USER=${DB_USER:-postgres}
export DB_PASSWORD=${DB_PASSWORD:-postgres}

# Set PGPASSWORD for psql commands
export PGPASSWORD=$DB_PASSWORD

# Wait for postgres
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is ready!"

# Initialize database if needed
echo "Checking database status..."
if ! PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Database does not exist, creating fresh database..."
    PGPASSWORD=$DB_PASSWORD createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME"
fi

# Initialize migrations if they don't exist
export FLASK_APP=app.py
if [ ! -d "migrations" ]; then
    echo "Initializing alembic migrations..."
    flask db init
    flask db migrate -m "create_initial_tables"
fi

# Apply any pending migrations
echo "Running database migrations..."
flask db upgrade

# Start the Flask application
echo "Starting Flask application..."
flask run --host=0.0.0.0
