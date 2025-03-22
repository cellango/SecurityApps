# PerimeterAI Scripts

This directory contains utility scripts for managing the PerimeterAI project.

## Available Scripts

### cleanup.sh

A utility script for cleaning up Docker resources associated with PerimeterAI services.

#### Features

- **Container Cleanup**: Removes all PerimeterAI containers
- **Network Cleanup**: Removes PerimeterAI Docker networks
- **Simple Execution**: Easy to use with clear feedback
- **Color-coded Output**: Visual feedback for different operations

#### Usage

```bash
# Make the script executable (first time only)
chmod +x scripts/cleanup.sh

# Run the cleanup script
./scripts/cleanup.sh
```

#### What it Does

1. **Container Cleanup**
   - Stops all running PerimeterAI containers
   - Removes containers with "perimeterai" prefix

2. **Network Cleanup**
   - Removes the PerimeterAI Docker network

#### Output

The script provides color-coded output:
- 🟢 Green: Success messages
- 🔴 Red: Operation messages and steps

#### Example Output
```
[RED] Stopping all PerimeterAI containers...
[RED] Removing all PerimeterAI containers...
[RED] Removing all PerimeterAI networks...
[GREEN] Cleanup complete! You can now start the services with 'docker compose up -d'
```

### check_health.sh

A script for monitoring the health status of PerimeterAI services.

#### Features

- **Health Monitoring**: Checks health endpoints of all services
- **Color-coded Status**: Visual feedback for service health
- **Regular Updates**: Continuous monitoring of service status

#### Usage

```bash
# Make the script executable (first time only)
chmod +x scripts/check_health.sh

# Run the health check script
./scripts/check_health.sh
```

#### What it Checks

Monitors health status for:
- Signature Service
- Keycloak
- Keyboard Dynamics Backend
- Keyboard Dynamics Frontend
- Redis
- PostgreSQL
- Prometheus
- Grafana

#### Integration

Both scripts can be integrated with your build system or CI/CD pipeline for automated cleanup and health monitoring.
