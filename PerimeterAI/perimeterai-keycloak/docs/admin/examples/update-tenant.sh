#!/bin/bash

# Script to update tenant configuration in Keycloak
# Usage: ./update-tenant.sh <tenant-id> <attribute> <value>

# Configuration
KEYCLOAK_URL="https://keycloak.example.com/auth"
REALM="perimeterai"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="password"

# Check arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <tenant-id> <attribute> <value>"
    echo "Example: $0 tenant-acme tenant_status inactive"
    exit 1
fi

TENANT_ID=$1
ATTRIBUTE=$2
VALUE=$3

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

# Get client UUID
CLIENT_UUID=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    | jq -r ".[] | select(.clientId==\"${TENANT_ID}\") | .id")

if [ -z "$CLIENT_UUID" ]; then
    echo "Tenant not found: ${TENANT_ID}"
    exit 1
fi

# Get current client configuration
CLIENT_CONFIG=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${CLIENT_UUID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json")

# Update attribute
UPDATED_CONFIG=$(echo "${CLIENT_CONFIG}" | jq ".attributes.${ATTRIBUTE} = \"${VALUE}\"")

# Update client
RESPONSE=$(curl -s -X PUT "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${CLIENT_UUID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "${UPDATED_CONFIG}")

if [ $? -eq 0 ]; then
    echo "Successfully updated tenant ${TENANT_ID}"
    echo "Set ${ATTRIBUTE} = ${VALUE}"
else
    echo "Failed to update tenant"
    echo "${RESPONSE}"
    exit 1
fi
