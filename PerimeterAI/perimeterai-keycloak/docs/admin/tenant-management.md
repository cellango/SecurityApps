# Tenant Management Guide

This guide explains how to manage tenant information in the PerimeterAI Keycloak system. As an administrator, you'll learn how to create, update, and manage tenant configurations.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Accessing the Admin Console](#accessing-the-admin-console)
3. [Creating a New Tenant](#creating-a-new-tenant)
4. [Updating Tenant Information](#updating-tenant-information)
5. [Managing Tenant Users](#managing-tenant-users)
6. [Tenant Configuration Reference](#tenant-configuration-reference)
7. [Example Configurations and Scripts](#example-configurations-and-scripts)
8. [Best Practices](#best-practices)
9. [Error Handling](#error-handling)
10. [Troubleshooting](#troubleshooting)
11. [Support and Maintenance](#support-and-maintenance)
12. [Monitoring Configuration](#monitoring-configuration)

## Prerequisites

Before managing tenants, ensure you have:
- Administrator access to the Keycloak admin console
- Understanding of your organization's tenant structure
- Required tenant information (domain, contact details, etc.)

## Accessing the Admin Console

### URL Access

The Keycloak admin console can be accessed at:
- Production: `https://keycloak.perimeterai.com/auth/admin`
- Development: `https://keycloak.dev.perimeterai.com/auth/admin`
- Local: `http://localhost:8080/auth/admin`

### Login Steps

1. Navigate to the appropriate admin console URL based on your environment
2. Log in with your administrator credentials
3. Select the "PerimeterAI" realm from the realm dropdown in the top-left corner
4. You should now see the PerimeterAI tenant management interface

### Access Troubleshooting

If you cannot access the admin console:
1. Verify your network connection to the Keycloak server
2. Ensure your administrator account is properly configured
3. Check if your IP is allowlisted if access restrictions are in place
4. Clear browser cache and cookies if you experience login issues

### Security Notes

- Always use HTTPS for production and development environments
- Never share your admin credentials
- Use 2FA if configured
- Log out when you're done to prevent unauthorized access

## Creating a New Tenant

To create a new tenant:

1. Navigate to "Clients" in the left sidebar
2. Click "Create Client"
3. Fill in the following information:
   - Client ID: `tenant-<tenant-name>`
   - Client Protocol: "openid-connect"
   - Root URL: The tenant's primary domain
4. Click "Save"
5. Configure the following settings:
   ```
   Access Type: confidential
   Valid Redirect URIs: [tenant's allowed redirect URIs]
   Web Origins: [tenant's allowed origins]
   ```
6. Under "Credentials" tab, copy the client secret for tenant configuration

### Required Tenant Attributes

Configure these custom attributes under the "Attributes" tab:
- `tenant_id`: Unique identifier for the tenant
- `tenant_name`: Display name of the tenant
- `tenant_domain`: Primary domain of the tenant
- `tenant_plan`: Subscription plan level
- `tenant_status`: Active/Inactive status

## Updating Tenant Information

To update tenant information:

1. Navigate to "Clients"
2. Find and click on the tenant's client ID
3. Make necessary changes in the following tabs:
   - Settings: Basic configuration
   - Credentials: Client secret management
   - Roles: Role management
   - Attributes: Custom tenant attributes

### Updating Tenant Status

To change a tenant's status:
1. Navigate to the tenant's client settings
2. Go to "Attributes" tab
3. Update the `tenant_status` attribute
4. Click "Save"

## Managing Tenant Users

### Adding Users to a Tenant

1. Navigate to "Users"
2. Click "Add User"
3. Fill in user details
4. Under "Groups", assign the user to the appropriate tenant group
5. Set required attributes:
   - `tenant_id`: Match with tenant's ID
   - `tenant_role`: User's role within tenant

### User Roles and Permissions

Configure these standard roles for tenant users:
- `tenant-admin`: Full tenant administration rights
- `tenant-user`: Basic tenant access
- `tenant-viewer`: Read-only access

## Tenant Configuration Reference

### Required Attributes
| Attribute | Description | Example |
|-----------|-------------|---------|
| tenant_id | Unique identifier | tenant-123 |
| tenant_name | Display name | Acme Corp |
| tenant_domain | Primary domain | acme.com |
| tenant_plan | Subscription tier | standard |
| tenant_status | Current status | active |

### Optional Attributes
| Attribute | Description | Example |
|-----------|-------------|---------|
| tenant_contact | Primary contact | admin@acme.com |
| tenant_created | Creation date | 2024-12-25 |
| tenant_features | Enabled features | ["feature1","feature2"] |

## Example Configurations and Scripts

We provide several example configurations and scripts to help you manage tenants effectively. These can be found in the `examples` directory.

### 1. Sample Tenant Configuration

The `tenant-config.json` file provides a complete example of tenant configuration including:
- Basic client settings
- Custom attributes
- Role definitions

Example usage:
```bash
# View the sample configuration
cat examples/tenant-config.json

# Use it as a template
cp examples/tenant-config.json my-tenant-config.json
```

### 2. Tenant Creation Script

The `create-tenant.sh` script automates the process of creating a new tenant:
- Creates client in Keycloak
- Sets up default roles
- Configures client secret
- Sets initial attributes

Usage:
```bash
# Make the script executable
chmod +x create-tenant.sh

# Create a new tenant
./create-tenant.sh "Acme Corp" "acme.example.com" "enterprise"
```

### 3. Tenant Update Script

The `update-tenant.sh` script helps you update tenant attributes:
- Updates single attribute at a time
- Preserves other configurations
- Validates input

Usage:
```bash
# Make the script executable
chmod +x update-tenant.sh

# Update tenant status
./update-tenant.sh tenant-acme tenant_status inactive

# Update tenant plan
./update-tenant.sh tenant-acme tenant_plan premium
```

### Script Configuration

Before using the scripts, update the configuration variables in each script:
```bash
KEYCLOAK_URL="https://your-keycloak-url/auth"
REALM="your-realm"
ADMIN_USERNAME="your-admin"
ADMIN_PASSWORD="your-password"
```

### Best Practices for Using Scripts

1. Always test scripts in a non-production environment first
2. Keep the configuration files secure and never commit sensitive data
3. Regularly update the scripts to match your Keycloak version
4. Add error handling for your specific use cases
5. Consider adding logging for audit purposes

## Best Practices

1. Use consistent naming conventions for tenant IDs
2. Regularly audit tenant configurations
3. Document custom tenant requirements
4. Implement proper access controls
5. Monitor tenant resource usage

## Error Handling

The `error-handling.sh` script provides comprehensive error handling functions that can be incorporated into your tenant management scripts. Here's how to use them effectively:

### 1. Logging System

The script includes a flexible logging system with different levels:
```bash
LOG_ERROR=0  # Critical errors
LOG_WARN=1   # Warnings
LOG_INFO=2   # Information
LOG_DEBUG=3  # Debug information

# Example usage
log ${LOG_ERROR} "Failed to create tenant: Invalid input"
log ${LOG_INFO} "Successfully updated tenant configuration"
```

### 2. Input Validation

Always validate input before processing:

```bash
# Validate tenant ID
if ! validate_tenant_id "${tenant_id}"; then
    log ${LOG_ERROR} "Invalid tenant ID: ${tenant_id}"
    exit 1
fi

# Validate URL
if ! validate_url "${tenant_domain}"; then
    log ${LOG_ERROR} "Invalid domain: ${tenant_domain}"
    exit 1
fi
```

### 3. API Error Handling

Handle Keycloak API errors properly:

```bash
# Check Keycloak connection
if ! check_keycloak_connection "${KEYCLOAK_URL}"; then
    log ${LOG_ERROR} "Cannot connect to Keycloak"
    exit 1
fi

# Handle API response
response=$(curl -s -X POST "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "${CLIENT_JSON}")

if ! handle_api_error "${response}" "create_client"; then
    log ${LOG_ERROR} "Failed to create client"
    exit 1
fi
```

### 4. Configuration Backup

Always backup before making changes:

```bash
# Backup current configuration
if ! backup_tenant_config "${tenant_id}"; then
    log ${LOG_ERROR} "Failed to backup tenant configuration"
    exit 1
fi

# Proceed with changes
update_tenant_configuration
```

### 5. Common Error Scenarios and Solutions

#### Authentication Errors
```bash
# Check token validity
if [ -z "${TOKEN}" ]; then
    log ${LOG_ERROR} "Failed to obtain access token"
    exit 1
fi
```

#### Missing Required Attributes
```bash
# Validate required attributes
if ! validate_tenant_attributes "${attributes}"; then
    log ${LOG_ERROR} "Missing required tenant attributes"
    exit 1
fi
```

#### Network Issues
```bash
# Retry mechanism for network operations
MAX_RETRIES=3
retry_count=0

while [ ${retry_count} -lt ${MAX_RETRIES} ]; do
    if check_keycloak_connection "${KEYCLOAK_URL}"; then
        break
    fi
    retry_count=$((retry_count + 1))
    sleep 5
done

if [ ${retry_count} -eq ${MAX_RETRIES} ]; then
    log ${LOG_ERROR} "Failed to connect after ${MAX_RETRIES} attempts"
    exit 1
fi
```

### 6. Best Practices for Error Handling

1. **Always Log Errors**
   ```bash
   log ${LOG_ERROR} "Detailed error message"
   ```

2. **Use Exit Codes Properly**
   ```bash
   # Success
   exit 0

   # General error
   exit 1

   # Configuration error
   exit 2

   # Network error
   exit 3
   ```

3. **Cleanup on Exit**
   ```bash
   trap cleanup EXIT
   ```

4. **Validate All Inputs**
   ```bash
   validate_tenant_id "${tenant_id}" || exit 1
   validate_url "${domain}" || exit 1
   validate_tenant_attributes "${attributes}" || exit 1
   ```

5. **Handle Timeouts**
   ```bash
   curl --connect-timeout 5 --max-time 10 [...]
   ```

### 7. Monitoring and Alerts

Configure monitoring for the error log:
```bash
# Check for critical errors
if grep -q "ERROR" "${LOG_FILE}"; then
    send_alert "Critical errors found in tenant management"
fi
```

## Troubleshooting

Common issues and solutions:

1. **Client Authentication Failed**
   - Verify client secret is correct
   - Check client status is active
   - Confirm redirect URIs are properly configured

2. **User Access Issues**
   - Verify user belongs to correct tenant group
   - Check tenant_id attribute matches
   - Confirm user roles are properly assigned

3. **Configuration Errors**
   - Validate all required attributes are set
   - Check for proper JSON formatting in attributes
   - Verify domain configurations

## Monitoring Configuration

We provide comprehensive monitoring solutions for tenant management. The monitoring system includes scripts for collecting metrics, Prometheus configuration for monitoring, and alert rules.

### 1. Tenant Monitoring Script

The `tenant-monitor.sh` script provides continuous monitoring of tenant health and resources:

```bash
# Start the monitoring script
./tenant-monitor.sh

# Features:
- Collects tenant metrics
- Monitors resource usage
- Checks configuration drift
- Generates HTML reports
- Sends alerts via webhook
```

#### Key Metrics Monitored:
- Active users
- Error rates
- Response times
- Resource usage (memory, storage)
- Configuration changes

### 2. Prometheus Configuration

Use the provided `prometheus-config.yml` for metric collection:

```yaml
scrape_configs:
  - job_name: 'keycloak'
    metrics_path: '/auth/realms/master/metrics'
    scheme: 'https'
    static_configs:
      - targets: ['keycloak:8443']
```

### 3. Alert Rules

Configure alerts using `alert-rules.yml`:

```yaml
- alert: TenantHighErrorRate
  expr: rate(keycloak_failed_login_attempts{client=~"tenant-.*"}[5m]) > 10
  for: 5m
  labels:
    severity: critical
```

### 4. Monitoring Dashboard

Access metrics through:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

### 5. Alert Thresholds

Default thresholds (configurable):
```bash
# Error rates
MAX_ERRORS=100           # per 5 minutes

# Response time
MAX_RESPONSE_TIME=2000   # milliseconds

# Resource usage
MEMORY_LIMIT=1024       # MB
STORAGE_LIMIT=5120      # MB
```

### 6. Monitoring Best Practices

1. **Regular Checks**
   ```bash
   # Check tenant health every 5 minutes
   */5 * * * * /path/to/tenant-monitor.sh
   ```

2. **Log Rotation**
   ```bash
   # Rotate logs weekly, keep 4 weeks
   /var/log/perimeterai/tenant-*.log {
       weekly
       rotate 4
       compress
   }
   ```

3. **Backup Metrics**
   ```bash
   # Daily backup of metrics
   0 0 * * * tar -czf /backup/metrics-$(date +%Y%m%d).tar.gz /var/metrics/perimeterai/
   ```

### 7. Alert Configuration

Configure alert destinations:
```bash
# Webhook
ALERT_WEBHOOK="https://alerts.example.com/webhook"

# Email
ALERT_EMAIL="admin@example.com"

# Slack
SLACK_WEBHOOK="https://hooks.slack.com/services/..."
```

### 8. Monitoring Reports

Generate and access reports:
```bash
# Generate report
./tenant-monitor.sh --report

# Report locations
HTML: /var/metrics/perimeterai/monitoring_report.html
JSON: /var/metrics/perimeterai/monitoring_report.json
```

### 9. Troubleshooting Monitoring

Common monitoring issues:

1. **No Metrics**
   - Check Prometheus connection
   - Verify Keycloak metrics endpoint
   - Check permissions

2. **False Alerts**
   - Adjust thresholds in `alert-rules.yml`
   - Verify alert conditions
   - Check time synchronization

3. **Missing Data**
   - Check disk space
   - Verify retention policies
   - Monitor scrape intervals

## Support and Maintenance

For additional support:
- Contact: support@perimeterai.com
- Documentation: [link to docs]
- Issue Tracking: [link to issue tracker]

Remember to regularly backup tenant configurations and maintain an audit log of changes.
