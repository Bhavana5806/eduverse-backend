from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import assessment
from app.api.routes import recommendation
import os

app = FastAPI(
    title="EduVerse AI Core Engine",
    description="Global Intelligent Learning, Simulation & Predictive Exam Ecosystem",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(assessment.router, prefix="/api/v1", tags=["Assessment"])
app.include_router(recommendation.router, prefix="/api/v1", tags=["Recommendation"])

@app.get("/")
def root():
    return {
        "status": "EduVerse AI Backend Running Successfully",
        "version": "1.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}