#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print with timestamp
log() {
    local level=$1
    local message=$2
    local color=$3
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message${NC}"
}

# Function to handle errors
handle_error() {
    log "ERROR" "An error occurred. Cleaning up..." "$RED"
    exit 1
}

# Set error handling
trap 'handle_error' ERR

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log "ERROR" "Docker is not running. Please start Docker first." "$RED"
        exit 1
    fi
}

# Main cleanup function
cleanup() {
    local prefix=$1
    
    log "INFO" "Starting cleanup for ${prefix} containers and resources..." "$GREEN"
    
    # Stop all containers with the prefix
    log "INFO" "Stopping containers..." "$YELLOW"
    if [[ $(docker ps -q -f name="${prefix}") ]]; then
        docker compose down || log "WARN" "Some containers could not be stopped" "$YELLOW"
    else
        log "INFO" "No running containers found" "$GREEN"
    fi
    
    # Remove containers
    log "INFO" "Removing containers..." "$YELLOW"
    if [[ $(docker ps -a -q -f name="${prefix}") ]]; then
        docker rm -f $(docker ps -a | grep "${prefix}" | awk '{print $1}') 2>/dev/null || \
            log "WARN" "Some containers could not be removed" "$YELLOW"
    else
        log "INFO" "No containers to remove" "$GREEN"
    fi
    
    # Remove networks
    log "INFO" "Removing networks..." "$YELLOW"
    if [[ $(docker network ls | grep "${prefix}") ]]; then
        docker network rm $(docker network ls | grep "${prefix}" | awk '{print $1}') 2>/dev/null || \
            log "WARN" "Some networks could not be removed" "$YELLOW"
    else
        log "INFO" "No networks to remove" "$GREEN"
    fi
    
    # Remove volumes (optional, uncomment if needed)
    # log "INFO" "Removing volumes..." "$YELLOW"
    # docker volume rm $(docker volume ls -q -f name="${prefix}") 2>/dev/null || \
    #     log "WARN" "Some volumes could not be removed" "$YELLOW"
    
    # Remove unused images (optional)
    log "INFO" "Checking for dangling images..." "$YELLOW"
    if [[ $(docker images -q -f "dangling=true") ]]; then
        docker image prune -f || log "WARN" "Could not remove dangling images" "$YELLOW"
    else
        log "INFO" "No dangling images found" "$GREEN"
    fi
}

# Check if Docker is running
check_docker

# Main execution
log "INFO" "Starting AppSentinel cleanup process..." "$GREEN"

# Clean AppInventory containers and resources
cleanup "appinventory"

# Clean AppScore containers and resources
cleanup "appscore"

# Final status
log "SUCCESS" "Cleanup completed successfully!" "$GREEN"
log "INFO" "You can now start the services with 'make start' or 'docker compose up -d'" "$GREEN"
