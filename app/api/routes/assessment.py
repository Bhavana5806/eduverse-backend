from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models, schemas
from app.agents.assessment_agent import analyze_performance
from app.agents.adaptive_agent import generate_recommendation

router = APIRouter()

@router.post("/assess")
def assess_student(data: schemas.PerformanceCreate, db: Session = Depends(get_db)):

    performance = models.StudentPerformance(
        student_name=data.student_name,
        subject=data.subject,
        topic=data.topic,
        score=data.score,
        max_score=data.max_score
    )

    db.add(performance)
    db.commit()
    db.refresh(performance)

    percentage, status = analyze_performance(data.score, data.max_score)
    recommendation = generate_recommendation(status, percentage)

    return {
        "student_name": data.student_name,
        "subject": data.subject,
        "topic": data.topic,
        "percentage": percentage,
        "status": status,
        "recommendation": recommendation
    }

@router.get("/performance")
def get_all_performance(db: Session = Depends(get_db)):
    return db.query(models.StudentPerformance).all()