@echo off
echo ========================================
echo EduVerse Backend - Railway Deployment
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Git not initialized. Initializing...
    git init
    git branch -M main
)

REM Add all files
echo Adding files to git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (default: Deploy to Railway): "
if "%commit_msg%"=="" set commit_msg=Deploy to Railway
git commit -m "%commit_msg%"

REM Check if remote exists
git remote | findstr origin >nul
if errorlevel 1 (
    echo No remote found.
    set /p repo_url="Enter your GitHub repository URL: "
    git remote add origin %repo_url%
)

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo SUCCESS: Code pushed to GitHub!
echo ========================================
echo.
echo Next Steps:
echo 1. Go to https://railway.app
echo 2. Click 'New Project' - 'Deploy from GitHub repo'
echo 3. Select your repository
echo 4. Add PostgreSQL database
echo 5. Set environment variables in Railway:
echo    - DATABASE_URL (from PostgreSQL service)
echo    - SECRET_KEY (generate new one)
echo    - ALGORITHM=HS256
echo    - ACCESS_TOKEN_EXPIRE_MINUTES=60
echo    - GEMINI_API_KEY (your Google Gemini API key)
echo 6. Generate domain in Settings
echo.
echo Your API will be live at: https://your-app.up.railway.app
echo.
pause
