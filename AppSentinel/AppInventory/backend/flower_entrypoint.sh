#!/bin/sh

# Print environment variables for debugging
echo "Environment variables:"
echo "CELERY_BROKER_URL: $CELERY_BROKER_URL"
echo "CELERY_RESULT_BACKEND: $CELERY_RESULT_BACKEND"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is ready!"

# Wait for Celery worker
echo "Waiting for Celery worker..."
sleep 10  # Give worker time to initialize

# Start Flower
echo "Starting Flower..."
celery -A app.celery_app.celery_app flower --port=5555 --address=0.0.0.0
