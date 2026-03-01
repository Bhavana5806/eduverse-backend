"""
Enhanced Database Models for EduVerse AI - All 10 Engines
Comprehensive models supporting the complete autonomous agentic AI system
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum

# Enums for standardized data
class EducationLevel(str, enum.Enum):
    SCHOOL = "school"
    COLLEGE = "college"
    COMPETITIVE = "competitive"

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SimulationType(str, enum.Enum):
    VIRTUAL_LAB = "virtual_lab"
    MOTION_SIMULATOR = "motion_simulator"
    GRAPH_VISUALIZER = "graph_visualizer"
    DS_VISUALIZER = "ds_visualizer"
    CIRCUIT_BUILDER = "circuit_builder"
    NEURAL_NETWORK = "neural_network"
    INTERACTIVE_TUTORIAL = "interactive_tutorial"

class ExamType(str, enum.Enum):
    SCHOOL_BOARD = "school_board"
    UNIVERSITY = "university"
    COMPETITIVE = "competitive"
    GOVERNMENT = "government"
    PLACEMENT = "placement"

class Language(str, enum.Enum):
    ENGLISH = "English"
    TAMIL = "Tamil"
    HINDI = "Hindi"
    MALAYALAM = "Malayalam"
    TELUGU = "Telugu"
    KANNADA = "Kannada"

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    MENTOR = "mentor"

# ==================== CORE MODELS ====================

class User(Base):
    """Enhanced User Model with Role-Based Access"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    mentor_profile = relationship("Mentor", back_populates="user", uselist=False)

class Student(Base):
    """Enhanced Student Profile Model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), index=True)
    age = Column(Integer)
    education_level = Column(Enum(EducationLevel))
    language_preference = Column(Enum(Language), default=Language.ENGLISH)
    
    # School specific
    standard = Column(String(10), nullable=True)
    
    # College specific
    college_year = Column(Integer, nullable=True)
    department = Column(String(50), nullable=True)
    
    # Syllabus and content
    syllabus_image_url = Column(Text, nullable=True)
    syllabus_text = Column(Text, nullable=True)
    
    # Learning preferences
    learning_style = Column(String(50), default="visual")  # visual, auditory, kinesthetic
    accessibility_needs = Column(JSON, default={})
    
    # Performance tracking
    overall_performance = Column(Float, default=0.0)
    last_assessment_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    assessments = relationship("Assessment", back_populates="student")
    weakness_profiles = relationship("WeaknessProfile", back_populates="student")
    simulation_progress = relationship("SimulationProgress", back_populates="student")
    learning_paths = relationship("LearningPath", back_populates="student")
    career_profiles = relationship("CareerProfile", back_populates="student")
    mock_tests = relationship("MockTest", back_populates="student")
    content_interactions = relationship("ContentInteraction", back_populates="student")

class Mentor(Base):
    """Industry Mentor Model"""
    __tablename__ = "mentors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    email = Column(String(100))
    industry = Column(String(100))
    expertise = Column(JSON)  # List of expertise areas
    experience_years = Column(Integer)
    company = Column(String(100))
    linkedin_profile = Column(String(200), nullable=True)
    is_verified = Column(Boolean, default=False)
    availability_hours = Column(JSON, default={})  # {day: [time_slots]}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="mentor_profile")
    sessions = relationship("MentorSession", back_populates="mentor")

# ==================== ASSESSMENT & DIAGNOSTIC MODELS ====================

class Assessment(Base):
    """Enhanced Assessment Model with Detailed Analytics"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String(100))
    topic = Column(String(100))
    subtopic = Column(String(100), nullable=True)
    
    # Performance metrics
    score = Column(Float)
    max_score = Column(Float)
    percentage = Column(Float)
    time_taken = Column(Integer)  # in seconds
    accuracy = Column(Float)
    
    # Difficulty and complexity
    difficulty = Column(Enum(DifficultyLevel))
    complexity_level = Column(Integer)  # 1-10 scale
    question_count = Column(Integer)
    
    # Adaptive learning data
    previous_score = Column(Float, nullable=True)
    improvement_percentage = Column(Float, nullable=True)
    
    # Metadata
    assessment_type = Column(String(50))  # diagnostic, formative, summative
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="assessments")

class WeaknessProfile(Base):
    """Comprehensive Weakness Analysis Model"""
    __tablename__ = "weakness_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String(100))
    
    # Detailed weakness analysis
    weak_topics = Column(JSON)  # {topic: {score: float, priority: str, last_tested: datetime}}
    strength_topics = Column(JSON)  # {topic: {score: float, mastery: str}}
    priority_index = Column(JSON)  # {topic: priority_score}
    
    # Learning gaps
    conceptual_gaps = Column(JSON)  # {concept: description}
    procedural_gaps = Column(JSON)  # {procedure: description}
    
    # Progress tracking
    last_updated = Column(DateTime, default=datetime.utcnow)
    improvement_trend = Column(JSON, default=[])  # Array of {date: score}
    
    student = relationship("Student", back_populates="weakness_profiles")

class LearningPath(Base):
    """Personalized Learning Path Model"""
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String(100))
    current_level = Column(Enum(DifficultyLevel))
    target_level = Column(Enum(DifficultyLevel))
    
    # Path configuration
    milestones = Column(JSON)  # {milestone_id: {name, topics, estimated_time, status}}
    current_milestone = Column(Integer, default=1)
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    completed_topics = Column(JSON, default=[])  # Array of topic names
    estimated_completion = Column(DateTime, nullable=True)
    
    # Adaptive adjustments
    path_adjustments = Column(JSON, default=[])  # Array of {date, reason, adjustment}
    last_adjusted = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="learning_paths")

# ==================== SIMULATION & INTERACTIVE MODELS ====================

class SimulationModule(Base):
    """Simulation Module Catalog"""
    __tablename__ = "simulation_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    simulation_type = Column(Enum(SimulationType))
    subject = Column(String(100))
    topic = Column(String(100))
    
    # Configuration
    difficulty_levels = Column(JSON)  # {level: config}
    estimated_duration = Column(Integer)  # in minutes
    prerequisites = Column(JSON, default=[])  # Array of topic names
    
    # Content
    description = Column(Text)
    learning_objectives = Column(JSON)  # Array of objectives
    visual_assets = Column(JSON, default=[])  # Array of asset URLs
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SimulationProgress(Base):
    """Student Simulation Progress Tracking"""
    __tablename__ = "simulation_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    simulation_id = Column(Integer, ForeignKey("simulation_modules.id"))
    
    # Progress metrics
    mastery_score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    best_score = Column(Float, default=0.0)
    last_attempt_score = Column(Float, default=0.0)
    
    # Engagement metrics
    time_spent = Column(Integer, default=0)  # in seconds
    interactions_count = Column(Integer, default=0)
    guidance_used = Column(Integer, default=0)
    
    # Status
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("Student", back_populates="simulation_progress")
    simulation = relationship("SimulationModule")

class SimulationSession(Base):
    """Detailed Simulation Session Tracking"""
    __tablename__ = "simulation_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    simulation_id = Column(Integer, ForeignKey("simulation_modules.id"))
    
    # Session details
    session_start = Column(DateTime)
    session_end = Column(DateTime, nullable=True)
    duration = Column(Integer)  # in seconds
    
    # Performance during session
    actions_taken = Column(JSON)  # Array of {action, timestamp, result}
    decisions_made = Column(JSON)  # Array of {decision, correct, timestamp}
    hints_used = Column(Integer, default=0)
    
    # Learning outcomes
    concepts_understood = Column(JSON, default=[])  # Array of concept names
    skills_improved = Column(JSON, default=[])  # Array of skill names
    confidence_level = Column(Integer)  # 1-10 scale
    
    student = relationship("Student")
    simulation = relationship("SimulationModule")

# ==================== CONTENT & QUESTION MODELS ====================

class ContentRepository(Base):
    """AI-Generated Content Repository"""
    __tablename__ = "content_repository"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content_type = Column(String(50))  # video, text, interactive, simulation
    subject = Column(String(100))
    topic = Column(String(100))
    subtopic = Column(String(100), nullable=True)
    
    # Content details
    content_data = Column(JSON)  # URL, duration, size, etc.
    difficulty = Column(Enum(DifficultyLevel))
    estimated_time = Column(Integer)  # in minutes
    
    # Multilingual support
    translations = Column(JSON, default={})  # {language: content_url}
    audio_narrations = Column(JSON, default={})  # {language: audio_url}
    
    # Metadata
    created_by = Column(String(100))  # AI agent name
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)

class ExamDatabase(Base):
    """Historical Exam Question Database"""
    __tablename__ = "exam_database"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_type = Column(Enum(ExamType))
    subject = Column(String(100))
    year = Column(Integer)
    board_university = Column(String(100))
    
    # Question details
    question_text = Column(Text)
    question_type = Column(String(50))  # MCQ, short_answer, long_answer, numerical
    marks = Column(Integer)
    difficulty = Column(Enum(DifficultyLevel))
    
    # Topic mapping
    topic = Column(String(100))
    subtopic = Column(String(100), nullable=True)
    concept_tags = Column(JSON, default=[])  # Array of concept names
    
    # Answer and explanation
    correct_answer = Column(Text)
    explanation = Column(Text)
    solution_steps = Column(JSON, default=[])  # Array of steps
    
    # Metadata
    source = Column(String(200))  # Exam name, paper code
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionBank(Base):
    """Generated Question Bank for Practice"""
    __tablename__ = "question_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    exam_type = Column(Enum(ExamType))
    subject = Column(String(100))
    
    # Question generation
    generated_questions = Column(JSON)  # Array of question objects
    difficulty_distribution = Column(JSON)  # {difficulty: count}
    topic_coverage = Column(JSON)  # {topic: question_count}
    
    # Usage tracking
    generated_at = Column(DateTime, default=datetime.utcnow)
    used_count = Column(Integer, default=0)
    average_accuracy = Column(Float, default=0.0)
    
    student = relationship("Student")

# ==================== CAREER & INDUSTRY MODELS ====================

class CareerDatabase(Base):
    """Global Career and Job Market Database"""
    __tablename__ = "career_database"
    
    id = Column(Integer, primary_key=True, index=True)
    career_name = Column(String(100))
    industry = Column(String(100))
    job_role = Column(String(100))
    
    # Career details
    description = Column(Text)
    required_skills = Column(JSON)  # {skill: proficiency_level}
    education_requirements = Column(JSON)  # Array of required qualifications
    salary_range = Column(JSON)  # {min, max, currency}
    
    # Market data
    demand_level = Column(String(20))  # High, Medium, Low
    growth_rate = Column(Float)  # Annual growth percentage
    global_opportunities = Column(JSON, default=[])  # Array of countries
    
    # Future trends
    emerging_trends = Column(JSON, default=[])  # Array of trend descriptions
    technology_impact = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class CareerProfile(Base):
    """Student Career Intelligence Profile"""
    __tablename__ = "career_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    # Student assessment
    interests = Column(JSON)  # {interest: score}
    strengths = Column(JSON)  # {skill: proficiency}
    personality_traits = Column(JSON, default={})
    
    # Career matches
    recommended_careers = Column(JSON)  # {career_id: match_score}
    skill_gaps = Column(JSON)  # {skill: current_level, target_level}
    
    # Development plan
    certifications = Column(JSON, default=[])  # Array of certification objects
    learning_path = Column(JSON, default=[])  # Array of learning steps
    timeline = Column(JSON, default={})  # {phase: duration}
    
    # Progress tracking
    updated_at = Column(DateTime, default=datetime.utcnow)
    last_career_test = Column(DateTime, nullable=True)
    
    student = relationship("Student", back_populates="career_profiles")

class MentorSession(Base):
    """Mentor-Student Session Tracking"""
    __tablename__ = "mentor_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    # Session details
    session_date = Column(DateTime)
    session_duration = Column(Integer)  # in minutes
    session_type = Column(String(50))  # career_guidance, skill_review, project_mentoring
    
    # Topics covered
    topics_discussed = Column(JSON)  # Array of topic names
    career_advice = Column(Text)
    skill_assessment = Column(JSON, default={})  # {skill: feedback}
    
    # Follow-up
    action_items = Column(JSON, default=[])  # Array of actionable items
    next_session_scheduled = Column(DateTime, nullable=True)
    
    mentor = relationship("Mentor", back_populates="sessions")
    student = relationship("Student")

# ==================== ANALYTICS & REPORTING MODELS ====================

class ProgressAnalytics(Base):
    """Comprehensive Progress Analytics"""
    __tablename__ = "progress_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    # Performance metrics
    weekly_progress = Column(JSON)  # {week: {topics_covered, assessments_taken, avg_score}}
    monthly_improvement = Column(JSON)  # {month: improvement_percentage}
    subject_wise_performance = Column(JSON)  # {subject: {avg_score, topics_mastered}}
    
    # Learning efficiency
    time_efficiency = Column(JSON)  # {topic: {time_spent, retention_score}}
    engagement_metrics = Column(JSON)  # {metric: value}
    
    # Predictive analytics
    predicted_performance = Column(JSON)  # {exam: {predicted_score, confidence}}
    risk_factors = Column(JSON, default=[])  # Array of potential issues
    
    # Report generation
    last_report_generated = Column(DateTime, nullable=True)
    report_frequency = Column(String(20), default="weekly")  # daily, weekly, monthly
    
    student = relationship("Student")

class ContentInteraction(Base):
    """Detailed Content Interaction Tracking"""
    __tablename__ = "content_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    content_id = Column(Integer, ForeignKey("content_repository.id"))
    
    # Interaction details
    interaction_type = Column(String(50))  # view, complete, rate, share
    interaction_time = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, default=0)  # in seconds
    
    # Engagement metrics
    completion_status = Column(String(20))  # started, in_progress, completed
    interaction_depth = Column(Integer, default=0)  # pages viewed, sections completed
    rating = Column(Integer, nullable=True)  # 1-5 scale
    
    # Learning outcomes
    concepts_learned = Column(JSON, default=[])  # Array of concept names
    retention_score = Column(Float, default=0.0)
    
    student = relationship("Student", back_populates="content_interactions")
    content = relationship("ContentRepository")

class SystemMetrics(Base):
    """System-wide Performance and Usage Metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(String(50))  # user_engagement, content_usage, system_performance
    metric_name = Column(String(100))
    metric_value = Column(JSON)  # {value, unit, timestamp}
    
    # Context
    time_period = Column(DateTime)
    user_segment = Column(String(50), nullable=True)  # new_users, returning, premium
    geographic_data = Column(JSON, default={})  # {region: count}
    
    created_at = Column(DateTime, default=datetime.utcnow)

# ==================== CONFIGURATION MODELS ====================

class SystemConfiguration(Base):
    """System-wide Configuration Settings"""
    __tablename__ = "system_configuration"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True)
    config_value = Column(JSON)
    config_type = Column(String(50))  # feature_flag, threshold, setting
    description = Column(Text)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_modified = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(100))

class Notification(Base):
    """User Notification System"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    notification_type = Column(String(50))  # achievement, reminder, update, alert
    title = Column(String(200))
    message = Column(Text)
    
    # Delivery
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    priority = Column(String(20))  # low, medium, high, urgent
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    user = relationship("User")


class LearningSession(Base):
    """Learning session with anti-distraction features"""
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content_repository.id"), nullable=True)
    session_type = Column(String(50), default="video")  # video, assessment, simulation
    session_key = Column(String(100), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    session_state = Column(String(50), default="active")  # active, paused, locked, completed
    focus_score = Column(Float, default=1.0)
    distractions_count = Column(Integer, default=0)
    locked_until = Column(DateTime)
    session_duration = Column(Integer)  # in seconds
    efficiency_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="learning_sessions")
    content = relationship("ContentRepository", back_populates="video_sessions")
    distractions = relationship("DistractionEvent", back_populates="session")


class DistractionEvent(Base):
    """Records of distractions during learning sessions"""
    __tablename__ = "distraction_events"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    distraction_type = Column(String(50), nullable=False)  # tab_switch, window_focus_loss, ai_tool_usage, etc.
    severity = Column(String(20), default="medium")  # low, medium, high
    message = Column(String(500))
    action_taken = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    session_duration_at_event = Column(Integer)  # session duration in seconds when event occurred
    
    # Relationships
    session = relationship("LearningSession", back_populates="distractions")
    student = relationship("Student", back_populates="distractions")
