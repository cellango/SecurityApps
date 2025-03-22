#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${RED}Stopping all PerimeterAI containers...${NC}"
docker compose down

echo -e "${RED}Removing all PerimeterAI containers...${NC}"
docker rm -f $(docker ps -a | grep 'perimeter\|perimeterai' | awk '{print $1}') 2>/dev/null || true

echo -e "${RED}Removing all PerimeterAI networks...${NC}"
docker network rm $(docker network ls | grep 'perimeter\|perimeterai' | awk '{print $1}') 2>/dev/null || true

echo -e "${GREEN}Cleanup complete! You can now start the services with 'docker compose up -d'${NC}"
