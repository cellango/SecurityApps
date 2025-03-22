#!/bin/bash
set -e

# Function to check if PostgreSQL is ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    while ! pg_isready -h postgres -p 5432 -q; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
}

# Wait for PostgreSQL to be ready
wait_for_postgres

# Initialize alembic if not already initialized
if [ ! -f /app/migrations/alembic.ini ]; then
    echo "Initializing alembic..."
    flask db init
fi

# Run database migrations
echo "Running database migrations..."
if ! flask db upgrade; then
    echo "Migration failed, but continuing since tables may already exist..."
fi

# If this is a fresh database, initialize with seed data
if [ "$FLASK_ENV" = "development" ]; then
    echo "Checking if database needs initialization..."
    TEAM_COUNT=$(psql -h postgres -U postgres -d security_score_card -t -c "SELECT COUNT(*) FROM teams;")
    if [ "$TEAM_COUNT" = "0" ]; then
        echo "Initializing database with seed data..."
        flask db-init
    fi
fi

# Start the application
exec flask run --host=0.0.0.0
