# PerimeterAI User Guide

## Overview
PerimeterAI is a comprehensive security platform that combines keyboard dynamics analysis, signature verification, policy management, and robust identity and access management. This guide provides detailed information about each component and how to use them.

## Components

### 1. Identity and Access Management (Keycloak)
**URL**: `http://localhost:8081`
- **Admin Console**: `http://localhost:8081/admin`
- **Account Console**: `http://localhost:8081/realms/master/account`

#### Features:
- User Authentication and Authorization
- Tenant Management
- Role-Based Access Control
- Single Sign-On (SSO)
- Multi-Factor Authentication

#### Tenant Management:
1. Log in to the Admin Console
2. Navigate to the "Tenant Info" tab
3. Here you can:
   - View existing tenants
   - Create new tenants
   - Edit tenant details
   - Delete tenants

### 2. Keyboard Dynamics Platform
The keyboard dynamics platform consists of multiple services working together to provide behavioral biometric authentication.

#### Frontend Application
**URL**: `http://localhost:3002`
- User interface for keyboard dynamics enrollment
- Real-time typing pattern visualization
- User profile management
- Authentication status monitoring

#### Analytics Service
**URL**: `http://localhost:5000`
- Behavioral biometric analysis
- User typing pattern recognition
- Risk score calculation
- Anomaly detection
- Machine learning model management

#### Collector Service
**URL**: `http://localhost:3001`
- Real-time keystroke data collection
- Data preprocessing
- Secure data transmission

#### Authentication Service
**URL**: `http://localhost:4000`
- User authentication based on typing patterns
- Session management
- Integration with Keycloak
- Risk-based authentication decisions

### 3. Signature Verification Service
**URL**: `http://localhost:8082`

#### Features:
- Digital signature verification
- Document signing capabilities
- PKI infrastructure integration
- Signature validation
- Audit trail management
- Certificate management

#### Key Components:
- Signature API Gateway
- Certificate Authority Integration
- Document Processing Engine
- Validation Service
- Audit Service

### 4. Policy Studio
**Frontend URL**: `http://localhost:3000`
**Backend URL**: `http://localhost:4000`

#### Features:
- Visual policy creation and management
- Real-time policy validation
- Policy version control
- Policy testing and simulation
- Integration with Keycloak
- Policy deployment management

#### Key Components:
- Policy Designer UI
  - Visual policy editor
  - Policy templates
  - Condition builder
  - Action configurator
  - Testing interface
  
- Policy Management Backend
  - Policy storage and versioning
  - Policy validation engine
  - Integration APIs
  - Deployment orchestration
  
- Policy Database
  - Version history
  - Policy metadata
  - Deployment states
  - Audit logs

#### Policy Types:
1. Authentication Policies
   - Multi-factor authentication rules
   - Risk-based authentication
   - Session management
   
2. Authorization Policies
   - Resource access control
   - Role-based permissions
   - Attribute-based access control
   
3. Risk Management Policies
   - Threat detection rules
   - Behavioral analysis thresholds
   - Alert and notification rules

### 5. Monitoring and Analytics
- **Grafana**: `http://localhost:3000`
  - Real-time monitoring dashboards
  - Performance metrics
  - User behavior analytics
  - System health monitoring
- **Prometheus**: `http://localhost:9090`
  - Metrics collection
  - Alert management
  - Performance data storage
- **Redis**: `localhost:6379`
  - Session storage
  - Cache management
  - Real-time data processing
- **PostgreSQL**: `localhost:5432`
  - User data storage
  - Typing pattern storage
  - Tenant management data
  - Audit logs

## Component Integration

### Authentication Flow
1. User accesses protected resource
2. Keycloak initiates authentication
3. Keyboard Dynamics service collects typing patterns
4. Analytics service evaluates risk score
5. Authentication decision is made based on:
   - Traditional credentials
   - Typing pattern match
   - Risk score
   - Signature verification (if required)
6. Policy Studio evaluates applicable policies
7. Final access decision is made based on policy evaluation

### Policy Enforcement Flow
1. User requests access to a resource
2. Policy enforcement point intercepts request
3. Policy Studio evaluates applicable policies
4. Policies are evaluated considering:
   - User attributes
   - Resource characteristics
   - Environmental factors
   - Risk scores
   - Authentication status
5. Access decision is returned
6. Policy enforcement point applies the decision

### Data Flow
1. Collector service captures raw keystroke data
2. Data is preprocessed and normalized
3. Analytics service processes the data
4. Results are stored in PostgreSQL
5. Risk scores are cached in Redis
6. Authentication service makes decisions
7. Metrics are sent to Prometheus
8. Grafana visualizes the results

## Environment Setup

### Prerequisites
- Docker and Docker Compose
- Java 11 or higher
- Node.js 14 or higher
- Gradle (for signature service)

### Starting the Services
```bash
# Clone the repository
git clone https://github.com/your-org/PerimeterAI.git

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### Configuration
Each component has its own configuration files:
- Keyboard Dynamics: `/services/config/*.yml`
- Signature Service: `/conf/*.xml`
- Keycloak: `/config/keycloak.conf`
- Policy Studio:
  - Frontend: `/frontend/config/*.js`
  - Backend: `/backend/config/*.yml`

## Security Considerations
1. Always use HTTPS in production
2. Regularly rotate API keys and secrets
3. Monitor system logs for suspicious activities
4. Keep all components updated to the latest versions
5. Follow the principle of least privilege
6. Implement proper certificate management
7. Regular security audits
8. Data encryption at rest and in transit

## Troubleshooting

### Common Issues
1. **Service not starting**
   - Check Docker logs: `docker-compose logs [service-name]`
   - Verify port availability
   - Check configuration files

2. **Authentication Issues**
   - Verify Keycloak configuration
   - Check client credentials
   - Validate token settings
   - Check signature service status

3. **Data Collection Issues**
   - Verify network connectivity
   - Check Redis connection
   - Validate data format
   - Monitor collector service logs

4. **Signature Verification Issues**
   - Check certificate validity
   - Verify PKI configuration
   - Monitor signature service logs
   - Check document format compatibility

## Support and Resources
- GitHub Repository: [PerimeterAI Repository]
- Documentation: [Full API Documentation]
- Issue Tracker: [GitHub Issues]
- Community Forum: [PerimeterAI Community]

## Version Information
- Keycloak: 26.0.7
- Flask: 2.0.1
- SQLAlchemy: 1.4.23
- Redis: 3.5.3
- Node.js: 14.x
- Signature Service: 1.0.0

## License
[Include license information here]
