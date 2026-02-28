from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from datetime import datetime
from app.db.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    language = Column(String, default="English")
    education_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String)
    topic = Column(String)
    score = Column(Float)
    max_score = Column(Float)
    time_taken = Column(Integer)
    difficulty = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class WeaknessProfile(Base):
    __tablename__ = "weakness_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String)
    weak_topics = Column(JSON)
    strength_topics = Column(JSON)
    priority_index = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow)

class SimulationProgress(Base):
    __tablename__ = "simulation_progress"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    simulation_type = Column(String)
    topic = Column(String)
    mastery_score = Column(Float)
    attempts = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExamPrediction(Base):
    __tablename__ = "exam_predictions"
    id = Column(Integer, primary_key=True, index=True)
    exam_type = Column(String)
    subject = Column(String)
    high_probability_topics = Column(JSON)
    question_patterns = Column(JSON)
    weightage_distribution = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class MockTest(Base):
    __tablename__ = "mock_tests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    exam_type = Column(String)
    score = Column(Float)
    accuracy = Column(Float)
    speed_score = Column(Float)
    rank_estimate = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class CareerProfile(Base):
    __tablename__ = "career_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    interests = Column(JSON)
    strengths = Column(JSON)
    recommended_careers = Column(JSON)
    skill_gaps = Column(JSON)
    certifications = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow)

class LearningPath(Base):
    __tablename__ = "learning_paths"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String)
    current_level = Column(String)
    target_level = Column(String)
    milestones = Column(JSON)
    progress_percentage = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)