#!/bin/bash

# AI Business Platform - Quick Deploy Script
set -e

echo "=================================="
echo "AI Business Platform Deployment"
echo "=================================="
echo ""

# Check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "✅ Docker is installed: $(docker --version)"
    echo "✅ Docker Compose is installed: $(docker-compose --version)"
    echo ""
}

# Create .env file if it doesn't exist
setup_env() {
    if [ ! -f .env ]; then
        echo "Creating .env file from template..."
        cp .env.example .env
        echo "⚠️  Please edit .env file with your configuration before proceeding to production!"
        echo ""
    else
        echo "✅ .env file already exists"
        echo ""
    fi
}

# Deploy function
deploy() {
    echo "Starting deployment..."
    echo ""
    
    # Build images
    echo "📦 Building Docker images..."
    docker-compose build
    
    # Start services
    echo "🚀 Starting services..."
    docker-compose up -d
    
    # Wait for services to be healthy
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    # Check status
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "Access points:"
    echo "  - Application API: http://localhost:8000"
    echo "  - PostgreSQL: localhost:5432"
    echo "  - Redis: localhost:6379"
    echo "  - Kafka: localhost:9092"
    echo "  - Weaviate: http://localhost:8080"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_env
    
    read -p "Do you want to proceed with deployment? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy
    else
        echo "Deployment cancelled."
        exit 0
    fi
}

main
