.PHONY: help install start stop restart clean test lint format migrate-all rebuild restart-full

# Colors for terminal output
BLUE=\033[0;34m
GREEN=\033[0;32m
RED=\033[0;31m
YELLOW=\033[1;33m
NC=\033[0m # No Color

# Help command
help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-30s$(NC) %s\n", $$1, $$2}'

# Installation commands
install: ## Install all dependencies for both services
	@echo "$(GREEN)Installing dependencies for AppInventory...$(NC)"
	cd AppInventory && make install
	@echo "$(GREEN)Installing dependencies for AppScore...$(NC)"
	cd AppScore && make install

# Docker commands
start: ## Start all services using docker-compose
	@echo "$(GREEN)Starting all services...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Services started successfully!$(NC)"
	@echo "$(BLUE)AppInventory Backend: http://localhost:5001$(NC)"
	@echo "$(BLUE)AppScore Backend: http://localhost:5002$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"

stop: ## Stop all services
	@echo "$(RED)Stopping all services...$(NC)"
	@pkill -f celery || true
	docker compose down
	@echo "$(RED)Stopping AppInventory services...$(NC)"
	cd AppInventory && docker compose down

rebuild: ## Rebuild all docker images
	@echo "$(YELLOW)Rebuilding all docker images...$(NC)"
	docker compose build --no-cache

restart: stop start ## Simple restart (stop and start)

restart-full: ## Full restart: stop, clean, rebuild, and start
	@echo "$(YELLOW)Performing full restart...$(NC)"
	@echo "$(RED)Stopping all services...$(NC)"
	docker compose down
	@echo "$(RED)Cleaning up volumes...$(NC)"
	docker compose down -v
	@echo "$(YELLOW)Rebuilding all images...$(NC)"
	docker compose build --no-cache
	@echo "$(GREEN)Starting services...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Full restart completed!$(NC)"
	@echo "$(BLUE)AppInventory Backend: http://localhost:5001$(NC)"
	@echo "$(BLUE)AppScore Backend: http://localhost:5002$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"

clean: ## Clean up docker volumes and temporary files
	@echo "$(RED)Cleaning up...$(NC)"
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "node_modules" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Development commands
dev-appinventory: ## Start AppInventory in development mode
	@echo "$(GREEN)Starting AppInventory in development mode...$(NC)"
	cd AppInventory && make dev

dev-appscore: ## Start AppScore in development mode
	@echo "$(GREEN)Starting AppScore in development mode...$(NC)"
	cd AppScore && make dev

# Database commands
migrate-appinventory: ## Run database migrations for AppInventory
	@echo "$(GREEN)Running AppInventory migrations...$(NC)"
	cd AppInventory && make migrate

migrate-appscore: ## Run database migrations for AppScore
	@echo "$(GREEN)Running AppScore migrations...$(NC)"
	cd AppScore && make migrate

migrate-all: migrate-appinventory migrate-appscore ## Run all database migrations

# Testing commands
test: ## Run all tests
	@echo "$(GREEN)Running AppInventory tests...$(NC)"
	cd AppInventory && make test
	@echo "$(GREEN)Running AppScore tests...$(NC)"
	cd AppScore && make test

# Code quality commands
lint: ## Run linters on all code
	@echo "$(GREEN)Linting Python code...$(NC)"
	cd AppInventory && make lint
	cd AppScore && make lint
	@echo "$(GREEN)Linting JavaScript code...$(NC)"
	cd AppInventory && make lint-frontend
	cd AppScore && make lint-frontend

format: ## Format all code
	@echo "$(GREEN)Formatting Python code...$(NC)"
	cd AppInventory && make format
	cd AppScore && make format
	@echo "$(GREEN)Formatting JavaScript code...$(NC)"
	cd AppInventory && make format-frontend
	cd AppScore && make format-frontend

# Logs
logs: ## View docker compose logs
	docker compose logs -f

# Default command
.DEFAULT_GOAL := help
