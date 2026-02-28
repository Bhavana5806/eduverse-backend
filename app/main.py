from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import eduverse_routes, ai_routes
import os

app = FastAPI(
    title="EduVerse AI - Global Intelligent Learning Ecosystem",
    description="""🌍 EduVerse AI: Complete 10-Engine Educational Intelligence Platform
    
    **10 Integrated Engines:**
    1. Student Intelligence & Assessment Engine
    2. Foundation Rebuilding Engine
    3. Hybrid Simulation Intelligence Engine
    4. Question Intelligence & Prediction Engine
    5. Competitive & Government Exam Engine
    6. College Mastery & Department Excellence Engine
    7. Career Intelligence & Global Demand Engine
    8. Multilingual & Accessibility Engine
    9. Industry Integration & Credibility Layer
    10. Explainability & Transparency Engine
    
    **Features:**
    - Adaptive Learning
    - Exam Prediction
    - Career Guidance
    - Multilingual Support (Tamil, Hindi, Malayalam, Telugu, Kannada, English)
    - Simulation-Based Learning
    - Mock Tests & Rank Estimation
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(eduverse_routes.router, prefix="/api/v1", tags=["EduVerse AI - All Engines"])
app.include_router(ai_routes.router, prefix="/api/v1", tags=["AI Content Generation"])

@app.get("/", tags=["Root"])
def root():
    return {
        "status": "EduVerse AI Backend Running Successfully",
        "version": "2.0.0",
        "platform": "Global Intelligent Learning Ecosystem",
        "engines": [
            "Student Intelligence & Assessment",
            "Foundation Rebuilding",
            "Hybrid Simulation Intelligence",
            "Question Intelligence & Prediction",
            "Competitive & Government Exam",
            "College Mastery",
            "Career Intelligence",
            "Multilingual & Accessibility",
            "Industry Integration",
            "Explainability & Transparency"
        ],
        "supported_languages": ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"],
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "docs": "/docs",
        "api_base": "/api/v1"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "EduVerse AI",
        "version": "2.0.0",
        "engines_active": 10
    }

@app.get("/api/v1/features", tags=["Features"])
def get_features():
    return {
        "assessment": "Adaptive testing with weakness detection",
        "foundation": "Micro-concept breakdown and rebuilding",
        "simulation": "Interactive experiential learning",
        "prediction": "Exam pattern analysis and question prediction",
        "mock_tests": "Competitive exam preparation with rank estimation",
        "career": "AI-powered career guidance and skill gap analysis",
        "multilingual": "6 languages with text-to-speech",
        "explainability": "Transparent AI decision explanations"
    }