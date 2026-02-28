# EduVerse AI Backend - Deployment Guide

## 🚀 Railway Deployment

### Prerequisites
- GitHub account
- Railway account (https://railway.app)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - EduVerse AI Backend"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python and deploy

### Step 3: Configure Environment Variables

In Railway Dashboard → Variables, add:

```
DATABASE_URL=<your-railway-postgres-url>
SECRET_KEY=<generate-strong-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Step 4: Add PostgreSQL Database

1. In Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Copy the DATABASE_URL from PostgreSQL service
4. Add it to your backend service variables

### Step 5: Generate Domain

1. Go to Settings in your backend service
2. Click "Generate Domain"
3. Your API will be live at: `https://your-app.up.railway.app`

## 🌐 Frontend Deployment (Vercel)

### Connect Backend to Frontend

In your Next.js `.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app/api/v1
```

Deploy to Vercel:
```bash
vercel --prod
```

## 📡 API Endpoints

- Health Check: `GET /health`
- Root: `GET /`
- Assessment: `POST /api/v1/assess`
- Performance: `GET /api/v1/performance`

## 🔒 Security Notes

- Never commit `.env` file
- Use strong SECRET_KEY in production
- Configure CORS properly for your frontend domain
- Enable HTTPS (Railway provides this automatically)

## 📊 Monitoring

Railway provides:
- Automatic logs
- Metrics dashboard
- Deployment history
- Rollback capability

## 🛠 Local Development

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📝 Notes

- Railway automatically sets PORT environment variable
- Database migrations run on startup
- Zero-downtime deployments
- Auto-scaling available
