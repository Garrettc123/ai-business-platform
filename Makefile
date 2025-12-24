.PHONY: help build up down logs ps clean test deploy k8s-deploy k8s-delete

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

ps: ## Show service status
	docker-compose ps

clean: ## Remove all containers, volumes, and images
	docker-compose down -v
	docker system prune -f

test: ## Run tests
	docker-compose exec app pytest

restart: ## Restart services
	docker-compose restart

# Kubernetes targets
k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/secrets.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/postgres.yaml
	kubectl apply -f k8s/redis.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/ingress.yaml

k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

k8s-status: ## Check Kubernetes deployment status
	kubectl get all -n ai-platform

k8s-logs: ## View Kubernetes logs
	kubectl logs -l app=ai-platform -n ai-platform -f

k8s-shell: ## Get shell in running pod
	kubectl exec -it $$(kubectl get pod -l app=ai-platform -n ai-platform -o jsonpath='{.items[0].metadata.name}') -n ai-platform -- bash

# Development targets
dev: ## Start in development mode
	docker-compose -f docker-compose.yml up

prod: ## Start in production mode
	docker-compose up -d

backup: ## Backup database
	docker-compose exec postgres pg_dump -U admin ai_platform > backup_$$(date +%Y%m%d_%H%M%S).sql

restore: ## Restore database (use BACKUP_FILE=filename.sql)
	cat $(BACKUP_FILE) | docker-compose exec -T postgres psql -U admin ai_platform
