# PerimeterAI

PerimeterAI is a comprehensive authentication and authorization platform built on top of Keycloak, enhanced with advanced security features including keyboard dynamics-based MFA and a policy management studio.

## Components

### 1. Keycloak Custom (keycloak-custom)
An enhanced version of Keycloak with:
- Multi-tenancy support
- High Availability features
- Modularized architecture for improved maintainability
- Custom extensions and features

### 2. Keyboard Dynamics (keyboard-dynamics)
A machine learning-based system that:
- Captures user keyboard dynamics
- Processes typing patterns
- Integrates with Keycloak for enhanced MFA
- Provides real-time risk assessment based on typing patterns

### 3. Policy Studio (policy-studio)
A standalone policy management interface that:
- Provides CRUD operations for Keycloak policies
- Offers a user-friendly interface for policy management
- Integrates with Keycloak via REST API
- Supports version control for policies

### 4. PerimeterSignature (perimeter-signature)
A customized implementation of EJBCA (Enterprise Java Beans Certificate Authority) that:
- Provides digital signature and certificate management capabilities
- Integrates with Keycloak for authentication and authorization
- Supports custom certificate profiles and validation rules
- Offers REST APIs for certificate lifecycle management

### 5. Monitoring Component (perimeter-monitoring)
The monitoring component provides centralized metrics collection and visualization for all PerimeterAI services using Prometheus and Grafana.

## Multitenancy Module

The multitenancy module provides comprehensive tenant management capabilities with built-in audit logging. This module enables secure tenant isolation and tracking of all tenant-related operations.

### Features

#### Tenant Management
- Create, read, update, and delete tenants
- Tenant status management (Active/Inactive/Deleted)
- Tenant-specific configuration storage using JSONB
- Automatic realm creation and configuration
- <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
 Container security-score-card-frontend-1  Restarting
 Container security-score-card-frontend-1  Started
 Container security-score-card-frontend-1  Restarting
 Container security-score-card-frontend-1  Started
email management

#### Audit Logging
The audit system provides comprehensive tracking of all tenant-related operations:

**Audit Events:**
- `TENANT_CREATED`: New tenant creation
- `TENANT_UPDATED`: Tenant information updates
- `TENANT_DELETED`: Tenant deletion
- `TENANT_ACTIVATED`: Tenant activation
- `TENANT_DEACTIVATED`: Tenant deactivation
- `TENANT_CONFIG_UPDATED`: Configuration changes

**Tracked Information:**
- Event type and timestamp
- Actor ID and type (Admin/User/System)
- IP address and user agent
- Detailed event information in JSON format
- Tenant context

**Query Capabilities:**
```http
# Query by tenant
GET /audit/tenant/{tenantId}?from=2024-01-01T00:00:00&to=2024-12-31T23:59:59&page=0&size=20

# Query by actor
GET /audit/actor/{actorId}?page=0&size=20

# Query by event type
GET /audit/event-type/{eventType}?page=0&size=20
```

**Retention Policy:**
- Automatic cleanup of old audit logs
- Configurable retention period (default: 365 days)
- Daily scheduled cleanup
- Manual cleanup endpoint: `DELETE /audit/retention/execute?retentionDays=365`

### Database Schema

#### Tenant Table
```sql
CREATE TABLE tenant (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    admin_email VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    configuration JSONB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

#### Audit Tables
```sql
CREATE TABLE audit_event_type (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE audit_log (
    id VARCHAR(36) PRIMARY KEY,
    event_type_id VARCHAR(36) NOT NULL,
    tenant_id VARCHAR(36) NOT NULL,
    actor_id VARCHAR(255) NOT NULL,
    actor_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (event_type_id) REFERENCES audit_event_type(id),
    FOREIGN KEY (tenant_id) REFERENCES tenant(id)
);
```

### Configuration

#### Module Configuration
```xml
<!-- modules/multitenancy/config.xml -->
<config>
    <!-- Audit Configuration -->
    <audit>
        <!-- Retention settings -->
        <retention>
            <enabled>true</enabled>
            <days>365</days>
            <schedule>0 0 0 * * ?</schedule> <!-- Daily at midnight -->
        </retention>
        
        <!-- Logging settings -->
        <logging>
            <include-ip>true</include-ip>
            <include-user-agent>true</include-user-agent>
            <max-detail-size>32768</max-detail-size>
        </logging>
        
        <!-- Query limits -->
        <query>
            <max-page-size>100</max-page-size>
            <default-page-size>20</default-page-size>
        </query>
    </audit>

    <!-- Tenant Configuration -->
    <tenant>
        <realm>
            <auto-create>true</auto-create>
            <name-pattern>tenant-{id}</name-pattern>
        </realm>
        <defaults>
            <session-timeout>1800</session-timeout>
            <max-users>1000</max-users>
        </defaults>
    </tenant>
</config>
```

#### Environment Variables
```bash
# Tenant Management
TENANT_AUTO_CREATE_REALM=true
TENANT_DEFAULT_SESSION_TIMEOUT=1800
TENANT_MAX_USERS=1000

# Audit Configuration
AUDIT_RETENTION_ENABLED=true
AUDIT_RETENTION_DAYS=365
AUDIT_INCLUDE_IP=true
AUDIT_INCLUDE_USER_AGENT=true
AUDIT_MAX_DETAIL_SIZE=32768

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=keycloak
DB_USER=keycloak
DB_PASSWORD=password
```

### Troubleshooting Guide

#### Common Issues and Solutions

1. **Tenant Creation Fails**

   Symptoms:
   - Error: "Failed to create realm"
   - Tenant status remains "PENDING"

   Solutions:
   ```java
   // Check realm creation permissions
   if (!keycloakSession.hasRealmPermission()) {
       throw new NotAuthorizedException("Insufficient permissions");
   }

   // Verify realm name uniqueness
   if (realmProvider.getRealmByName(realmName) != null) {
       throw new ConflictException("Realm already exists");
   }
   ```

2. **Audit Logs Not Being Created**

   Symptoms:
   - Missing audit entries
   - Silent failures

   Solutions:
   ```java
   // Enable debug logging
   logging.level.org.perimeter.keycloak.multitenancy=DEBUG

   // Verify transaction management
   @Transactional
   public void createAuditLog() {
       try {
           // Your audit log creation code
       } catch (Exception e) {
           log.error("Failed to create audit log", e);
           throw e;
       }
   }
   ```

3. **Retention Policy Not Working**

   Symptoms:
   - Old logs not being deleted
   - Disk space issues

   Solutions:
   ```java
   // Manual retention execution
   public void forceRetention() {
       LocalDateTime cutoff = LocalDateTime.now().minusDays(
           config.getRetentionDays());
       int deleted = auditRepository.deleteAuditLogsBefore(cutoff);
       log.info("Deleted {} old audit logs", deleted);
   }
   ```

4. **Performance Issues**

   Symptoms:
   - Slow queries
   - High memory usage

   Solutions:
   ```sql
   -- Add indexes for common queries
   CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
   CREATE INDEX idx_audit_log_tenant_actor ON audit_log(tenant_id, actor_id);
   
   -- Optimize large queries
   SELECT * FROM audit_log 
   WHERE tenant_id = ? 
   AND timestamp > ?
   ORDER BY timestamp DESC 
   LIMIT 100;
   ```

#### Diagnostic Tools

1. **Health Check Endpoint**
```http
GET /multitenancy/health
```
Response:
```json
{
    "status": "UP",
    "components": {
        "database": "UP",
        "auditService": "UP",
        "retentionPolicy": "UP"
    },
    "metrics": {
        "activeTenantsCount": 42,
        "auditLogsLast24h": 1234,
        "oldestAuditLog": "2024-01-01T00:00:00Z"
    }
}
```

2. **Debug Logging**
```properties
# logging.properties
logger.multitenancy.name=org.perimeter.keycloak.multitenancy
logger.multitenancy.level=DEBUG
```

### Enhanced Security

#### Access Control

1. **Role-Based Access Control (RBAC)**
```java
public class SecurityConfig {
    private static final String[] ADMIN_ROLES = {
        "realm-admin",
        "audit-admin"
    };
    
    private static final String[] AUDITOR_ROLES = {
        "audit-viewer"
    };
    
    public static void validateAdminAccess(KeycloakSession session) {
        if (!hasAnyRole(session, ADMIN_ROLES)) {
            throw new ForbiddenException("Requires admin role");
        }
    }
}
```

2. **API Security**
```java
@Path("/audit")
public class AuditResource {
    @GET
    @Path("/logs")
    @RolesAllowed({"audit-admin", "audit-viewer"})
    @RateLimit(requests = 100, period = 60)
    public Response getLogs() {
        // Implementation
    }
}
```

#### Data Protection

1. **Sensitive Data Handling**
```java
public class AuditLogSanitizer {
    private static final Set<String> SENSITIVE_FIELDS = Set.of(
        "password", "secret", "token", "key"
    );
    
    public static String sanitizeDetails(String details) {
        JsonNode node = objectMapper.readTree(details);
        sanitizeNode(node);
        return objectMapper.writeValueAsString(node);
    }
}
```

2. **Encryption at Rest**
```sql
-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create encrypted audit logs table
CREATE TABLE encrypted_audit_log (
    id UUID PRIMARY KEY,
    encrypted_data BYTEA,
    -- other fields
    CONSTRAINT encrypt_audit_data FOREIGN KEY (id) 
    REFERENCES audit_log(id) ON DELETE CASCADE
);
```

#### Audit Trail Security

1. **Immutability**
```java
@Entity
public class AuditLog {
    @PreUpdate
    @PreRemove
    private void blockModification() {
        throw new IllegalStateException("Audit logs are immutable");
    }
}
```

2. **Digital Signatures**
```java
public class AuditSignatureService {
    public String signAuditLog(AuditLog log) {
        String data = String.format("%s:%s:%s",
            log.getId(),
            log.getTimestamp(),
            log.getDetails()
        );
        return signatureProvider.sign(data);
    }
}
```

#### Security Best Practices

1. **Input Validation**
```java
public class TenantValidator {
    public static void validate(Tenant tenant) {
        validateName(tenant.getName());
        validateEmail(tenant.getAdminEmail());
        validateConfiguration(tenant.getConfiguration());
    }
}
```

2. **Rate Limiting**
```java
@Provider
public class RateLimitFilter implements ContainerRequestFilter {
    private final RateLimiter rateLimiter;
    
    @Override
    public void filter(ContainerRequestContext context) {
        if (!rateLimiter.tryAcquire()) {
            throw new TooManyRequestsException();
        }
    }
}
```

3. **Session Management**
```java
public class SessionConfig {
    public static void configureSession(KeycloakSession session) {
        session.getContext().setRealm(realm);
        session.getContext().setClient(client);
        session.getContext().setUser(user);
    }
}
```

### Monitoring Component

The monitoring component provides centralized metrics collection and visualization for all PerimeterAI services using Prometheus and Grafana.

#### Features

- Centralized metrics collection
- Real-time monitoring and alerting
- Pre-configured dashboards
- Auto-discovery of PerimeterAI components
- Custom alert rules
- Node-level metrics collection

#### Components

#### Prometheus
- Metrics collection and storage
- Query language for metrics analysis
- Alert manager integration
- Service discovery
- Data retention policies

#### Grafana
- Metric visualization
- Pre-configured dashboards
- Alert notifications
- User authentication
- Dashboard sharing

#### Node Exporter
- System metrics collection
- Hardware monitoring
- Resource utilization tracking

#### Configuration

#### Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'perimeter-signature'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['perimeter-signature:8080']
```

#### Alert Rules
```yaml
- alert: HighCPUUsage
  expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
  for: 5m
  labels:
    severity: warning
```

#### Metrics

#### Standard Metrics
- CPU Usage
- Memory Utilization
- Disk I/O
- Network Traffic
- Request Latency
- Error Rates

#### Custom PerimeterAI Metrics
- Signature Operations
- Certificate Management
- Authentication Events
- API Performance
- Security Events

#### Usage

1. Start the monitoring stack:
```bash
cd perimeter-monitoring
docker-compose up -d
```

2. Access interfaces:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/perimeter123)

3. View metrics:
   - System metrics: http://localhost:9100/metrics
   - Application metrics: http://<component>:8080/metrics

#### Integration

To add metrics to a new PerimeterAI component:

1. Add Prometheus client library:
```xml
<dependency>
    <groupId>io.prometheus</groupId>
    <artifactId>simpleclient</artifactId>
    <version>0.16.0</version>
</dependency>
```

2. Define metrics:
```java
static final Counter signatureRequests = Counter.build()
    .name("signature_requests_total")
    .help("Total signature requests")
    .register();
```

3. Update Prometheus configuration:
```yaml
- job_name: 'new-component'
  metrics_path: '/metrics'
  static_configs:
    - targets: ['new-component:port']
```

#### Security

- HTTPS enabled for all endpoints
- Basic authentication for Grafana
- Role-based access control
- Network isolation
- Encrypted metrics storage

#### Best Practices

1. **Metric Naming**:
   - Use lowercase with underscores
   - Include units in metric names
   - Follow the pattern: `component_metric_unit`

2. **Labels**:
   - Use meaningful label names
   - Limit cardinality
   - Include service and environment labels

3. **Alerts**:
   - Define meaningful thresholds
   - Include clear descriptions
   - Set appropriate evaluation intervals

4. **Dashboard Organization**:
   - Group related metrics
   - Use consistent naming
   - Include documentation

### Usage Examples

#### Creating a Tenant
```java
// Create tenant
Tenant tenant = new Tenant();
tenant.setName("Example Corp");
tenant.setAdminEmail("admin@example.com");
tenant.setStatus(TenantStatus.ACTIVE);
tenantRepository.create(tenant);

// Audit log is automatically created
auditService.logTenantEvent("TENANT_CREATED", tenant, "admin-user", 
    Map.of("details", "Initial tenant creation"));
```

#### Querying Audit Logs
```java
// Get recent tenant events
List<AuditLog> logs = auditRepository.findByTenantIdPaginated(
    tenantId,
    LocalDateTime.now().minusDays(7),
    LocalDateTime.now(),
    0,
    20
);

// Get actions by specific admin
List<AuditLog> adminLogs = auditRepository.findByActorIdPaginated(
    "admin-user",
    0,
    20
);
```

### Security Considerations
- Only users with the `admin` role can access audit logs
- All tenant operations are automatically logged
- IP addresses and user agents are tracked for security analysis
- Audit logs are immutable once created
- Retention policy ensures compliance with data retention requirements

### Integration Testing
The module includes comprehensive integration tests covering:
- Tenant CRUD operations
- Audit log creation and querying
- Pagination functionality
- Retention policy execution
- Date range filtering

## Architecture

Each component is containerized using Docker and has its own docker-compose configuration for isolated development and deployment. The components communicate via REST APIs, ensuring loose coupling and independent scalability.

## Getting Started

Each component has its own README with specific setup instructions. Navigate to the respective directories:

- `/keycloak-custom` - Custom Keycloak implementation
- `/keyboard-dynamics` - Keyboard dynamics ML service
- `/policy-studio` - Policy management interface
- `/perimeter-monitoring` - Monitoring component

## Contributors

### Original Contributors
- Clement Ellango
- Carolina Clement

## Prerequisites

- Docker and Docker Compose
- Java 17 or later
- Node.js 18 or later
- Python 3.8 or later (for keyboard dynamics ML component)
