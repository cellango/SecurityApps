.PHONY: keycloak-build keycloak-up keycloak-down keycloak-logs keycloak-clean keycloak-restart

# Colors for output
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[1;33m
NC := \033[0m

# Variables
COMPOSE_FILE := docker-compose.keycloak.yml
KEYCLOAK_SERVICE := keycloak
POSTGRES_SERVICE := postgres

# Build Keycloak service
keycloak-build:
	@echo "$(GREEN)Building Keycloak service...$(NC)"
	docker compose -f $(COMPOSE_FILE) build $(KEYCLOAK_SERVICE)
	@echo "$(GREEN)Build complete!$(NC)"

# Start Keycloak and its dependencies
keycloak-up:
	@echo "$(GREEN)Starting Keycloak and PostgreSQL...$(NC)"
	docker compose -f $(COMPOSE_FILE) up -d $(POSTGRES_SERVICE) $(KEYCLOAK_SERVICE)
	@echo "$(GREEN)Services started! Keycloak will be available at http://localhost:8081$(NC)"
	@echo "$(YELLOW)Admin credentials: admin/admin$(NC)"

# Stop Keycloak and its dependencies
keycloak-down:
	@echo "$(RED)Stopping Keycloak and PostgreSQL...$(NC)"
	docker compose -f $(COMPOSE_FILE) stop $(KEYCLOAK_SERVICE) $(POSTGRES_SERVICE)
	@echo "$(GREEN)Services stopped!$(NC)"

# View Keycloak logs
keycloak-logs:
	@echo "$(YELLOW)Showing Keycloak logs...$(NC)"
	docker compose -f $(COMPOSE_FILE) logs -f $(KEYCLOAK_SERVICE)

# Clean up Keycloak containers and volumes
keycloak-clean:
	@echo "$(RED)Cleaning up Keycloak resources...$(NC)"
	docker compose -f $(COMPOSE_FILE) rm -f $(KEYCLOAK_SERVICE)
	docker compose -f $(COMPOSE_FILE) rm -f $(POSTGRES_SERVICE)
	@echo "$(GREEN)Cleanup complete!$(NC)"

# Restart Keycloak service
keycloak-restart: keycloak-down keycloak-up
	@echo "$(GREEN)Keycloak service restarted!$(NC)"

# Help target
help:
	@echo "$(GREEN)Available targets:$(NC)"
	@echo "  $(YELLOW)keycloak-build$(NC)   - Build Keycloak service"
	@echo "  $(YELLOW)keycloak-up$(NC)      - Start Keycloak and PostgreSQL"
	@echo "  $(YELLOW)keycloak-down$(NC)    - Stop Keycloak and PostgreSQL"
	@echo "  $(YELLOW)keycloak-logs$(NC)    - View Keycloak logs"
	@echo "  $(YELLOW)keycloak-clean$(NC)   - Clean up Keycloak containers and volumes"
	@echo "  $(YELLOW)keycloak-restart$(NC) - Restart Keycloak service"
	@echo "  $(YELLOW)help$(NC)             - Show this help message"

# Default target
.DEFAULT_GOAL := help
