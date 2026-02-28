from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.agents import ai_content_generator
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SyllabusRequest(BaseModel):
    syllabus: List[str]
    level: str
    language: str = "English"

class TopicRequest(BaseModel):
    topic: str
    level: str
    language: str = "English"

@router.post("/ai/generate-lecture")
def generate_lecture(request: TopicRequest):
    """AI generates complete lecture content"""
    result = ai_content_generator.generate_lecture_content(
        request.topic, request.level, request.language
    )
    return result

@router.post("/ai/generate-notes")
def generate_notes(request: TopicRequest):
    """AI generates study notes"""
    result = ai_content_generator.generate_study_notes(request.topic, request.level)
    return result

@router.post("/ai/generate-questions")
def generate_questions(topic: str, difficulty: str, count: int = 10):
    """AI generates assessment questions"""
    result = ai_content_generator.generate_questions(topic, difficulty, count)
    return result

@router.post("/ai/generate-simulation")
def generate_simulation(topic: str, subject: str):
    """AI generates simulation design"""
    result = ai_content_generator.generate_simulation_description(topic, subject)
    return result

@router.post("/ai/generate-syllabus-content")
def generate_syllabus_content(request: SyllabusRequest):
    """AI generates complete content for entire syllabus - FULLY AUTONOMOUS"""
    result = ai_content_generator.generate_complete_syllabus_content(
        request.syllabus, request.level
    )
    return result

@router.post("/ai/autonomous-learning-path")
def create_autonomous_path(student_id: int, syllabus: List[str]):
    """AI creates complete autonomous learning path"""
    student_profile = {"weak_topics": [], "strong_topics": []}  # Get from DB
    result = ai_content_generator.autonomous_learning_path(student_profile, syllabus)
    return result

@router.post("/ai/generate-video-script")
def generate_video_script(topic: str, duration: int = 10):
    """AI generates video lecture script"""
    result = ai_content_generator.generate_video_script(topic, duration)
    return result

# ============ PLACEMENT & GOVERNMENT EXAMS ============

from app.agents import placement_govt_exam_agent

@router.post("/placement/generate-roadmap")
def generate_placement_roadmap(student_id: int, target_domain: str, db: Session = Depends(get_db)):
    """Generate Industry 4.0 placement roadmap"""
    student_profile = {"skills": []}  # Get from DB
    result = placement_govt_exam_agent.generate_placement_roadmap(student_profile, target_domain)
    return result

@router.post("/govt-exam/generate-strategy")
def generate_govt_exam_strategy(exam_name: str, student_id: int, db: Session = Depends(get_db)):
    """Generate government exam preparation strategy"""
    student_profile = {}  # Get from DB
    result = placement_govt_exam_agent.generate_govt_exam_strategy(exam_name, student_profile)
    return result

@router.get("/govt-exam/all-exams")
def get_all_exams():
    """Get all supported government exams"""
    return placement_govt_exam_agent.get_all_exam_options()

@router.get("/placement/industry-domains")
def get_industry_domains():
    """Get all Industry 4.0 domains"""
    return placement_govt_exam_agent.get_industry_4_0_domains()

@router.post("/dual-prep/generate-plan")
def generate_dual_prep_plan(placement_domain: str, govt_exam: str):
    """Prepare for BOTH placement AND government exam"""
    return placement_govt_exam_agent.generate_dual_preparation_plan(placement_domain, govt_exam)
