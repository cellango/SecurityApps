# PerimeterAI Keycloak Module

This module provides a standalone Keycloak authentication server for the PerimeterAI project.

## Features

- Standalone Keycloak server with PostgreSQL database
- Health checks for both services
- Persistent storage for PostgreSQL data
- Easy deployment using Make commands
- Configurable admin credentials

## Prerequisites

- Docker and Docker Compose
- Make

## Quick Start

1. Build the services:
```bash
make build
```

2. Start the services:
```bash
make up
```

Keycloak will be available at http://localhost:8081
Default admin credentials: admin/admin

## Available Commands

- `make build` - Build Keycloak service
- `make up` - Start Keycloak and PostgreSQL
- `make down` - Stop all services
- `make logs` - View Keycloak logs
- `make clean` - Clean up all resources including volumes
- `make restart` - Restart all services
- `make health` - Check Keycloak health status
- `make help` - Show help message

## Configuration

### Environment Variables

#### PostgreSQL
- `POSTGRES_DB`: Database name (default: keycloak)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: perimeter123)

#### Keycloak
- `KEYCLOAK_ADMIN`: Admin username (default: admin)
- `KEYCLOAK_ADMIN_PASSWORD`: Admin password (default: admin)
- `KC_HOSTNAME_URL`: Public URL (default: http://localhost:8081)
- `KC_HTTP_ENABLED`: HTTP enabled flag (default: true)

## Health Checks

The module includes health checks for both services:

- PostgreSQL: Checks database connectivity every 10s
- Keycloak: Checks server health every 30s

## Volumes

- `postgres_data`: Persistent storage for PostgreSQL data

## Networks

- `keycloak-network`: Isolated network for Keycloak services

## Troubleshooting

1. If services fail to start:
   ```bash
   make logs
   ```

2. To reset everything:
   ```bash
   make clean
   make up
   ```

3. To check service health:
   ```bash
   make health
   ```
