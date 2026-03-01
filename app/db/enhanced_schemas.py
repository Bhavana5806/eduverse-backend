"""
Enhanced Pydantic Schemas for EduVerse AI - All 10 Engines
Comprehensive data validation and serialization schemas
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum as PyEnum
from typing_extensions import Annotated

# Enums for API validation
class EducationLevel(str, PyEnum):
    SCHOOL = "school"
    COLLEGE = "college"
    COMPETITIVE = "competitive"

class DifficultyLevel(str, PyEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SimulationType(str, PyEnum):
    VIRTUAL_LAB = "virtual_lab"
    MOTION_SIMULATOR = "motion_simulator"
    GRAPH_VISUALIZER = "graph_visualizer"
    DS_VISUALIZER = "ds_visualizer"
    CIRCUIT_BUILDER = "circuit_builder"
    NEURAL_NETWORK = "neural_network"
    INTERACTIVE_TUTORIAL = "interactive_tutorial"

class ExamType(str, PyEnum):
    SCHOOL_BOARD = "school_board"
    UNIVERSITY = "university"
    COMPETITIVE = "competitive"
    GOVERNMENT = "government"
    PLACEMENT = "placement"

class Language(str, PyEnum):
    ENGLISH = "English"
    TAMIL = "Tamil"
    HINDI = "Hindi"
    MALAYALAM = "Malayalam"
    TELUGU = "Telugu"
    KANNADA = "Kannada"

class UserRole(str, PyEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    MENTOR = "mentor"

class NotificationType(str, PyEnum):
    ACHIEVEMENT = "achievement"
    REMINDER = "reminder"
    UPDATE = "update"
    ALERT = "alert"

# ==================== CORE SCHEMAS ====================

class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    age: int
    education_level: EducationLevel
    language_preference: Language = Language.ENGLISH
    learning_style: str = "visual"
    accessibility_needs: Dict[str, Any] = {}

class StudentCreate(StudentBase):
    standard: Optional[str] = None
    college_year: Optional[int] = None
    department: Optional[str] = None
    syllabus_image_url: Optional[str] = None
    syllabus_text: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    user_id: int
    overall_performance: float
    last_assessment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MentorBase(BaseModel):
    name: str
    email: str
    industry: str
    expertise: List[str]
    experience_years: int
    company: str
    linkedin_profile: Optional[str] = None

class MentorCreate(MentorBase):
    availability_hours: Dict[str, List[str]] = {}

class MentorResponse(MentorBase):
    id: int
    user_id: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== ASSESSMENT SCHEMAS ====================

class AssessmentBase(BaseModel):
    student_id: int
    subject: str
    topic: str
    subtopic: Optional[str] = None
    score: float
    max_score: float
    time_taken: int
    difficulty: DifficultyLevel
    complexity_level: int
    question_count: int
    assessment_type: str

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    id: int
    percentage: float
    accuracy: float
    previous_score: Optional[float] = None
    improvement_percentage: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WeaknessProfileBase(BaseModel):
    student_id: int
    subject: str
    weak_topics: Dict[str, Dict[str, Any]]
    strength_topics: Dict[str, Dict[str, Any]]
    priority_index: Dict[str, float]
    conceptual_gaps: Dict[str, str]
    procedural_gaps: Dict[str, str]

class WeaknessProfileCreate(WeaknessProfileBase):
    pass

class WeaknessProfileResponse(WeaknessProfileBase):
    id: int
    last_updated: datetime
    improvement_trend: List[Dict[str, Any]]

    class Config:
        from_attributes = True

class LearningPathBase(BaseModel):
    student_id: int
    subject: str
    current_level: DifficultyLevel
    target_level: DifficultyLevel
    milestones: Dict[str, Dict[str, Any]]
    current_milestone: int
    progress_percentage: float
    completed_topics: List[str]
    estimated_completion: Optional[datetime] = None

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathResponse(LearningPathBase):
    id: int
    path_adjustments: List[Dict[str, Any]]
    last_adjusted: datetime

    class Config:
        from_attributes = True

# ==================== SIMULATION SCHEMAS ====================

class SimulationModuleBase(BaseModel):
    name: str
    simulation_type: SimulationType
    subject: str
    topic: str
    difficulty_levels: Dict[str, Dict[str, Any]]
    estimated_duration: int
    prerequisites: List[str]
    description: str
    learning_objectives: List[str]
    visual_assets: List[str]

class SimulationModuleCreate(SimulationModuleBase):
    pass

class SimulationModuleResponse(SimulationModuleBase):
    id: int
    is_active: bool
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True

class SimulationProgressBase(BaseModel):
    student_id: int
    simulation_id: int
    mastery_score: float
    attempts: int
    best_score: float
    last_attempt_score: float
    time_spent: int
    interactions_count: int
    guidance_used: int
    completed: bool

class SimulationProgressCreate(SimulationProgressBase):
    pass

class SimulationProgressResponse(SimulationProgressBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SimulationSessionBase(BaseModel):
    student_id: int
    simulation_id: int
    session_start: datetime
    session_end: Optional[datetime] = None
    duration: int
    actions_taken: List[Dict[str, Any]]
    decisions_made: List[Dict[str, Any]]
    hints_used: int
    concepts_understood: List[str]
    skills_improved: List[str]
    confidence_level: int

class SimulationSessionCreate(SimulationSessionBase):
    pass

class SimulationSessionResponse(SimulationSessionBase):
    id: int

    class Config:
        from_attributes = True

# ==================== CONTENT & QUESTION SCHEMAS ====================

class ContentRepositoryBase(BaseModel):
    title: str
    content_type: str
    subject: str
    topic: str
    subtopic: Optional[str] = None
    content_data: Dict[str, Any]
    difficulty: DifficultyLevel
    estimated_time: int
    translations: Dict[str, str]
    audio_narrations: Dict[str, str]
    created_by: str
    views_count: int
    rating: float

class ContentRepositoryCreate(ContentRepositoryBase):
    pass

class ContentRepositoryResponse(ContentRepositoryBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ExamDatabaseBase(BaseModel):
    exam_type: ExamType
    subject: str
    year: int
    board_university: str
    question_text: str
    question_type: str
    marks: int
    difficulty: DifficultyLevel
    topic: str
    subtopic: Optional[str] = None
    concept_tags: List[str]
    correct_answer: str
    explanation: str
    solution_steps: List[str]
    source: str

class ExamDatabaseCreate(ExamDatabaseBase):
    pass

class ExamDatabaseResponse(ExamDatabaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class QuestionBankBase(BaseModel):
    student_id: Optional[int] = None
    exam_type: ExamType
    subject: str
    generated_questions: List[Dict[str, Any]]
    difficulty_distribution: Dict[str, int]
    topic_coverage: Dict[str, int]
    used_count: int
    average_accuracy: float

class QuestionBankCreate(QuestionBankBase):
    pass

class QuestionBankResponse(QuestionBankBase):
    id: int
    generated_at: datetime

    class Config:
        from_attributes = True

# ==================== CAREER & INDUSTRY SCHEMAS ====================

class CareerDatabaseBase(BaseModel):
    career_name: str
    industry: str
    job_role: str
    description: str
    required_skills: Dict[str, str]
    education_requirements: List[str]
    salary_range: Dict[str, Any]
    demand_level: str
    growth_rate: float
    global_opportunities: List[str]
    emerging_trends: List[str]
    technology_impact: str

class CareerDatabaseCreate(CareerDatabaseBase):
    pass

class CareerDatabaseResponse(CareerDatabaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CareerProfileBase(BaseModel):
    student_id: int
    interests: Dict[str, float]
    strengths: Dict[str, str]
    personality_traits: Dict[str, Any]
    recommended_careers: Dict[str, float]
    skill_gaps: Dict[str, Dict[str, str]]
    certifications: List[Dict[str, Any]]
    learning_path: List[Dict[str, Any]]
    timeline: Dict[str, Any]

class CareerProfileCreate(CareerProfileBase):
    pass

class CareerProfileResponse(CareerProfileBase):
    id: int
    updated_at: datetime
    last_career_test: Optional[datetime] = None

    class Config:
        from_attributes = True

class MentorSessionBase(BaseModel):
    mentor_id: int
    student_id: int
    session_date: datetime
    session_duration: int
    session_type: str
    topics_discussed: List[str]
    career_advice: str
    skill_assessment: Dict[str, str]
    action_items: List[Dict[str, Any]]
    next_session_scheduled: Optional[datetime] = None

class MentorSessionCreate(MentorSessionBase):
    pass

class MentorSessionResponse(MentorSessionBase):
    id: int

    class Config:
        from_attributes = True

# ==================== ANALYTICS & REPORTING SCHEMAS ====================

class ProgressAnalyticsBase(BaseModel):
    student_id: int
    weekly_progress: Dict[str, Dict[str, Any]]
    monthly_improvement: Dict[str, float]
    subject_wise_performance: Dict[str, Dict[str, Any]]
    time_efficiency: Dict[str, Dict[str, Any]]
    engagement_metrics: Dict[str, Any]
    predicted_performance: Dict[str, Dict[str, Any]]
    risk_factors: List[str]
    report_frequency: str

class ProgressAnalyticsCreate(ProgressAnalyticsBase):
    pass

class ProgressAnalyticsResponse(ProgressAnalyticsBase):
    id: int
    last_report_generated: Optional[datetime] = None

    class Config:
        from_attributes = True

class ContentInteractionBase(BaseModel):
    student_id: int
    content_id: int
    interaction_type: str
    interaction_time: datetime
    duration: int
    completion_status: str
    interaction_depth: int
    rating: Optional[int] = None
    concepts_learned: List[str]
    retention_score: float

class ContentInteractionCreate(ContentInteractionBase):
    pass

class ContentInteractionResponse(ContentInteractionBase):
    id: int

    class Config:
        from_attributes = True

class SystemMetricsBase(BaseModel):
    metric_type: str
    metric_name: str
    metric_value: Dict[str, Any]
    time_period: datetime
    user_segment: Optional[str] = None
    geographic_data: Dict[str, Any]

class SystemMetricsCreate(SystemMetricsBase):
    pass

class SystemMetricsResponse(SystemMetricsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== CONFIGURATION SCHEMAS ====================

class SystemConfigurationBase(BaseModel):
    config_key: str
    config_value: Dict[str, Any]
    config_type: str
    description: str
    is_active: bool
    modified_by: str

class SystemConfigurationCreate(SystemConfigurationBase):
    pass

class SystemConfigurationResponse(SystemConfigurationBase):
    id: int
    last_modified: datetime

    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    user_id: int
    notification_type: NotificationType
    title: str
    message: str
    priority: str
    expires_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== AGGREGATE SCHEMAS ====================

class StudentDashboard(BaseModel):
    """Complete student dashboard data"""
    student_info: StudentResponse
    current_assessment: Optional[AssessmentResponse] = None
    weakness_analysis: Optional[WeaknessProfileResponse] = None
    learning_path: Optional[LearningPathResponse] = None
    simulation_progress: List[SimulationProgressResponse]
    career_profile: Optional[CareerProfileResponse] = None
    recent_content_interactions: List[ContentInteractionResponse]
    progress_analytics: Optional[ProgressAnalyticsResponse] = None

class AssessmentAnalysis(BaseModel):
    """Comprehensive assessment analysis"""
    assessment: AssessmentResponse
    weakness_impact: Dict[str, Any]
    recommended_actions: List[Dict[str, str]]
    simulation_recommendations: List[Dict[str, Any]]
    learning_path_updates: List[Dict[str, Any]]

class CareerAnalysis(BaseModel):
    """Complete career analysis"""
    student_profile: StudentResponse
    career_matches: List[Dict[str, Any]]
    skill_gap_analysis: Dict[str, Any]
    development_roadmap: Dict[str, Any]
    industry_trends: List[Dict[str, Any]]

class SimulationAnalytics(BaseModel):
    """Simulation performance analytics"""
    student_id: int
    simulation_type: SimulationType
    overall_mastery: float
    time_efficiency: float
    engagement_score: float
    concept_mastery: Dict[str, float]
    improvement_recommendations: List[str]

class ContentAnalytics(BaseModel):
    """Content engagement analytics"""
    student_id: int
    content_type_performance: Dict[str, Dict[str, Any]]
    language_preference_impact: Dict[str, Any]
    accessibility_feature_usage: Dict[str, int]
    content_recommendations: List[Dict[str, Any]]

# ==================== REQUEST/RESPONSE WRAPPERS ====================

class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaginatedResponse(BaseModel):
    """Paginated API response"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

class BulkOperationResponse(BaseModel):
    """Response for bulk operations"""
    success_count: int
    failed_count: int
    errors: List[Dict[str, str]]
    processed_items: List[Any]

# ==================== VALIDATION CLASSES ====================

class AssessmentValidator:
    """Validation methods for assessments"""
    
    @staticmethod
    def validate_score(score: float, max_score: float) -> bool:
        return 0 <= score <= max_score
    
    @staticmethod
    def validate_time_taken(time_taken: int) -> bool:
        return time_taken > 0
    
    @staticmethod
    def validate_complexity_level(level: int) -> bool:
        return 1 <= level <= 10

class StudentValidator:
    """Validation methods for student data"""
    
    @staticmethod
    def validate_age(age: int) -> bool:
        return 5 <= age <= 100
    
    @staticmethod
    def validate_education_level(level: str, age: int) -> bool:
        if level == "school":
            return 5 <= age <= 18
        elif level == "college":
            return 17 <= age <= 30
        elif level == "competitive":
            return 16 <= age <= 35
        return True

class SimulationValidator:
    """Validation methods for simulations"""
    
    @staticmethod
    def validate_mastery_score(score: float) -> bool:
        return 0 <= score <= 100
    
    @staticmethod
    def validate_confidence_level(level: int) -> bool:
        return 1 <= level <= 10
    
    @staticmethod
    def validate_duration(duration: int) -> bool:
        return duration > 0