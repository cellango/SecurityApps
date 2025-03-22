.PHONY: help dev prod clean stop restart logs test lint

# Variables
APP_NAME = appinventory-frontend
DOCKER_REGISTRY = # Add your registry here if needed

help: ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment
	docker-compose up --build

dev-detach: ## Start development environment in detached mode
	docker-compose up --build -d

prod: ## Build production image
	docker build -t $(APP_NAME) \
		--target production \
		--build-arg NODE_ENV=production \
		.

prod-run: prod ## Build and run production image
	docker run -p 3000:3000 $(APP_NAME)

clean: stop ## Clean up containers, images, and build cache
	docker-compose down --rmi all --volumes --remove-orphans
	rm -rf node_modules build
	docker system prune -f

stop: ## Stop all containers
	docker-compose down

restart: stop dev ## Restart development environment

logs: ## Show development logs
	docker-compose logs -f

test: ## Run tests
	docker-compose run --rm frontend npm run test:ci

lint: ## Run linting
	docker-compose run --rm frontend npm run lint

type-check: ## Run type checking
	docker-compose run --rm frontend npm run type-check

format: ## Format code
	docker-compose run --rm frontend npm run format
