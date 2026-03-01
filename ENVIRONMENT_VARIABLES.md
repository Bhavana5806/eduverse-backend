# EduVerse AI - Environment Variables

## Backend Environment Variables

### Required Variables

#### Database Configuration
```bash
DATABASE_URL=postgresql://user:password@host:port/database
# For Railway: Use the automatically provided DATABASE_URL
```

#### Security Configuration
```bash
SECRET_KEY=your-super-secret-key-here
# Generate with: openssl rand -base64 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

#### AI Services Configuration
```bash
GEMINI_API_KEY=your-gemini-api-key-here
# Get from: https://makersuite.google.com/app/apikey

YOUTUBE_API_KEY=your-youtube-data-api-key-here
# Get from: https://console.developers.google.com/apis/credentials

OPENAI_API_KEY=your-openai-api-key-here
# Get from: https://platform.openai.com/api-keys

ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
# Get from: https://elevenlabs.io/app/api
```

#### Video Generation Services
```bash
# For AI Video Generation
STABILITY_API_KEY=your-stability-ai-api-key-here
# Get from: https://platform.stability.ai/

RUNWAYML_API_KEY=your-runwayml-api-key-here
# Get from: https://runwayml.com/

# For Video Processing
FFMPEG_PATH=/usr/bin/ffmpeg
# Default: /usr/bin/ffmpeg (Linux), /usr/local/bin/ffmpeg (macOS)
```

#### Anti-Distraction Services
```bash
# For Browser Activity Monitoring
ACTIVITY_MONITOR_ENABLED=true
DISTRACTION_THRESHOLD=3
SESSION_LOCK_DURATION=600  # 10 minutes in seconds

# For Real-time Communication
WEBSOCKET_URL=wss://your-websocket-server.com
ACTIVITY_CHECK_INTERVAL=30000  # 30 seconds in milliseconds
```

#### Cloud Storage
```bash
# For Video and Content Storage
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=eduverse-ai-content

# Alternative: Google Cloud Storage
GOOGLE_CLOUD_STORAGE_BUCKET=eduverse-ai-content
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

#### Email and Notifications
```bash
# For Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# For Push Notifications
FCM_SERVER_KEY=your-firebase-cloud-messaging-server-key
# Get from: Firebase Console > Project Settings > Cloud Messaging
```

#### Analytics and Monitoring
```bash
# For Application Monitoring
SENTRY_DSN=your-sentry-dsn-here
# Get from: https://sentry.io/settings/[organization]/projects/[project]/keys/

# For Performance Monitoring
NEW_RELIC_LICENSE_KEY=your-new-relic-license-key
NEW_RELIC_APP_NAME=eduverse-ai-backend
```

### Optional Variables

#### Development Configuration
```bash
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### Performance Configuration
```bash
# Database Connection Pool
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379/0

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # 60 seconds
```

#### Feature Flags
```bash
# Feature Toggles
ENABLE_VIDEO_GENERATION=true
ENABLE_ANTI_DISTRACTION=true
ENABLE_MULTILINGUAL=true
ENABLE_SIMULATION=true
ENABLE_CAREER_GUIDANCE=true
```

## Frontend Environment Variables

### Required Variables

#### API Configuration
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
# For Production: https://your-backend-domain.com/api/v1
```

#### AI Services Configuration
```bash
NEXT_PUBLIC_GEMINI_API_KEY=your-gemini-api-key-here
NEXT_PUBLIC_YOUTUBE_API_KEY=your-youtube-data-api-key-here
```

#### Authentication
```bash
NEXT_PUBLIC_AUTH_DOMAIN=your-auth-domain.com
NEXT_PUBLIC_AUTH_CLIENT_ID=your-auth-client-id
```

### Optional Variables

#### Feature Configuration
```bash
NEXT_PUBLIC_ENABLE_VIDEO_PLAYER=true
NEXT_PUBLIC_ENABLE_ANTI_DISTRACTION=true
NEXT_PUBLIC_ENABLE_MULTILINGUAL=true
NEXT_PUBLIC_ENABLE_DARK_MODE=true
```

#### Analytics
```bash
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn-here
```

## Railway Deployment Variables

### Automatic Variables (Set by Railway)
```bash
# Database
DATABASE_URL=postgresql://...

# Application
PORT=8000
RAILWAY_ENVIRONMENT=production
RAILWAY_SERVICE_NAME=eduverse-backend
```

### Manual Variables (Set in Railway Dashboard)
```bash
# Security
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Services
GEMINI_API_KEY=your-production-gemini-key
YOUTUBE_API_KEY=your-production-youtube-key
OPENAI_API_KEY=your-production-openai-key
ELEVENLABS_API_KEY=your-production-elevenlabs-key

# Storage
AWS_ACCESS_KEY_ID=your-production-aws-key
AWS_SECRET_ACCESS_KEY=your-production-aws-secret
S3_BUCKET_NAME=eduverse-ai-production

# Monitoring
SENTRY_DSN=your-production-sentry-dsn
```

## Vercel Deployment Variables

### Frontend Variables (Set in Vercel Dashboard)
```bash
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com/api/v1
NEXT_PUBLIC_GEMINI_API_KEY=your-production-gemini-key
NEXT_PUBLIC_YOUTUBE_API_KEY=your-production-youtube-key
```

### Environment-Specific Variables

#### Development
```bash
# Use .env.development
DEBUG=true
LOG_LEVEL=DEBUG
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

#### Staging
```bash
# Use .env.staging
DEBUG=false
LOG_LEVEL=INFO
NEXT_PUBLIC_API_BASE_URL=https://staging-api.eduverse.ai/api/v1
```

#### Production
```bash
# Use .env.production
DEBUG=false
LOG_LEVEL=WARNING
NEXT_PUBLIC_API_BASE_URL=https://api.eduverse.ai/api/v1
```

## Security Notes

### Key Management
- Never commit `.env` files to version control
- Use different keys for different environments
- Rotate API keys regularly
- Use strong, unique secret keys

### Production Security
- Set `DEBUG=false` in production
- Use HTTPS for all API endpoints
- Implement proper CORS policies
- Enable rate limiting
- Monitor for suspicious activity

### Key Generation Commands

```bash
# Generate SECRET_KEY
openssl rand -base64 32

# Generate JWT Secret
openssl rand -hex 32

# Generate API Keys (for development)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check `DATABASE_URL` format
   - Verify database credentials
   - Ensure database is accessible

2. **API Key Errors**
   - Verify API keys are valid
   - Check API usage limits
   - Ensure proper permissions

3. **CORS Errors**
   - Check `CORS_ORIGINS` setting
   - Verify frontend URL matches
   - Check browser console for details

4. **Authentication Errors**
   - Verify `SECRET_KEY` matches between services
   - Check token expiration settings
   - Ensure proper JWT format

### Testing Environment Variables

```bash
# Test backend startup
python -c "from app.core.config import settings; print('Config loaded successfully')"

# Test API connectivity
curl -X GET "http://localhost:8000/health"

# Test frontend build
npm run build
```

## Next Steps

1. Set up all required environment variables in your deployment platform
2. Test the application in each environment
3. Monitor logs for any configuration issues
4. Implement proper key rotation procedures
5. Set up monitoring and alerting for critical services