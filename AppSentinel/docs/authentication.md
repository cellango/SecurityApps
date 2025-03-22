# Authentication in AppSentinel

AppSentinel provides enterprise-grade authentication using both OAuth/OIDC and SAML protocols, powered by Keycloak as the Identity Provider (IdP). This document explains the authentication setup, configuration, and usage.

## Overview

The authentication system supports:
- OAuth 2.0/OpenID Connect (OIDC) authentication
- SAML 2.0 authentication
- Role-Based Access Control (RBAC)
- Single Sign-On (SSO) across AppInventory and AppScore
- Secure token handling and validation

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │ ←──► │   Backend   │ ←──► │  Keycloak   │
│   (React)   │      │  (FastAPI)  │      │    (IdP)    │
└─────────────┘      └─────────────┘      └─────────────┘
```

## Setup and Configuration

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Node.js 14+

### Initial Setup

1. Start the services:
```bash
make start
```

2. Run the setup script:
```bash
cd scripts
chmod +x setup.sh
./setup.sh
```

### Default Credentials

- Keycloak Admin:
  - URL: http://localhost:8080/admin
  - Username: admin
  - Password: admin

- Test User:
  - Username: testuser
  - Password: testpass

## Role-Based Access Control

The system includes three default roles:

1. `app-admin`:
   - Full system access
   - Can manage users and roles
   - Access to admin-only endpoints

2. `app-user`:
   - Standard user access
   - Can use all regular application features
   - Cannot access admin endpoints

3. `app-viewer`:
   - Read-only access
   - Can view but not modify data
   - Limited feature access

## Authentication Methods

### OAuth/OIDC Authentication

1. Frontend Implementation:
```javascript
// Use the Auth component
import Auth from './components/Auth';

function App() {
  return (
    <Auth>
      <YourApp />
    </Auth>
  );
}
```

2. Protected API Endpoints:
```python
@app.get("/api/protected")
@require_roles([ROLES["user"]])
async def protected_route(user=Depends(idp.get_current_user)):
    return {"message": "Protected data", "user": user}
```

### SAML Authentication

1. Service Provider (SP) Configuration:
   - Entity ID: http://localhost:5000/saml/metadata
   - ACS URL: http://localhost:5000/saml/acs
   - SLO URL: http://localhost:5000/saml/sls

2. Identity Provider (IdP) Configuration:
   - Entity ID: http://keycloak:8080/realms/appsentinel
   - SSO URL: http://keycloak:8080/realms/appsentinel/protocol/saml
   - SLO URL: http://keycloak:8080/realms/appsentinel/protocol/saml

## Security Considerations

1. Token Storage:
   - Access tokens are stored in browser's localStorage
   - Refresh tokens are handled securely by Keycloak
   - SAML assertions are never stored client-side

2. CORS Configuration:
   - Strict origin checking
   - Limited to application domains
   - Credentials included in requests

3. SSL/TLS:
   - Required for production deployments
   - Optional for development

## Customization

### Custom Roles

Add new roles through Keycloak admin console:
1. Navigate to Roles
2. Click "Create Role"
3. Set role name and description
4. Assign to users/groups

### Custom Claims

Add custom claims in Keycloak:
1. Navigate to Client Scopes
2. Create or select a scope
3. Add mapper for custom claims

## Troubleshooting

Common issues and solutions:

1. Token Validation Fails:
   - Check token expiration
   - Verify Keycloak realm matches
   - Ensure correct client secret

2. SAML Authentication Fails:
   - Verify metadata configuration
   - Check certificate validity
   - Ensure clock synchronization

3. Role Access Denied:
   - Check user role assignments
   - Verify role mapping configuration
   - Check required roles in code

## API Reference

### OAuth Endpoints

```
GET /auth/login          # Redirect to Keycloak login
GET /auth/callback       # OAuth callback handler
GET /auth/logout         # Logout and clear session
```

### SAML Endpoints

```
GET  /saml/metadata     # SAML metadata endpoint
POST /saml/acs         # Assertion Consumer Service
GET  /saml/sls         # Single Logout Service
```

## Development Guidelines

1. Adding Protected Routes:
```python
@app.get("/api/your-route")
@require_roles([ROLES["user"]])
async def your_route(user=Depends(idp.get_current_user)):
    # Your code here
    pass
```

2. Accessing User Context:
```python
# In FastAPI endpoints
user = idp.get_current_user()
user_roles = user.get('realm_access', {}).get('roles', [])
```

3. Frontend Role Checking:
```javascript
const hasRole = (role) => {
  const user = getCurrentUser();
  return user?.roles?.includes(role);
};
```

## Production Deployment

Additional steps for production:

1. SSL/TLS Configuration:
   - Enable HTTPS
   - Update callback URLs
   - Configure secure cookies

2. Security Headers:
   - Enable CSP
   - Set X-Frame-Options
   - Configure HSTS

3. Monitoring:
   - Enable Keycloak audit logging
   - Monitor failed authentication attempts
   - Set up alerts for suspicious activities
