#!/bin/bash

# Script to create a new tenant in Keycloak
# Usage: ./create-tenant.sh <tenant-name> <tenant-domain> <tenant-plan>

# Configuration
KEYCLOAK_URL="https://keycloak.example.com/auth"
REALM="perimeterai"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="password"

# Check arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <tenant-name> <tenant-domain> <tenant-plan>"
    exit 1
fi

TENANT_NAME=$1
TENANT_DOMAIN=$2
TENANT_PLAN=$3
TENANT_ID="tenant-${TENANT_NAME,,}"  # Convert to lowercase

# Get access token
echo "Getting admin access token..."
TOKEN=$(curl -s -X POST "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${ADMIN_USERNAME}" \
    -d "password=${ADMIN_PASSWORD}" \
    -d "grant_type=password" \
    -d "client_id=admin-cli" | jq -r '.access_token')

if [ -z "$TOKEN" ]; then
    echo "Failed to get access token"
    exit 1
fi

# Create client (tenant)
echo "Creating tenant client..."
CLIENT_JSON=$(cat <<EOF
{
    "clientId": "${TENANT_ID}",
    "enabled": true,
    "protocol": "openid-connect",
    "redirectUris": ["https://${TENANT_DOMAIN}/*"],
    "webOrigins": ["https://${TENANT_DOMAIN}"],
    "publicClient": false,
    "attributes": {
        "tenant_id": "${TENANT_ID}",
        "tenant_name": "${TENANT_NAME}",
        "tenant_domain": "${TENANT_DOMAIN}",
        "tenant_plan": "${TENANT_PLAN}",
        "tenant_status": "active",
        "tenant_created": "$(date +%Y-%m-%d)"
    }
}
EOF
)

RESPONSE=$(curl -s -X POST "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "${CLIENT_JSON}")

if [ $? -eq 0 ]; then
    echo "Successfully created tenant: ${TENANT_ID}"
    
    # Get client ID
    CLIENT_UUID=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        | jq -r ".[] | select(.clientId==\"${TENANT_ID}\") | .id")
    
    # Get client secret
    CLIENT_SECRET=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${CLIENT_UUID}/client-secret" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        | jq -r '.value')
    
    echo "Client ID: ${TENANT_ID}"
    echo "Client Secret: ${CLIENT_SECRET}"
else
    echo "Failed to create tenant"
    echo "${RESPONSE}"
    exit 1
fi

# Create default roles
echo "Creating default tenant roles..."
ROLES=("tenant-admin" "tenant-user" "tenant-viewer")
for ROLE in "${ROLES[@]}"; do
    ROLE_JSON=$(cat <<EOF
    {
        "name": "${ROLE}",
        "clientRole": true,
        "composite": false
    }
EOF
    )
    
    curl -s -X POST "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${CLIENT_UUID}/roles" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "${ROLE_JSON}"
    
    if [ $? -eq 0 ]; then
        echo "Created role: ${ROLE}"
    else
        echo "Failed to create role: ${ROLE}"
    fi
done

echo "Tenant setup complete!"
