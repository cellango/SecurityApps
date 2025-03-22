from fastapi_keycloak import FastAPIKeycloak
from fastapi import Depends, HTTPException, status
from functools import wraps

# Initialize Keycloak instance
idp = FastAPIKeycloak(
    server_url="http://keycloak:8080",
    client_id="appinventory",
    client_secret="your-client-secret",  # This will be set when we create the client in Keycloak
    admin_client_secret="admin",
    realm="appsentinel",
    callback_uri="http://localhost:3000/callback"
)

# Roles required for different operations
ROLES = {
    "admin": "app-admin",
    "user": "app-user",
    "viewer": "app-viewer"
}

def require_roles(roles):
    """Decorator to check if user has required roles"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated"
                )
            
            user_roles = user.get('realm_access', {}).get('roles', [])
            if not any(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have required roles"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# SAML configuration
SAML_SETTINGS = {
    "strict": True,
    "debug": True,
    "sp": {
        "entityId": "http://localhost:5000/saml/metadata",
        "assertionConsumerService": {
            "url": "http://localhost:5000/saml/acs",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "http://localhost:5000/saml/sls",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": "",  # Will be set during Keycloak configuration
        "privateKey": ""  # Will be set during Keycloak configuration
    },
    "idp": {
        "entityId": "http://keycloak:8080/realms/appsentinel",
        "singleSignOnService": {
            "url": "http://keycloak:8080/realms/appsentinel/protocol/saml",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "http://keycloak:8080/realms/appsentinel/protocol/saml",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": ""  # Will be set during Keycloak configuration
    }
}
