# Deployment Guide

This guide covers deploying the AI Business Platform using various methods.

## Prerequisites

- Docker 24.0+
- Kubernetes 1.28+ (for K8s deployment)
- kubectl (for K8s deployment)
- Helm 3.12+ (optional, for advanced deployments)
- 4GB+ RAM available
- 20GB+ disk space

## Environment Variables

Create a `.env` file in the project root:

```bash
# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password

# API Keys (required for LLM features)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Deployment Methods

### 1. Docker Compose (Recommended for Local/Development)

The easiest way to get started:

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

**Access Points:**
- Application API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Kafka: localhost:9092
- Weaviate: http://localhost:8080

### 2. Docker (Standalone)

Build and run the application container:

```bash
# Build image
docker build -t ai-platform:latest .

# Run container
docker run -d \
  --name ai-platform \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  -e REDIS_URL=redis://host:6379 \
  ai-platform:latest

# View logs
docker logs -f ai-platform

# Stop container
docker stop ai-platform
docker rm ai-platform
```

### 3. Kubernetes Deployment

For production deployments with high availability:

#### Step 1: Create Namespace and Secrets

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Update secrets with your credentials
# Edit k8s/secrets.yaml with your actual credentials
kubectl apply -f k8s/secrets.yaml

# Apply ConfigMap
kubectl apply -f k8s/configmap.yaml
```

#### Step 2: Deploy Infrastructure Services

```bash
# Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Deploy Redis
kubectl apply -f k8s/redis.yaml

# Wait for services to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n ai-platform --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n ai-platform --timeout=300s
```

#### Step 3: Deploy Application

```bash
# Build and tag your Docker image
docker build -t your-registry/ai-platform:latest .
docker push your-registry/ai-platform:latest

# Update k8s/deployment.yaml with your image registry
# Then deploy
kubectl apply -f k8s/deployment.yaml

# Wait for deployment
kubectl wait --for=condition=available deployment/ai-platform-app -n ai-platform --timeout=300s
```

#### Step 4: Configure Ingress (Optional)

```bash
# Install NGINX Ingress Controller (if not already installed)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx

# Update k8s/ingress.yaml with your domain
kubectl apply -f k8s/ingress.yaml
```

#### Verify Deployment

```bash
# Check all resources
kubectl get all -n ai-platform

# Check pod status
kubectl get pods -n ai-platform

# View application logs
kubectl logs -l app=ai-platform -n ai-platform -f

# Port forward to access locally
kubectl port-forward -n ai-platform svc/ai-platform-service 8000:80
```

### 4. Cloud Deployments

#### AWS ECS/EKS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag ai-platform:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-platform:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-platform:latest

# Deploy to EKS using kubectl (cluster must be configured)
kubectl apply -f k8s/
```

#### Google Cloud (GKE)

```bash
# Build and push to GCR
gcloud auth configure-docker
docker tag ai-platform:latest gcr.io/<project-id>/ai-platform:latest
docker push gcr.io/<project-id>/ai-platform:latest

# Deploy to GKE
kubectl apply -f k8s/
```

#### Azure (AKS)

```bash
# Build and push to ACR
az acr login --name <registry-name>
docker tag ai-platform:latest <registry-name>.azurecr.io/ai-platform:latest
docker push <registry-name>.azurecr.io/ai-platform:latest

# Deploy to AKS
kubectl apply -f k8s/
```

## Scaling

### Horizontal Pod Autoscaling (HPA)

```bash
# Create HPA for application
kubectl autoscale deployment ai-platform-app \
  --namespace ai-platform \
  --cpu-percent=70 \
  --min=3 \
  --max=10

# Check HPA status
kubectl get hpa -n ai-platform
```

### Manual Scaling

```bash
# Scale application pods
kubectl scale deployment ai-platform-app --replicas=5 -n ai-platform

# Using docker-compose
docker-compose up -d --scale app=5
```

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# In Kubernetes
kubectl exec -it <pod-name> -n ai-platform -- curl localhost:8000/health
```

### Resource Usage

```bash
# Docker
docker stats

# Kubernetes
kubectl top pods -n ai-platform
kubectl top nodes
```

## Troubleshooting

### Common Issues

1. **Container fails to start**
   ```bash
   # Check logs
   docker logs ai-platform
   # or
   kubectl logs <pod-name> -n ai-platform
   ```

2. **Database connection errors**
   - Verify DATABASE_URL is correct
   - Check if PostgreSQL is running
   - Verify network connectivity

3. **Out of memory errors**
   - Increase container memory limits
   - Scale down replicas or reduce concurrent workers

4. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process or use different port
   ```

### Debug Commands

```bash
# Docker Compose
docker-compose logs -f app
docker-compose exec app bash

# Kubernetes
kubectl describe pod <pod-name> -n ai-platform
kubectl logs <pod-name> -n ai-platform --previous
kubectl exec -it <pod-name> -n ai-platform -- bash
```

## Backup and Recovery

### Database Backup

```bash
# Docker Compose
docker-compose exec postgres pg_dump -U admin ai_platform > backup.sql

# Kubernetes
kubectl exec -it postgres-0 -n ai-platform -- pg_dump -U admin ai_platform > backup.sql
```

### Restore Database

```bash
# Docker Compose
cat backup.sql | docker-compose exec -T postgres psql -U admin ai_platform

# Kubernetes
cat backup.sql | kubectl exec -i postgres-0 -n ai-platform -- psql -U admin ai_platform
```

## Security Considerations

1. **Change default passwords** in production
2. **Use secrets management** (HashiCorp Vault, AWS Secrets Manager)
3. **Enable TLS/SSL** for all communications
4. **Implement network policies** in Kubernetes
5. **Regular security updates** for base images
6. **Enable audit logging**
7. **Use non-root containers** (already configured)

## Performance Tuning

1. **Database Connection Pooling**: Adjust pool size based on load
2. **Redis Memory**: Configure maxmemory policy
3. **Worker Processes**: Set based on CPU cores
4. **Resource Limits**: Fine-tune CPU/memory limits
5. **Caching Strategy**: Implement appropriate caching layers

## Updates and Rollbacks

### Rolling Updates (Kubernetes)

```bash
# Update image
kubectl set image deployment/ai-platform-app ai-platform=ai-platform:v2 -n ai-platform

# Check rollout status
kubectl rollout status deployment/ai-platform-app -n ai-platform

# Rollback if needed
kubectl rollout undo deployment/ai-platform-app -n ai-platform
```

### Zero-Downtime Updates (Docker Compose)

```bash
# Build new version
docker-compose build

# Rolling update
docker-compose up -d --no-deps --scale app=6 app
docker-compose up -d --no-deps --scale app=3 app
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/Garrettc123/ai-business-platform/issues
- Documentation: See `/docs` directory

## License

MIT License - See LICENSE file for details
