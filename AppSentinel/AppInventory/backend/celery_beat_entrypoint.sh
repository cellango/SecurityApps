#!/bin/sh

# Print environment variables for debugging
echo "Environment variables:"
echo "DATABASE_URL: $DATABASE_URL"
echo "SQLALCHEMY_DATABASE_URI: $SQLALCHEMY_DATABASE_URI"
echo "FLASK_APP: $FLASK_APP"
echo "FLASK_ENV: $FLASK_ENV"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is ready!"

# Wait for Celery worker
echo "Waiting for Celery worker..."
sleep 10  # Give worker time to initialize

# Start Celery beat
echo "Starting Celery beat..."
rm -f ./celerybeat.pid  # Remove any stale PID file
celery -A app.celery_app.celery_app beat --loglevel=info
