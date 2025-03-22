.PHONY: build up down logs clean restart help

# Colors for output
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[1;33m
NC := \033[0m

# Variables
COMPOSE_FILE := docker-compose.yml
SERVICE_NAME := keycloak

# Build service
build:
	@echo "$(GREEN)Building Keycloak service...$(NC)"
	docker compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)Build complete!$(NC)"

# Start service and its dependencies
up:
	@echo "$(GREEN)Starting Keycloak and PostgreSQL...$(NC)"
	docker compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Services started! Keycloak will be available at http://localhost:8081$(NC)"
	@echo "$(YELLOW)Admin credentials: admin/admin$(NC)"

# Stop service and its dependencies
down:
	@echo "$(RED)Stopping services...$(NC)"
	docker compose -f $(COMPOSE_FILE) down
	@echo "$(GREEN)Services stopped!$(NC)"

# View logs
logs:
	@echo "$(YELLOW)Showing Keycloak logs...$(NC)"
	docker compose -f $(COMPOSE_FILE) logs -f $(SERVICE_NAME)

# Clean up containers and volumes
clean:
	@echo "$(RED)Cleaning up resources...$(NC)"
	docker compose -f $(COMPOSE_FILE) down -v
	@echo "$(GREEN)Cleanup complete!$(NC)"

# Restart service
restart: down up
	@echo "$(GREEN)Services restarted!$(NC)"

# Health check
health:
	@echo "$(YELLOW)Checking Keycloak health...$(NC)"
	@curl -s http://localhost:8081/health/ready || echo "$(RED)Health check failed!$(NC)"

# Help target
help:
	@echo "$(GREEN)Available targets:$(NC)"
	@echo "  $(YELLOW)build$(NC)   - Build Keycloak service"
	@echo "  $(YELLOW)up$(NC)      - Start Keycloak and PostgreSQL"
	@echo "  $(YELLOW)down$(NC)    - Stop all services"
	@echo "  $(YELLOW)logs$(NC)    - View Keycloak logs"
	@echo "  $(YELLOW)clean$(NC)   - Clean up all resources including volumes"
	@echo "  $(YELLOW)restart$(NC) - Restart all services"
	@echo "  $(YELLOW)health$(NC)  - Check Keycloak health status"
	@echo "  $(YELLOW)help$(NC)    - Show this help message"

# Default target
.DEFAULT_GOAL := help
