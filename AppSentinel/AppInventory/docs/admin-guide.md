# Administrator Guide

## System Overview
AppSentinel is a web-based application for managing security controls. This guide covers installation, configuration, maintenance, and troubleshooting for system administrators.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Database Management](#database-management)
4. [User Management](#user-management)
5. [Maintenance](#maintenance)
6. [Monitoring](#monitoring)
7. [Backup and Recovery](#backup-and-recovery)
8. [Troubleshooting](#troubleshooting)

## Installation

### System Requirements
- CPU: 2+ cores
- RAM: 4GB minimum
- Storage: 20GB minimum
- OS: Linux (Ubuntu 20.04 LTS recommended)

### Software Requirements
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Redis (optional, for caching)

### Installation Steps

1. **System Packages**
```bash
sudo apt update
sudo apt install python3.8 python3.8-venv nodejs npm postgresql-13
```

2. **Clone Repository**
```bash
git clone https://github.com/your-org/appsentinel.git
cd appsentinel
```

3. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Frontend Setup**
```bash
cd frontend
npm install
```

5. **Database Setup**
```bash
sudo -u postgres createdb appsentinel
sudo -u postgres createuser appsentinel
flask db upgrade
```

## Configuration

### Environment Variables
Create `.env` file in backend directory:
```ini
FLASK_APP=app
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@localhost/appsentinel
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379/0  # Optional
```

### Application Configuration
Edit `config.py`:
```python
class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20
    }
```

### Web Server Configuration
Example Nginx configuration:
```nginx
server {
    listen 80;
    server_name appsentinel.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Database Management

### Backup
```bash
# Daily backup
pg_dump -U postgres appsentinel > backup_$(date +%Y%m%d).sql

# With compression
pg_dump -U postgres appsentinel | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore
```bash
psql -U postgres appsentinel < backup.sql
```

### Maintenance
```bash
# Vacuum analyze
psql -U postgres -d appsentinel -c "VACUUM ANALYZE;"

# Reindex
psql -U postgres -d appsentinel -c "REINDEX DATABASE appsentinel;"
```

## User Management

### Adding Users
```sql
INSERT INTO users (username, email, role)
VALUES ('newuser', 'user@example.com', 'user');
```

### Roles and Permissions
- Admin: Full system access
- Manager: Department/team management
- User: Basic access

### Password Reset
```bash
flask users reset-password username
```

## Maintenance

### Routine Tasks
1. **Daily**
   - Check error logs
   - Monitor disk space
   - Verify backups

2. **Weekly**
   - Review user activity
   - Check system updates
   - Run database maintenance

3. **Monthly**
   - Review security patches
   - Update documentation
   - Test backup restoration

### Log Rotation
Configure logrotate:
```
/var/log/appsentinel/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 appsentinel appsentinel
}
```

## Monitoring

### System Metrics
Monitor using Prometheus and Grafana:
- CPU usage
- Memory usage
- Disk space
- Database connections

### Application Metrics
- Request latency
- Error rates
- Active users
- Export frequency

### Alerts
Configure alerts for:
- High CPU/memory usage
- Low disk space
- Database connection issues
- Application errors

## Backup and Recovery

### Backup Strategy
1. **Database**
   - Daily full backups
   - Continuous WAL archiving
   - Off-site backup storage

2. **Application Files**
   - Config files
   - Custom scripts
   - User uploads

3. **Logs**
   - Application logs
   - Access logs
   - Error logs

### Recovery Procedures
1. **Database Recovery**
```bash
# Stop application
systemctl stop appsentinel

# Restore database
psql -U postgres appsentinel < backup.sql

# Start application
systemctl start appsentinel
```

2. **Application Recovery**
```bash
# Deploy from backup
tar xzf appsentinel-backup.tar.gz
cd appsentinel
./deploy.sh
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
systemctl status postgresql

# Check connection
psql -U postgres -d appsentinel -c "\l"
```

#### Application Errors
1. Check logs:
```bash
tail -f /var/log/appsentinel/app.log
```

2. Verify processes:
```bash
ps aux | grep appsentinel
```

#### Performance Issues
1. Check system resources:
```bash
top
df -h
free -m
```

2. Database queries:
```sql
SELECT * FROM pg_stat_activity;
```

### Support
For additional support:
- Email: admin-support@appsentinel.com
- Documentation: https://docs.appsentinel.com
- Issue Tracker: https://github.com/your-org/appsentinel/issues
