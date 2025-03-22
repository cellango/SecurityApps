#!/bin/bash

# Tenant monitoring script for PerimeterAI Keycloak
# This script monitors tenant health and sends alerts when issues are detected

# Configuration
KEYCLOAK_URL="https://keycloak.example.com/auth"
REALM="perimeterai"
LOG_FILE="/var/log/perimeterai/tenant-management.log"
METRICS_DIR="/var/metrics/perimeterai"
ALERT_WEBHOOK="https://alerts.example.com/webhook"

# Ensure directories exist
mkdir -p "${METRICS_DIR}"

# Source common error handling functions
source "$(dirname "$0")/../error-handling.sh"

# Function to collect tenant metrics
collect_tenant_metrics() {
    local tenant_id=$1
    local metrics_file="${METRICS_DIR}/${tenant_id}_metrics.json"
    
    # Get tenant statistics
    local stats=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${tenant_id}/statistics" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")
    
    # Record metrics with timestamp
    echo "{
        \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
        \"stats\": ${stats}
    }" > "${metrics_file}"
    
    echo "${metrics_file}"
}

# Function to check tenant health
check_tenant_health() {
    local tenant_id=$1
    local metrics_file=$2
    
    # Read metrics
    local active_users=$(jq -r '.stats.active_users' "${metrics_file}")
    local error_count=$(jq -r '.stats.error_count' "${metrics_file}")
    local response_time=$(jq -r '.stats.avg_response_time' "${metrics_file}")
    
    # Define thresholds
    local MAX_ERRORS=100
    local MAX_RESPONSE_TIME=2000  # milliseconds
    
    # Check thresholds
    if [ "${error_count}" -gt ${MAX_ERRORS} ]; then
        send_alert "${tenant_id}" "High error count: ${error_count}"
    fi
    
    if [ "${response_time}" -gt ${MAX_RESPONSE_TIME} ]; then
        send_alert "${tenant_id}" "High response time: ${response_time}ms"
    fi
}

# Function to monitor tenant resource usage
monitor_tenant_resources() {
    local tenant_id=$1
    
    # Get resource usage
    local usage=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${tenant_id}/resource-usage" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")
    
    # Check resource limits
    local memory_usage=$(echo "${usage}" | jq -r '.memory_usage')
    local storage_usage=$(echo "${usage}" | jq -r '.storage_usage')
    
    # Define limits
    local MEMORY_LIMIT=1024  # MB
    local STORAGE_LIMIT=5120 # MB
    
    if [ "${memory_usage}" -gt ${MEMORY_LIMIT} ]; then
        send_alert "${tenant_id}" "Memory usage exceeded: ${memory_usage}MB"
    fi
    
    if [ "${storage_usage}" -gt ${STORAGE_LIMIT} ]; then
        send_alert "${tenant_id}" "Storage usage exceeded: ${storage_usage}MB"
    fi
}

# Function to check tenant configuration drift
check_configuration_drift() {
    local tenant_id=$1
    local config_file="${METRICS_DIR}/${tenant_id}_config.json"
    
    # Get current configuration
    local current_config=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${tenant_id}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")
    
    # Compare with last known configuration
    if [ -f "${config_file}" ]; then
        local diff=$(diff <(echo "${current_config}" | jq -S .) <(jq -S . "${config_file}"))
        if [ ! -z "${diff}" ]; then
            send_alert "${tenant_id}" "Configuration drift detected:\n${diff}"
        fi
    fi
    
    # Update stored configuration
    echo "${current_config}" > "${config_file}"
}

# Function to send alerts
send_alert() {
    local tenant_id=$1
    local message=$2
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Log alert
    log ${LOG_ERROR} "Alert for ${tenant_id}: ${message}"
    
    # Send to webhook
    curl -s -X POST "${ALERT_WEBHOOK}" \
        -H "Content-Type: application/json" \
        -d "{
            \"tenant_id\": \"${tenant_id}\",
            \"message\": \"${message}\",
            \"timestamp\": \"${timestamp}\",
            \"severity\": \"error\"
        }"
}

# Function to generate monitoring report
generate_report() {
    local report_file="${METRICS_DIR}/monitoring_report.html"
    
    # Create HTML report
    cat > "${report_file}" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Tenant Monitoring Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .error { color: red; }
        .warning { color: orange; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>Tenant Monitoring Report</h1>
    <p>Generated: $(date)</p>
    <h2>Alerts</h2>
    <pre>$(grep "ERROR" "${LOG_FILE}" | tail -n 10)</pre>
    <h2>Tenant Metrics</h2>
    <pre>$(find "${METRICS_DIR}" -name "*_metrics.json" -exec cat {} \; | jq -r '.')</pre>
</body>
</html>
EOF
}

# Main monitoring loop
main() {
    while true; do
        # Get all tenants
        local tenants=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
            -H "Authorization: Bearer ${TOKEN}" \
            -H "Content-Type: application/json" \
            | jq -r '.[].clientId')
        
        for tenant_id in ${tenants}; do
            # Skip non-tenant clients
            if [[ ! ${tenant_id} =~ ^tenant- ]]; then
                continue
            fi
            
            # Collect and check metrics
            metrics_file=$(collect_tenant_metrics "${tenant_id}")
            check_tenant_health "${tenant_id}" "${metrics_file}"
            monitor_tenant_resources "${tenant_id}"
            check_configuration_drift "${tenant_id}"
        done
        
        # Generate report
        generate_report
        
        # Wait before next check
        sleep 300  # 5 minutes
    done
}

# Start monitoring
main
