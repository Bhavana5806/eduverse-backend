# EduVerse AI - Deployment Guide

## 🚀 Quick Start Deployment

This guide provides comprehensive instructions for deploying the EduVerse AI system in various environments.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 12+ or SQLite (for development)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 10GB free space minimum

### Required Software
```bash
# Python 3.10+
python --version

# pip package manager
pip --version

# Git for version control
git --version
```

## 🏗️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/eduverse-backend.git
cd eduverse-backend
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/eduverse
# For SQLite (development): sqlite:///./eduverse.db

# Authentication
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Services
GOOGLE_API_KEY=your-google-generative-ai-api-key

# Application
ENVIRONMENT=development
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (for caching, optional)
REDIS_URL=redis://localhost:6379/0

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 5. Database Setup

#### For PostgreSQL
```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Windows: Download from https://www.postgresql.org/download/windows/

# Create database and user
sudo -u postgres createdb eduverse
sudo -u postgres createuser --interactive eduverse_user

# Grant privileges
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE eduverse TO eduverse_user;
\q
```

#### For SQLite (Development Only)
No additional setup required. The database will be created automatically.

### 6. Run Database Migrations
```bash
# Initialize database
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Or use Alembic for migrations (if configured)
alembic upgrade head
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and Run Services**
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

2. **Docker Compose Configuration**
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/eduverse
      - SECRET_KEY=your-secret-key
      - GOOGLE_API_KEY=your-google-api-key
    volumes:
      - ./app:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: eduverse
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
```

### Single Container Deployment
```bash
# Build image
docker build -t eduverse-api .

# Run container
docker run -d \
  --name eduverse-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host:5432/eduverse \
  -e SECRET_KEY=your-secret-key \
  eduverse-api
```

## ☸️ Kubernetes Deployment

### 1. Create Kubernetes Manifests

#### Namespace and ConfigMap
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: eduverse

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: eduverse-config
  namespace: eduverse
data:
  environment: "production"
  debug: "false"
  allowed_hosts: "your-domain.com"
```

#### Secrets
```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: eduverse-secrets
  namespace: eduverse
type: Opaque
data:
  database-url: <base64-encoded-database-url>
  secret-key: <base64-encoded-secret-key>
  google-api-key: <base64-encoded-google-api-key>
```

#### Deployment and Service
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eduverse-api
  namespace: eduverse
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eduverse-api
  template:
    metadata:
      labels:
        app: eduverse-api
    spec:
      containers:
      - name: eduverse-api
        image: eduverse/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: eduverse-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: eduverse-secrets
              key: secret-key
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: eduverse-secrets
              key: google-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: eduverse-api-service
  namespace: eduverse
spec:
  selector:
    app: eduverse-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 2. Deploy to Kubernetes
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n eduverse
kubectl get services -n eduverse

# View logs
kubectl logs -f deployment/eduverse-api -n eduverse
```

## ☁️ Cloud Deployment

### AWS Deployment

#### Using AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
eb init eduverse-api --platform python --region us-east-1

# Create environment
eb create prod-env --instance-type t3.medium --scale 3

# Deploy
eb deploy
```

#### Using AWS ECS/Fargate
```yaml
# task-definition.json
{
  "family": "eduverse-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "eduverse-api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/eduverse-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ]
    }
  ]
}
```

### Google Cloud Platform

#### Using Google Cloud Run
```bash
# Build and push container
gcloud builds submit --tag gcr.io/your-project/eduverse-api

# Deploy to Cloud Run
gcloud run deploy eduverse-api \
  --image gcr.io/your-project/eduverse-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Using Google Kubernetes Engine
```bash
# Create GKE cluster
gcloud container clusters create eduverse-cluster \
  --num-nodes 3 \
  --zone us-central1-a

# Deploy application
kubectl apply -f k8s/
```

### Azure Deployment

#### Using Azure Container Instances
```bash
# Create resource group
az group create --name eduverse-rg --location eastus

# Create container instance
az container create \
  --resource-group eduverse-rg \
  --name eduverse-api \
  --image your-registry/eduverse-api:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000
```

## 🔒 SSL/TLS Configuration

### Using Let's Encrypt with Nginx
```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Automated SSL with Certbot
```bash
# Install Certbot
sudo apt-get install certbot

# Obtain certificate
sudo certbot certonly --standalone -d your-domain.com

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## 📊 Monitoring and Logging

### Application Monitoring
```python
# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

# Add metrics endpoint
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)
```

### Log Aggregation
```yaml
# docker-compose.yml additions
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  fluentd:
    image: fluent/fluentd:v1.14-debian-1
    volumes:
      - ./fluentd.conf:/fluentd/etc/fluent.conf
    ports:
      - "24224:24224"
```

### Health Checks
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0"
    }
```

## 🔧 Configuration Management

### Environment-Specific Configs
```python
# config/development.py
DEBUG = True
DATABASE_URL = "sqlite:///./dev.db"
LOG_LEVEL = "DEBUG"

# config/production.py
DEBUG = False
DATABASE_URL = "postgresql://prod-db-url"
LOG_LEVEL = "INFO"
```

### Feature Flags
```python
# config/feature_flags.py
FEATURE_FLAGS = {
    "ai_content_generation": True,
    "simulation_engine": True,
    "multilingual_support": True,
    "autonomous_agents": True
}
```

## 🧪 Testing in Production

### Staging Environment
```bash
# Create staging deployment
kubectl apply -f k8s/staging/

# Run integration tests
pytest tests/integration/ --env staging
```

### Blue-Green Deployment
```yaml
# k8s/blue-green.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: eduverse-api
spec:
  strategy:
    blueGreen:
      activeService: eduverse-api-active
      previewService: eduverse-api-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
  template:
    spec:
      containers:
      - name: eduverse-api
        image: eduverse/api:v2.0.0
```

## 📈 Performance Optimization

### Database Optimization
```sql
-- Create indexes for frequently queried fields
CREATE INDEX idx_assessments_student_id ON assessments(student_id);
CREATE INDEX idx_assessments_topic ON assessments(topic);
CREATE INDEX idx_simulations_student_id ON simulation_progress(student_id);
```

### Caching Strategy
```python
# Redis caching
from redis import Redis
from functools import lru_cache

redis_client = Redis(host='redis', port=6379, db=0)

@lru_cache(maxsize=128)
def get_cached_data(key):
    return redis_client.get(key)
```

### CDN Configuration
```nginx
# Serve static files via CDN
location /static/ {
    proxy_pass https://cdn.your-domain.com/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database connectivity
psql -h localhost -U username -d database_name

# Verify connection string format
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Port Binding Issues
```bash
# Check if port is in use
sudo lsof -i :8000

# Kill conflicting process
sudo kill -9 <PID>
```

#### Docker Issues
```bash
# Check container logs
docker logs <container_id>

# Restart container
docker restart <container_id>

# Rebuild image
docker build --no-cache -t eduverse-api .
```

### Performance Issues

#### High Memory Usage
```bash
# Monitor memory usage
docker stats

# Adjust memory limits
docker run --memory=1g eduverse-api
```

#### Slow Database Queries
```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- Analyze slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC;
```

## 📞 Support and Maintenance

### Regular Maintenance Tasks
```bash
# Database backups
pg_dump -h localhost -U username database_name > backup.sql

# Log rotation
sudo logrotate /etc/logrotate.d/eduverse

# Security updates
sudo apt-get update && sudo apt-get upgrade
```

### Monitoring Commands
```bash
# Check application health
curl https://your-domain.com/health

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-domain.com/api/v1/system/health

# Check error rates
kubectl logs deployment/eduverse-api -n eduverse | grep ERROR
```

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database created and migrated
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Monitoring and alerting set up
- [ ] Backup procedures established
- [ ] Load testing completed
- [ ] Security scanning performed
- [ ] Documentation updated
- [ ] Team trained on operations

## 🎯 Next Steps

1. **Frontend Integration**: Connect to your React/Next.js frontend
2. **CI/CD Pipeline**: Set up automated deployment workflows
3. **Monitoring**: Implement comprehensive monitoring and alerting
4. **Scaling**: Configure auto-scaling based on load
5. **Security**: Perform security audits and penetration testing

---

**For additional support, please refer to:**
- [API Documentation](API_DOCUMENTATION.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [GitHub Issues](https://github.com/your-org/eduverse-backend/issues)

**Last Updated**: January 2024