# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app app/
COPY scripts scripts/
COPY migrations migrations/
COPY config.py .
COPY wsgi.py .

# Make the scripts directory a module
RUN touch scripts/__init__.py

# Copy and set up entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@postgres:5432/appscore
ENV DATABASE_URL=postgresql://postgres:postgres@postgres:5432/appscore

EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]
