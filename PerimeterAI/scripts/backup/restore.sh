#!/bin/bash

# Load environment variables
source .env

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Please provide backup file path"
    exit 1
fi

BACKUP_FILE=$1
TEMP_DIR="/tmp/perimeterai_restore"

# Create temporary directory
mkdir -p ${TEMP_DIR}

# Extract backup
echo "Extracting backup..."
tar -xzf ${BACKUP_FILE} -C ${TEMP_DIR}

# Stop services
echo "Stopping services..."
docker-compose down

# Restore PostgreSQL database
echo "Restoring PostgreSQL database..."
docker-compose up -d postgres
sleep 10  # Wait for PostgreSQL to start
cat ${TEMP_DIR}/database.sql | docker-compose exec -T postgres psql -U ${POSTGRES_USER} ${POSTGRES_DB}

# Restore Keycloak configuration
echo "Restoring Keycloak configuration..."
docker cp ${TEMP_DIR}/keycloak/. $(docker-compose ps -q keycloak):/tmp/import
docker-compose exec -T keycloak /opt/keycloak/bin/kc.sh import --dir /tmp/import

# Restore Prometheus data
echo "Restoring Prometheus data..."
rm -rf /data/prometheus/*
tar -xzf ${TEMP_DIR}/prometheus.tar.gz -C /data/prometheus

# Restore Grafana data
echo "Restoring Grafana data..."
rm -rf /data/grafana/*
tar -xzf ${TEMP_DIR}/grafana.tar.gz -C /data/grafana

# Start services
echo "Starting services..."
docker-compose up -d

# Cleanup
rm -rf ${TEMP_DIR}

echo "Restore completed successfully!"
