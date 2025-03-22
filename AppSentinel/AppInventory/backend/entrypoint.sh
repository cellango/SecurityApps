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

# Run migrations
echo "Running database migrations..."
flask db upgrade

# Start the application
echo "Starting the application..."
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --debug
