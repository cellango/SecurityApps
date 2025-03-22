FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY app app/
COPY scripts scripts/
COPY migrations migrations/
COPY config.py .
COPY wsgi.py .

# Make the scripts directory a module
RUN touch scripts/__init__.py

# Copy and make the entrypoint scripts executable
COPY entrypoint.sh celery_entrypoint.sh celery_beat_entrypoint.sh flower_entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh /app/celery_entrypoint.sh /app/celery_beat_entrypoint.sh /app/flower_entrypoint.sh

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@appinventory-db:5432/appinventory
ENV DATABASE_URL=postgresql://postgres:postgres@appinventory-db:5432/appinventory

EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
