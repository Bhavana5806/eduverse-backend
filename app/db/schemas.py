from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# Student Schemas
class StudentCreate(BaseModel):
    name: str
    email: str
    language: str = "English"
    education_level: str

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    language: str
    education_level: str

# Assessment Schemas
class AssessmentCreate(BaseModel):
    student_id: int
    subject: str
    topic: str
    score: float
    max_score: float
    time_taken: int
    difficulty: str

class AssessmentResponse(BaseModel):
    percentage: float
    status: str
    weakness_detected: bool
    recommendation: str

# Weakness Analysis
class WeaknessAnalysis(BaseModel):
    student_id: int
    subject: str
    weak_topics: List[str]
    strength_topics: List[str]
    priority_learning: List[Dict]

# Simulation Schemas
class SimulationRequest(BaseModel):
    student_id: int
    simulation_type: str
    topic: str
    difficulty: str

class SimulationResponse(BaseModel):
    simulation_id: int
    parameters: Dict
    guidance_level: str
    language: str

# Exam Prediction
class ExamPredictionRequest(BaseModel):
    exam_type: str
    subject: str
    student_weaknesses: List[str]

class ExamPredictionResponse(BaseModel):
    high_probability_topics: List[Dict]
    priority_questions: List[str]
    weightage_distribution: Dict
    study_strategy: str

# Mock Test
class MockTestCreate(BaseModel):
    student_id: int
    exam_type: str
    answers: List[Dict]

class MockTestResponse(BaseModel):
    score: float
    accuracy: float
    speed_score: float
    rank_estimate: int
    weak_areas: List[str]
    improvement_tips: List[str]

# Career Intelligence
class CareerAnalysisRequest(BaseModel):
    student_id: int
    interests: List[str]
    strengths: List[str]

class CareerAnalysisResponse(BaseModel):
    recommended_careers: List[Dict]
    skill_gaps: List[str]
    certifications: List[str]
    learning_path: List[str]

# Foundation Rebuilding
class FoundationRequest(BaseModel):
    student_id: int
    subject: str
    weak_topic: str

class FoundationResponse(BaseModel):
    micro_concepts: List[str]
    explanations: List[Dict]
    practice_problems: List[Dict]
    visual_aids: List[str]

# Multilingual
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    audio_url: Optional[str]