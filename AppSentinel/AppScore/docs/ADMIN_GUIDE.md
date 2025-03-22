# Security Score Card - Administrator Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Environment Configuration](#environment-configuration)
4. [Logging System](#logging-system)
5. [Database Management](#database-management)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM
- 10GB disk space
- PostgreSQL 13+

### Recommended Requirements
- 4GB RAM
- 20GB disk space
- SSD storage for database

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd security-score-card
```

2. Create environment files:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

## Environment Configuration

### Available Environments

The application supports three environments:

1. **Development** (default)
   ```bash
   FLASK_ENV=development
   LOG_LEVEL=DEBUG
   ```
   - Full debug logging
   - SQL query logging
   - Detailed error messages
   - Hot reload enabled

2. **Production**
   ```bash
   FLASK_ENV=production
   LOG_LEVEL=INFO
   ```
   - Limited logging
   - No SQL query logging
   - Generic error messages
   - Performance optimizations

3. **Testing**
   ```bash
   FLASK_ENV=testing
   LOG_LEVEL=DEBUG
   ```
   - Full debug logging
   - Separate test database
   - Test-specific configurations

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| FLASK_ENV | Application environment | development | Yes |
| LOG_LEVEL | Logging verbosity | DEBUG | Yes |
| DATABASE_URL | PostgreSQL connection URL | postgresql://postgres:postgres@postgres:5432/security_score_card | Yes |
| SECRET_KEY | Flask secret key | your-secret-key | Yes |
| JWT_SECRET_KEY | JWT encryption key | your-jwt-secret-key | Yes |
| JWT_ACCESS_TOKEN_EXPIRES | JWT token expiry (seconds) | 3600 | No |
| JWT_REFRESH_TOKEN_EXPIRES | Refresh token expiry (seconds) | 2592000 | No |

## Logging System

### Log Levels

The application uses Python's standard logging levels:

1. **DEBUG** (10): Detailed information for debugging
   - Function entry/exit
   - SQL queries
   - Request/response details
   - Variable values

2. **INFO** (20): General operational information
   - Application startup/shutdown
   - User actions
   - Successful operations
   - Configuration changes

3. **WARNING** (30): Potential issues that don't affect operation
   - Deprecated feature usage
   - Resource usage warnings
   - Non-critical errors

4. **ERROR** (40): Serious issues that affect operation
   - API errors
   - Database connection issues
   - Authentication failures
   - Unhandled exceptions

5. **CRITICAL** (50): System-level failures
   - Application crashes
   - Database corruption
   - Security breaches

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Example:
```
2024-12-28 07:30:05,123 - security_score_card - INFO - Application started in development mode
2024-12-28 07:30:05,124 - security_score_card - DEBUG - Connecting to database: postgresql://postgres:xxxxx@postgres:5432/security_score_card
```

### Log Configuration

1. **Development Logging**
   ```yaml
   environment:
     - FLASK_ENV=development
     - LOG_LEVEL=DEBUG
   ```
   - All log levels enabled
   - Function tracing
   - SQL query logging
   - Request/response logging

2. **Production Logging**
   ```yaml
   environment:
     - FLASK_ENV=production
     - LOG_LEVEL=INFO
   ```
   - INFO and above only
   - No SQL query logging
   - Limited request logging
   - Error tracking enabled

3. **Testing Logging**
   ```yaml
   environment:
     - FLASK_ENV=testing
     - LOG_LEVEL=DEBUG
   ```
   - All log levels enabled
   - Test execution logging
   - Assertion results
   - Coverage information

### Log Management

1. **Log Rotation**
   - Logs are rotated daily
   - Maximum 30 days retention
   - Compressed after rotation

2. **Log Access**
   - Development: Console output
   - Production: File-based logging
   - Container logs accessible via `docker logs`

3. **Log Monitoring**
   ```bash
   # View real-time logs
   docker-compose logs -f backend

   # View specific service logs
   docker-compose logs backend | grep ERROR

   # View logs since specific time
   docker-compose logs --since 30m backend
   ```

## Database Management

### Database Configuration

1. **Development Database**
   ```yaml
   environment:
     - POSTGRES_DB=security_score_card
     - POSTGRES_USER=postgres
     - POSTGRES_PASSWORD=postgres
   ```

2. **Production Database**
   ```yaml
   environment:
     - POSTGRES_DB=security_score_card_prod
     - POSTGRES_USER=${DB_USER}
     - POSTGRES_PASSWORD=${DB_PASSWORD}
   ```

### Database Maintenance

1. **Backup**
   ```bash
   # Create backup
   docker-compose exec postgres pg_dump -U postgres security_score_card > backup.sql

   # Restore backup
   docker-compose exec -T postgres psql -U postgres security_score_card < backup.sql
   ```

2. **Migration**
   ```bash
   # Run migrations
   docker-compose exec backend flask db upgrade

   # Create new migration
   docker-compose exec backend flask db migrate -m "description"
   ```

## Security Configuration

### JWT Configuration

```yaml
environment:
  - JWT_SECRET_KEY=your-secure-key-here
  - JWT_ACCESS_TOKEN_EXPIRES=3600
  - JWT_REFRESH_TOKEN_EXPIRES=2592000
```

### SSL/TLS Configuration

For production, configure SSL/TLS in your reverse proxy:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

## Monitoring and Maintenance

### Health Checks

1. **API Health Check**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Database Health Check**
   ```bash
   docker-compose exec postgres pg_isready -U postgres
   ```

### Performance Monitoring

1. **Container Stats**
   ```bash
   docker stats security-score-card_backend_1
   ```

2. **Application Metrics**
   - Request latency
   - Database query time
   - Memory usage
   - CPU usage

### Maintenance Tasks

1. **Clear Cache**
   ```bash
   docker-compose exec backend flask cache clear
   ```

2. **Update Dependencies**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL logs
   - Verify connection string
   - Check network connectivity

2. **Authentication Failures**
   - Verify JWT configuration
   - Check token expiration
   - Validate user credentials

3. **Performance Issues**
   - Check resource usage
   - Review database indexes
   - Monitor query performance

### Debug Mode

To enable debug mode:

```bash
FLASK_ENV=development LOG_LEVEL=DEBUG docker-compose up
```

This will:
- Enable detailed logging
- Show SQL queries
- Display stack traces
- Enable hot reload

### Log Analysis

1. **Error Pattern Analysis**
   ```bash
   docker-compose logs backend | grep ERROR | sort | uniq -c
   ```

2. **Performance Analysis**
   ```bash
   docker-compose logs backend | grep "Query took" | sort -k6 -n
   ```

3. **Security Analysis**
   ```bash
   docker-compose logs backend | grep "Authentication failed"
   ```

### Support Information

For additional support:
1. Check the [GitHub Issues](https://github.com/your-repo/issues)
2. Review the [Documentation](https://your-docs-url)
3. Contact the development team
