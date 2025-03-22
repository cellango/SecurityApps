# Makefile for AppScore

# Variables
PYTHON = python3
PIP = pip3
FLASK = flask
NPM = npm
PYTEST = pytest
DOCKER = docker
DOCKER_COMPOSE = docker compose

# Colors for output
YELLOW = \033[1;33m
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m # No Color

# Directories
BACKEND_DIR = backend
FRONTEND_DIR = frontend
TEST_DIR = tests

.PHONY: help setup install test lint clean run docker-build docker-up docker-down migrate seed rebuild dev format lint-frontend format-frontend

help:
	@echo "$(YELLOW)AppScore Management Commands$(NC)"
	@echo "$(YELLOW)---------------------------$(NC)"
	@echo "make setup              - Initial project setup (dependencies, database)"
	@echo "make install           - Install all dependencies"
	@echo "make run              - Run both backend and frontend servers"
	@echo "make test             - Run all tests"
	@echo "make lint             - Run linters"
	@echo "make clean            - Clean up generated files"
	@echo "make migrate          - Run database migrations"
	@echo "make seed             - Seed database with sample data"
	@echo "make format           - Format code"

setup: install migrate seed
	@echo "$(GREEN)Setup complete!$(NC)"

install:
	@echo "$(GREEN)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) install

dev:
	cd $(BACKEND_DIR) && $(FLASK) run --port=5002 --debug &
	cd $(FRONTEND_DIR) && $(NPM) start

test:
	@echo "$(GREEN)Running backend tests...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) test

lint:
	@echo "$(GREEN)Linting backend code...$(NC)"
	cd $(BACKEND_DIR) && flake8

lint-frontend:
	@echo "$(GREEN)Linting frontend code...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run lint

format:
	@echo "$(GREEN)Formatting backend code...$(NC)"
	cd $(BACKEND_DIR) && black .

format-frontend:
	@echo "$(GREEN)Formatting frontend code...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run format

migrate:
	@echo "$(GREEN)Running database migrations...$(NC)"
	cd $(BACKEND_DIR) && $(FLASK) db upgrade

seed:
	@echo "$(GREEN)Seeding AppScore database...$(NC)"
	@if ! docker compose ps | grep -q "appscore-backend-1.*healthy"; then \
		echo "$(RED)Error: Backend container is not running or not healthy. Please start containers with 'docker compose up -d'$(NC)"; \
		exit 1; \
	fi
	@if ! docker compose ps | grep -q "appinventory-appinventory-db-1.*healthy"; then \
		echo "$(RED)Error: Database container is not running or not healthy. Please start containers with 'docker compose up -d'$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Waiting for database to be ready...$(NC)"
	@docker compose exec appinventory-appinventory-db-1 pg_isready -U postgres -d appscore || sleep 5
	@echo "$(GREEN)Running seed script...$(NC)"
	docker compose exec -T appscore-backend-1 python -m scripts.populate_sample_data

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "node_modules" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
