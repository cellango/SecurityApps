#!/bin/sh

# Print environment variables for debugging
echo "Environment variables:"
echo "DATABASE_URL: $DATABASE_URL"
echo "SQLALCHEMY_DATABASE_URI: $SQLALCHEMY_DATABASE_URI"
echo "FLASK_APP: $FLASK_APP"
echo "FLASK_ENV: $FLASK_ENV"

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z appinventory-db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is ready!"

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.celery_app.celery_app worker --loglevel=info
