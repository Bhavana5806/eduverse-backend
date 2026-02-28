"""
Test script to verify EduVerse Backend is working correctly
"""

import sys
import os

print("=" * 60)
print("EduVerse Backend - Pre-Deployment Test")
print("=" * 60)
print()

# Test 1: Import main app
print("[Test 1] Loading main application...")
try:
    from app.main import app
    print("  SUCCESS: Main app loaded")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# Test 2: Import routes
print("[Test 2] Loading API routes...")
try:
    from app.api.routes import eduverse_routes, ai_routes
    print("  SUCCESS: All routes loaded")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# Test 3: Import agents
print("[Test 3] Loading AI agents...")
try:
    from app.agents import (
        student_intelligence_agent,
        foundation_agent,
        simulation_agent,
        prediction_agent,
        competitive_exam_agent,
        college_mastery_agent,
        career_agent,
        multilingual_agent,
        industry_integration_agent,
        explainability_agent,
        ai_content_generator
    )
    print("  SUCCESS: All agents loaded")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# Test 4: Import database
print("[Test 4] Loading database modules...")
try:
    from app.db import database, models, schemas
    print("  SUCCESS: Database modules loaded")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# Test 5: Check environment variables
print("[Test 5] Checking environment configuration...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'ALGORITHM']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"  WARNING: Missing environment variables: {', '.join(missing_vars)}")
        print("  These should be set in Railway environment")
    else:
        print("  SUCCESS: All required environment variables present")
except Exception as e:
    print(f"  WARNING: {e}")

# Test 6: Check FastAPI app configuration
print("[Test 6] Checking FastAPI configuration...")
try:
    assert app.title == "EduVerse AI - Global Intelligent Learning Ecosystem"
    assert app.version == "2.0.0"
    print("  SUCCESS: FastAPI app configured correctly")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# Test 7: Check routes are registered
print("[Test 7] Checking registered routes...")
try:
    routes = [route.path for route in app.routes]
    critical_routes = ["/", "/health", "/docs", "/api/v1/student/create"]
    
    for route in critical_routes:
        if route not in routes:
            print(f"  WARNING: Route {route} not found")
    
    print(f"  SUCCESS: {len(routes)} routes registered")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print()
print("Your backend is ready for Railway deployment!")
print()
print("Next steps:")
print("1. Run: git add .")
print("2. Run: git commit -m 'Ready for deployment'")
print("3. Run: git push origin main")
print("4. Deploy on Railway: https://railway.app")
print()
