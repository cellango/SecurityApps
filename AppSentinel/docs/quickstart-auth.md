# Authentication Quick Start Guide

This guide will help you quickly get started with AppSentinel's authentication system.

## 1. Start the Services

```bash
# From project root
make start
```

## 2. Run Setup Script

```bash
cd scripts
chmod +x setup.sh
./setup.sh
```

## 3. Access the Applications

- Keycloak Admin Console: http://localhost:8080/admin
  - Username: admin
  - Password: admin

- AppInventory: http://localhost:3000
  - Test User: testuser
  - Password: testpass

## 4. Test Authentication Methods

### OAuth/OIDC Login
1. Click "Login with OAuth" on the application
2. Use test credentials
3. You'll be redirected back to the application

### SAML Login
1. Click "Login with SAML" on the application
2. Use test credentials
3. You'll be redirected back to the application

## 5. Verify Role Access

Test different role-based access:

1. Admin Access:
   - Go to /admin route
   - Should be accessible with admin role

2. User Access:
   - Go to /dashboard route
   - Should be accessible with user role

3. Viewer Access:
   - Go to /view route
   - Should be accessible with viewer role

## Need Help?

- Check the full documentation in `docs/authentication.md`
- Review logs in Keycloak admin console
- Check application logs using `docker compose logs`
