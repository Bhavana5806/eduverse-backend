#!/bin/bash

echo "🚀 EduVerse Backend - Railway Deployment Script"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Initializing..."
    git init
    git branch -M main
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
read -p "Enter commit message (default: 'Deploy to Railway'): " commit_msg
commit_msg=${commit_msg:-"Deploy to Railway"}
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "🔗 No remote found."
    read -p "Enter your GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://railway.app"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select your repository"
echo "4. Add PostgreSQL database"
echo "5. Set environment variables:"
echo "   - DATABASE_URL (from PostgreSQL service)"
echo "   - SECRET_KEY (generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "   - ALGORITHM=HS256"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES=60"
echo "   - GEMINI_API_KEY (your Google Gemini API key)"
echo "6. Generate domain in Settings"
echo ""
echo "🎉 Your API will be live at: https://your-app.up.railway.app"
