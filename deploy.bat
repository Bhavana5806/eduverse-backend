@echo off
echo.
echo ========================================
echo   EduVerse AI - Railway Deployment
echo ========================================
echo.
echo Step 1: Initialize Git
echo ------------------------
echo git init
echo git add .
echo git commit -m "Initial commit - EduVerse AI Backend"
echo.
echo Step 2: Push to GitHub
echo ------------------------
echo git remote add origin YOUR_GITHUB_REPO_URL
echo git branch -M main
echo git push -u origin main
echo.
echo Step 3: Railway Deployment
echo ------------------------
echo 1. Visit: https://railway.app
echo 2. New Project ^> Deploy from GitHub
echo 3. Select your repository
echo.
echo Step 4: Add PostgreSQL
echo ------------------------
echo New ^> Database ^> PostgreSQL
echo.
echo Step 5: Set Environment Variables
echo ------------------------
echo DATABASE_URL=your_postgres_url
echo SECRET_KEY=your_secret_key
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=60
echo.
echo Step 6: Generate Domain
echo ------------------------
echo Settings ^> Generate Domain
echo.
echo Done! Your API will be live.
echo.
pause
