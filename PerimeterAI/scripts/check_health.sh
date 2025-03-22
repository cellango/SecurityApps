#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service health
check_service_health() {
    local service=$1
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' "perimeter_${service}_1" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ ${service}: Service not found${NC}"
        return 1
    fi
    
    case $health_status in
        "healthy")
            echo -e "${GREEN}✓ ${service}: Healthy${NC}"
            return 0
            ;;
        "unhealthy")
            echo -e "${RED}✗ ${service}: Unhealthy${NC}"
            return 1
            ;;
        "starting")
            echo -e "${YELLOW}⟳ ${service}: Starting${NC}"
            return 2
            ;;
        *)
            if [ "$(docker inspect --format='{{.State.Status}}' "perimeter_${service}_1" 2>/dev/null)" == "running" ]; then
                echo -e "${YELLOW}? ${service}: Running (no health check)${NC}"
                return 0
            else
                echo -e "${RED}✗ ${service}: Not running${NC}"
                return 1
            fi
            ;;
    esac
}

# Array of services to check
services=(
    "signature"
    "keycloak"
    "postgres"
    "prometheus"
    "grafana"
    "keyboard-dynamics-backend"
    "keyboard-dynamics-frontend"
    "keyboard-dynamics"
    "keyboard-dynamics-auth"
    "keyboard-dynamics-collector"
    "redis"
)

echo "Checking service health..."
echo "-------------------------"

# Track overall status
overall_status=0

# Check each service
for service in "${services[@]}"; do
    check_service_health "$service"
    status=$?
    if [ $status -ne 0 ]; then
        overall_status=1
    fi
done

echo "-------------------------"
if [ $overall_status -eq 0 ]; then
    echo -e "${GREEN}All services are healthy!${NC}"
else
    echo -e "${RED}Some services are not healthy. Please check the details above.${NC}"
fi

exit $overall_status
