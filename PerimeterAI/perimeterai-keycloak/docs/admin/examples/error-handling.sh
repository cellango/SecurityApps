#!/bin/bash

# Common error handling functions for tenant management scripts

# Log levels
LOG_ERROR=0
LOG_WARN=1
LOG_INFO=2
LOG_DEBUG=3

# Default log level
CURRENT_LOG_LEVEL=${LOG_INFO}

# Log file location
LOG_FILE="/var/log/perimeterai/tenant-management.log"

# Ensure log directory exists
mkdir -p "$(dirname "${LOG_FILE}")"

# Function to log messages
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ ${level} -le ${CURRENT_LOG_LEVEL} ]; then
        case ${level} in
            ${LOG_ERROR}) prefix="ERROR";;
            ${LOG_WARN})  prefix="WARN ";;
            ${LOG_INFO})  prefix="INFO ";;
            ${LOG_DEBUG}) prefix="DEBUG";;
            *)           prefix="OTHER";;
        esac
        
        echo "[${timestamp}] ${prefix}: ${message}" | tee -a "${LOG_FILE}"
    fi
}

# Function to validate tenant ID format
validate_tenant_id() {
    local tenant_id=$1
    if [[ ! ${tenant_id} =~ ^tenant-[a-z0-9-]+$ ]]; then
        log ${LOG_ERROR} "Invalid tenant ID format: ${tenant_id}. Must start with 'tenant-' and contain only lowercase letters, numbers, and hyphens."
        return 1
    fi
    return 0
}

# Function to validate URL format
validate_url() {
    local url=$1
    if [[ ! ${url} =~ ^https?:// ]]; then
        log ${LOG_ERROR} "Invalid URL format: ${url}. Must start with http:// or https://"
        return 1
    fi
    return 0
}

# Function to check Keycloak connection
check_keycloak_connection() {
    local keycloak_url=$1
    local timeout=5
    
    if ! curl --connect-timeout ${timeout} -s "${keycloak_url}" > /dev/null; then
        log ${LOG_ERROR} "Failed to connect to Keycloak at ${keycloak_url}"
        return 1
    fi
    return 0
}

# Function to handle API errors
handle_api_error() {
    local response=$1
    local operation=$2
    
    if [[ $(echo "${response}" | jq -r '.error') != "null" ]]; then
        local error_message=$(echo "${response}" | jq -r '.error_description // .error')
        log ${LOG_ERROR} "API Error during ${operation}: ${error_message}"
        return 1
    fi
    return 0
}

# Function to validate tenant attributes
validate_tenant_attributes() {
    local attributes=$1
    local required_attrs=("tenant_id" "tenant_name" "tenant_domain" "tenant_plan" "tenant_status")
    
    for attr in "${required_attrs[@]}"; do
        if [[ $(echo "${attributes}" | jq -r ".${attr}") == "null" ]]; then
            log ${LOG_ERROR} "Missing required attribute: ${attr}"
            return 1
        fi
    done
    return 0
}

# Function to backup tenant configuration
backup_tenant_config() {
    local tenant_id=$1
    local backup_dir="/var/backup/perimeterai/tenants"
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local backup_file="${backup_dir}/${tenant_id}_${timestamp}.json"
    
    mkdir -p "${backup_dir}"
    
    if ! echo "${TENANT_CONFIG}" > "${backup_file}"; then
        log ${LOG_ERROR} "Failed to create backup for tenant ${tenant_id}"
        return 1
    fi
    
    log ${LOG_INFO} "Backup created: ${backup_file}"
    return 0
}

# Function to handle cleanup on script exit
cleanup() {
    local exit_code=$?
    if [ ${exit_code} -ne 0 ]; then
        log ${LOG_ERROR} "Script failed with exit code: ${exit_code}"
    fi
    exit ${exit_code}
}

# Set trap for cleanup
trap cleanup EXIT

# Example usage of error handling
example_error_handling() {
    local tenant_id=$1
    
    # Validate input
    if ! validate_tenant_id "${tenant_id}"; then
        return 1
    fi
    
    # Check Keycloak connection
    if ! check_keycloak_connection "${KEYCLOAK_URL}"; then
        return 1
    fi
    
    # Perform operation with error handling
    local response=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")
    
    if ! handle_api_error "${response}" "get_clients"; then
        return 1
    fi
    
    log ${LOG_INFO} "Operation completed successfully"
    return 0
}
