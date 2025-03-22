#!/bin/bash

# Set backup directory
BACKUP_DIR="./data/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/${TIMESTAMP}"

# Create backup directory
mkdir -p ${BACKUP_PATH}

# Backup PostgreSQL database
echo "Backing up PostgreSQL database..."
docker-compose exec -T postgres pg_dump -U postgres perimeterai > ${BACKUP_PATH}/database.sql

# Backup Keycloak configuration
echo "Backing up Keycloak configuration..."
docker-compose exec -T keycloak /opt/keycloak/bin/kc.sh export --dir /tmp/export
docker cp $(docker-compose ps -q keycloak):/tmp/export ${BACKUP_PATH}/keycloak

# Backup Prometheus data
echo "Backing up Prometheus data..."
tar -czf ${BACKUP_PATH}/prometheus.tar.gz -C ./data/prometheus .

# Backup Grafana data
echo "Backing up Grafana data..."
tar -czf ${BACKUP_PATH}/grafana.tar.gz -C ./data/grafana .

# Create final archive
echo "Creating final backup archive..."
FINAL_BACKUP="${BACKUP_DIR}/perimeterai_backup_${TIMESTAMP}.tar.gz"
tar -czf ${FINAL_BACKUP} -C ${BACKUP_PATH} .

# Cleanup old backups (keep last 7 days)
echo "Cleaning up old backups..."
find ${BACKUP_DIR} -type f -name "perimeterai_backup_*.tar.gz" -mtime +7 -delete

# Remove temporary files
rm -rf ${BACKUP_PATH}

echo "Backup completed successfully!"
