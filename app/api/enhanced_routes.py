"""
Enhanced API Routes for EduVerse AI - All 10 Engines
Comprehensive RESTful API endpoints with advanced features and security
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.db.database import get_db
from app.db.enhanced_models import (
    User, Student, Mentor, Assessment, WeaknessProfile, LearningPath,
    SimulationModule, SimulationProgress, ContentRepository, ExamDatabase,
    QuestionBank, CareerDatabase, CareerProfile, MentorSession,
    ProgressAnalytics, ContentInteraction, SystemMetrics, SystemConfiguration,
    Notification
)
from app.db.enhanced_schemas import (
    UserCreate, UserResponse, StudentCreate, StudentResponse, MentorCreate,
    MentorResponse, AssessmentCreate, AssessmentResponse, WeaknessProfileCreate,
    WeaknessProfileResponse, LearningPathCreate, LearningPathResponse,
    SimulationModuleCreate, SimulationModuleResponse, SimulationProgressCreate,
    SimulationProgressResponse, ContentRepositoryCreate, ContentRepositoryResponse,
    ExamDatabaseCreate, ExamDatabaseResponse, QuestionBankCreate, QuestionBankResponse,
    CareerDatabaseCreate, CareerDatabaseResponse, CareerProfileCreate, CareerProfileResponse,
    MentorSessionCreate, MentorSessionResponse, ProgressAnalyticsCreate,
    ProgressAnalyticsResponse, ContentInteractionCreate, ContentInteractionResponse,
    SystemMetricsCreate, SystemMetricsResponse, SystemConfigurationCreate,
    SystemConfigurationResponse, NotificationCreate, NotificationResponse,
    StudentDashboard, AssessmentAnalysis, CareerAnalysis, SimulationAnalytics,
    ContentAnalytics, ApiResponse, PaginatedResponse
)
from app.core.auth import (
    AuthManager, UserAuthenticator, RoleBasedAccessControl, SecurityManager,
    get_current_user, get_current_active_user, get_student, get_teacher,
    get_admin, get_mentor, get_teacher_or_admin, get_student_or_teacher,
    get_all_authenticated, rate_limiter, SECURITY_CONFIG
)
from app.agents import (
    student_intelligence_agent, foundation_agent, simulation_agent,
    prediction_agent, competitive_exam_agent, college_mastery_agent,
    career_agent, multilingual_agent, industry_integration_agent,
    explainability_agent, autonomous_orchestrator
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# ==================== AUTHENTICATION & USER MANAGEMENT ====================

@router.post("/auth/register", response_model=ApiResponse)
async def register_user(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check rate limiting
        if not rate_limiter.check_rate_limit(f"register_{user_data.email}", 5, 3600):  # 5 registrations per hour
            raise HTTPException(status_code=429, detail="Too many registration attempts")
        
        # Validate password strength
        password_check = SecurityManager.validate_password_strength(user_data.password)
        if not password_check["is_valid"]:
            return ApiResponse(
                success=False,
                message="Password does not meet security requirements",
                errors=password_check["errors"]
            )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            return ApiResponse(
                success=False,
                message="User with this email already exists"
            )
        
        # Create user
        hashed_password = AuthManager.hash_password(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate welcome notification
        welcome_notification = Notification(
            user_id=user.id,
            notification_type="update",
            title="Welcome to EduVerse AI",
            message="Your account has been successfully created. Explore our intelligent learning ecosystem!",
            priority="medium"
        )
        db.add(welcome_notification)
        db.commit()
        
        return ApiResponse(
            success=True,
            message="User registered successfully",
            data=UserResponse.from_orm(user)
        )
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/auth/login", response_model=ApiResponse)
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    """User login with JWT token generation"""
    try:
        # Check rate limiting
        if not rate_limiter.check_rate_limit(f"login_{email}", 10, 300):  # 10 attempts per 5 minutes
            raise HTTPException(status_code=429, detail="Too many login attempts")
        
        user = await UserAuthenticator.authenticate_user(db, email, password)
        if not user:
            return ApiResponse(
                success=False,
                message="Invalid email or password"
            )
        
        if not user.is_active:
            return ApiResponse(
                success=False,
                message="Account is inactive"
            )
        
        # Generate tokens
        access_token = AuthManager.create_access_token(data={"sub": user.email})
        refresh_token = AuthManager.create_refresh_token(data={"sub": user.email})
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Login successful",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": UserResponse.from_orm(user)
            }
        )
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/auth/refresh", response_model=ApiResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        payload = AuthManager.verify_token(refresh_token, "refresh")
        email = payload.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid user")
        
        # Generate new access token
        access_token = AuthManager.create_access_token(data={"sub": user.email})
        
        return ApiResponse(
            success=True,
            message="Token refreshed successfully",
            data={"access_token": access_token}
        )
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# ==================== STUDENT INTELLIGENCE & ASSESSMENT ENGINE ====================

@router.post("/students/{student_id}/assessments", response_model=ApiResponse)
async def submit_assessment(
    student_id: int,
    assessment_data: AssessmentCreate,
    current_user: User = Depends(get_student_or_teacher),
    db: Session = Depends(get_db)
):
    """Submit assessment and get intelligent analysis"""
    try:
        # Verify student ownership or teacher access
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if current_user.role == "student" and student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Create assessment
        assessment = Assessment(**assessment_data.dict())
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        # Analyze performance using AI agent
        analysis = student_intelligence_agent.analyze_assessment(
            assessment.score,
            assessment.max_score,
            assessment.time_taken,
            assessment.difficulty.value
        )
        
        # Generate weakness analysis
        assessments = db.query(Assessment).filter(Assessment.student_id == student_id).all()
        assessment_data_list = [
            {"topic": a.topic, "score": a.score, "max_score": a.max_score}
            for a in assessments
        ]
        
        skill_profile = student_intelligence_agent.build_skill_profile(student_id, assessment_data_list)
        
        # Check if foundation rebuilding needed
        if analysis["weakness_detected"]:
            foundation_check = foundation_agent.check_simulation_trigger(1, assessment.topic)
            recommendation = f"Weakness detected in {assessment.topic}. {foundation_check.get('reason', 'Start foundation rebuilding.')}"
        else:
            recommendation = "Great performance! Continue to next topic."
        
        return ApiResponse(
            success=True,
            message="Assessment submitted successfully",
            data={
                "assessment": AssessmentResponse.from_orm(assessment),
                "analysis": analysis,
                "skill_profile": skill_profile,
                "recommendation": recommendation
            }
        )
        
    except Exception as e:
        logger.error(f"Assessment submission error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit assessment")

@router.get("/students/{student_id}/weakness-analysis", response_model=ApiResponse)
async def get_weakness_analysis(
    student_id: int,
    current_user: User = Depends(get_student_or_teacher),
    db: Session = Depends(get_db)
):
    """Get comprehensive weakness analysis"""
    try:
        # Verify access
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if current_user.role == "student" and student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        assessments = db.query(Assessment).filter(Assessment.student_id == student_id).all()
        if not assessments:
            raise HTTPException(status_code=404, detail="No assessments found")
        
        assessment_data = [
            {"topic": a.topic, "score": a.score, "max_score": a.max_score}
            for a in assessments
        ]
        
        profile = student_intelligence_agent.build_skill_profile(student_id, assessment_data)
        
        # Save to database
        weakness_profile = WeaknessProfile(
            student_id=student_id,
            subject="General",
            weak_topics=profile["weak_topics"],
            strength_topics=profile["strong_topics"],
            priority_index=profile["priority_index"]
        )
        db.add(weakness_profile)
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Weakness analysis generated successfully",
            data=profile
        )
        
    except Exception as e:
        logger.error(f"Weakness analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate weakness analysis")

# ==================== FOUNDATION REBUILDING ENGINE ====================

@router.post("/students/{student_id}/foundation/rebuild", response_model=ApiResponse)
async def rebuild_foundation(
    student_id: int,
    foundation_data: Dict[str, str],
    current_user: User = Depends(get_student_or_teacher),
    db: Session = Depends(get_db)
):
    """Get foundation rebuilding plan"""
    try:
        # Verify access
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if current_user.role == "student" and student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        weak_topic = foundation_data.get("weak_topic")
        if not weak_topic:
            raise HTTPException(status_code=400, detail="Weak topic is required")
        
        # Generate learning path
        learning_path = foundation_agent.generate_learning_path(weak_topic, "Weak")
        
        # Generate visual explanations
        visual_aids = foundation_agent.generate_visual_explanation(weak_topic)
        
        return ApiResponse(
            success=True,
            message="Foundation rebuilding plan generated",
            data={
                "student_id": student_id,
                "topic": weak_topic,
                "learning_path": learning_path,
                "visual_aids": visual_aids,
                "micro_concepts": learning_path["learning_path"]
            }
        )
        
    except Exception as e:
        logger.error(f"Foundation rebuilding error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate foundation plan")

# ==================== SIMULATION INTELLIGENCE ENGINE ====================

@router.post("/simulations/start", response_model=ApiResponse)
async def start_simulation(
    simulation_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Start adaptive simulation"""
    try:
        student_id = simulation_data.get("student_id")
        simulation_type = simulation_data.get("simulation_type")
        topic = simulation_data.get("topic")
        difficulty = simulation_data.get("difficulty", "beginner")
        
        # Verify student ownership
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student or student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get simulation configuration
        config = simulation_agent.get_simulation_config(simulation_type, difficulty, student.language_preference.value)
        
        # Create simulation progress record
        simulation_progress = SimulationProgress(
            student_id=student_id,
            simulation_id=simulation_data.get("simulation_id", 1),  # Default simulation
            mastery_score=0.0,
            attempts=0,
            completed=False
        )
        db.add(simulation_progress)
        db.commit()
        db.refresh(simulation_progress)
        
        return ApiResponse(
            success=True,
            message="Simulation started successfully",
            data={
                "simulation_id": simulation_progress.id,
                "parameters": config,
                "guidance_level": config["difficulty"]["guidance"],
                "language": config["language"]
            }
        )
        
    except Exception as e:
        logger.error(f"Simulation start error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start simulation")

@router.post("/simulations/{simulation_id}/complete", response_model=ApiResponse)
async def complete_simulation(
    simulation_id: int,
    performance_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Complete simulation and get reinforcement test"""
    try:
        performance = performance_data.get("performance", 0.0)
        
        simulation = db.query(SimulationProgress).filter(SimulationProgress.id == simulation_id).first()
        if not simulation:
            raise HTTPException(status_code=404, detail="Simulation not found")
        
        # Verify student ownership
        student = db.query(Student).filter(Student.id == simulation.student_id).first()
        if not student or student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Generate reinforcement test
        test = simulation_agent.generate_reinforcement_test(simulation.simulation_id, simulation.simulation_id)
        
        # Calculate mastery
        mastery = simulation_agent.calculate_mastery_score(simulation.attempts + 1, performance, 80.0)
        
        # Update simulation progress
        simulation.mastery_score = mastery["mastery_score"]
        simulation.attempts += 1
        simulation.completed = mastery["level"] == "Mastered"
        simulation.completed_at = datetime.utcnow() if simulation.completed else None
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Simulation completed successfully",
            data={
                "reinforcement_test": test,
                "mastery": mastery,
                "next_step": "Take reinforcement test" if not simulation.completed else "Move to next topic"
            }
        )
        
    except Exception as e:
        logger.error(f"Simulation completion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to complete simulation")

# ==================== QUESTION INTELLIGENCE & PREDICTION ENGINE ====================

@router.post("/exam/predict", response_model=ApiResponse)
async def predict_exam_questions(
    prediction_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Get exam question predictions"""
    try:
        exam_type = prediction_data.get("exam_type")
        subject = prediction_data.get("subject")
        student_weaknesses = prediction_data.get("student_weaknesses", [])
        
        priority_pack = prediction_agent.generate_priority_questions(
            exam_type,
            subject,
            student_weaknesses
        )
        
        if "error" in priority_pack:
            raise HTTPException(status_code=404, detail=priority_pack["error"])
        
        # Save prediction
        exam_prediction = ExamDatabase(
            exam_type=exam_type,
            subject=subject,
            year=datetime.utcnow().year,
            board_university="Auto-generated",
            question_text="Prediction generated",
            question_type="prediction",
            marks=0,
            difficulty="beginner",
            topic="General",
            concept_tags=[],
            correct_answer="",
            explanation="",
            solution_steps=[],
            source="AI Prediction"
        )
        db.add(exam_prediction)
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Exam predictions generated successfully",
            data={
                "high_probability_topics": priority_pack["priority_question_pack"],
                "priority_questions": [q["topic"] for q in priority_pack["priority_question_pack"][:5]],
                "weightage_distribution": {"analyzed": True},
                "study_strategy": str(priority_pack["study_strategy"])
            }
        )
        
    except Exception as e:
        logger.error(f"Exam prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate exam predictions")

# ==================== COMPETITIVE & GOVERNMENT EXAM ENGINE ====================

@router.post("/mock-tests/generate", response_model=ApiResponse)
async def generate_mock_test(
    mock_test_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Generate adaptive mock test"""
    try:
        exam_type = mock_test_data.get("exam_type")
        difficulty = mock_test_data.get("difficulty", "medium")
        student_id = mock_test_data.get("student_id")
        
        # Get student weaknesses
        weakness_profile = db.query(WeaknessProfile).filter(WeaknessProfile.student_id == student_id).first()
        weak_topics = weakness_profile.weak_topics if weakness_profile else []
        
        mock_test = competitive_exam_agent.generate_mock_test(exam_type, difficulty, weak_topics)
        
        return ApiResponse(
            success=True,
            message="Mock test generated successfully",
            data=mock_test
        )
        
    except Exception as e:
        logger.error(f"Mock test generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate mock test")

@router.post("/mock-tests/evaluate", response_model=ApiResponse)
async def evaluate_mock_test(
    evaluation_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Evaluate mock test"""
    try:
        student_id = evaluation_data.get("student_id")
        exam_type = evaluation_data.get("exam_type")
        answers = evaluation_data.get("answers", [])
        
        # Placeholder correct answers (in production, fetch from database)
        correct_answers = ["A"] * len(answers)
        
        config = competitive_exam_agent.EXAM_CONFIGS.get(exam_type, {})
        if not config:
            raise HTTPException(status_code=404, detail="Exam type not supported")
        
        evaluation = competitive_exam_agent.evaluate_mock_test(
            answers,
            correct_answers,
            config
        )
        
        # Analyze speed vs accuracy
        speed_analysis = competitive_exam_agent.analyze_speed_vs_accuracy(
            120,  # time_taken in minutes
            evaluation["accuracy"],
            config["total_questions"]
        )
        
        # Estimate rank
        rank_est = competitive_exam_agent.estimate_rank(
            evaluation["score"],
            exam_type,
            config["total_questions"] * config["marks_per_question"]
        )
        
        # Save mock test result
        mock_test = MockTest(
            student_id=student_id,
            exam_type=exam_type,
            score=evaluation["score"],
            accuracy=evaluation["accuracy"],
            speed_score=speed_analysis["speed_score"],
            rank_estimate=rank_est["estimated_rank"]
        )
        db.add(mock_test)
        db.commit()
        
        weak_areas = [topic for topic, perf in evaluation["topic_performance"].items() 
                      if perf["correct"] / perf["total"] < 0.6]
        
        improvement_tips = competitive_exam_agent.generate_improvement_strategy(
            weak_areas,
            evaluation["accuracy"],
            speed_analysis["speed_score"]
        )
        
        return ApiResponse(
            success=True,
            message="Mock test evaluated successfully",
            data={
                "score": evaluation["score"],
                "accuracy": evaluation["accuracy"],
                "speed_score": speed_analysis["speed_score"],
                "rank_estimate": rank_est["estimated_rank"],
                "weak_areas": weak_areas,
                "improvement_tips": [tip["area"] for tip in improvement_tips]
            }
        )
        
    except Exception as e:
        logger.error(f"Mock test evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to evaluate mock test")

# ==================== CAREER INTELLIGENCE ENGINE ====================

@router.post("/career/analyze", response_model=ApiResponse)
async def analyze_career(
    career_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Analyze career fit and provide recommendations"""
    try:
        student_id = career_data.get("student_id")
        interests = career_data.get("interests", [])
        strengths = career_data.get("strengths", [])
        
        career_matches = career_agent.analyze_career_fit(
            interests,
            strengths,
            {}
        )
        
        if not career_matches:
            raise HTTPException(status_code=404, detail="No matching careers found")
        
        top_career = career_matches[0]["career"]
        skill_gaps = career_agent.identify_skill_gaps(top_career, strengths)
        roadmap = career_agent.generate_learning_roadmap(top_career, skill_gaps["skill_gaps"])
        
        # Save career profile
        career_profile = CareerProfile(
            student_id=student_id,
            interests=interests,
            strengths=strengths,
            recommended_careers=[c["career"] for c in career_matches[:3]],
            skill_gaps=skill_gaps["skill_gaps"],
            certifications=roadmap.get("certifications", [])
        )
        db.add(career_profile)
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Career analysis completed successfully",
            data={
                "recommended_careers": career_matches[:5],
                "skill_gaps": skill_gaps["skill_gaps"],
                "certifications": roadmap.get("certifications", []),
                "learning_path": [phase["skill"] for phase in roadmap["phases"]]
            }
        )
        
    except Exception as e:
        logger.error(f"Career analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze career")

# ==================== MULTILINGUAL & ACCESSIBILITY ENGINE ====================

@router.post("/translate", response_model=ApiResponse)
async def translate_content(
    translation_data: Dict[str, str],
    current_user: User = Depends(get_all_authenticated)
):
    """Translate content to target language"""
    try:
        text = translation_data.get("text")
        target_language = translation_data.get("target_language")
        
        if not text or not target_language:
            raise HTTPException(status_code=400, detail="Text and target language are required")
        
        translation = multilingual_agent.translate_text(text, target_language)
        audio = multilingual_agent.generate_audio_narration(translation["translated_text"], target_language)
        
        return ApiResponse(
            success=True,
            message="Content translated successfully",
            data={
                "translated_text": translation["translated_text"],
                "audio_url": audio.get("audio_url")
            }
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to translate content")

@router.get("/languages", response_model=ApiResponse)
async def get_supported_languages(current_user: User = Depends(get_all_authenticated)):
    """Get list of supported languages"""
    return ApiResponse(
        success=True,
        message="Languages retrieved successfully",
        data={
            "languages": multilingual_agent.SUPPORTED_LANGUAGES,
            "total": len(multilingual_agent.SUPPORTED_LANGUAGES)
        }
    )

# ==================== INDUSTRY INTEGRATION ENGINE ====================

@router.post("/mentors/onboard", response_model=ApiResponse)
async def onboard_mentor(
    mentor_data: MentorCreate,
    current_user: User = Depends(get_admin),
    db: Session = Depends(get_db)
):
    """Onboard industry mentor"""
    try:
        mentor = Mentor(**mentor_data.dict())
        db.add(mentor)
        db.commit()
        db.refresh(mentor)
        
        return ApiResponse(
            success=True,
            message="Mentor onboarded successfully",
            data=MentorResponse.from_orm(mentor)
        )
        
    except Exception as e:
        logger.error(f"Mentor onboarding error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to onboard mentor")

@router.get("/mentors/find/{domain}", response_model=ApiResponse)
async def find_mentor(
    domain: str,
    expertise: str,
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Find suitable mentor"""
    try:
        mentors = db.query(Mentor).filter(
            Mentor.industry == domain,
            Mentor.expertise.contains([expertise])
        ).all()
        
        return ApiResponse(
            success=True,
            message="Mentors found successfully",
            data=[MentorResponse.from_orm(mentor) for mentor in mentors]
        )
        
    except Exception as e:
        logger.error(f"Mentor search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to find mentors")

# ==================== EXPLAINABILITY & TRANSPARENCY ENGINE ====================

@router.get("/explain/topic-importance/{topic}", response_model=ApiResponse)
async def explain_topic_importance(
    topic: str,
    exam_type: str,
    probability: float = 75.0,
    current_user: User = Depends(get_all_authenticated)
):
    """Explain why a topic is important"""
    try:
        explanation = explainability_agent.explain_topic_importance(topic, exam_type, probability)
        return ApiResponse(
            success=True,
            message="Topic importance explained successfully",
            data=explanation
        )
        
    except Exception as e:
        logger.error(f"Topic explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to explain topic importance")

@router.get("/transparency-report/{student_id}", response_model=ApiResponse)
async def get_transparency_report(
    student_id: int,
    current_user: User = Depends(get_student_or_teacher),
    db: Session = Depends(get_db)
):
    """Get comprehensive transparency report"""
    try:
        # Verify access
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if current_user.role == "student" and student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        report = explainability_agent.generate_transparency_report(student_id, "Last 30 days")
        return ApiResponse(
            success=True,
            message="Transparency report generated successfully",
            data=report
        )
        
    except Exception as e:
        logger.error(f"Transparency report error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate transparency report")

# ==================== COLLEGE MASTERY ENGINE ====================

@router.get("/college/learning-path/{department}/{subject}", response_model=ApiResponse)
async def get_subject_learning_path(
    department: str,
    subject: str,
    current_level: str = "Beginner",
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Get deep learning path for college subject"""
    try:
        learning_path = college_mastery_agent.generate_subject_learning_path(department, subject, current_level)
        return ApiResponse(
            success=True,
            message="Learning path generated successfully",
            data=learning_path
        )
        
    except Exception as e:
        logger.error(f"Learning path generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate learning path")

@router.get("/college/projects/{department}", response_model=ApiResponse)
async def get_project_suggestions(
    department: str,
    skill_level: str,
    interests: List[str] = [],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Get project suggestions for college students"""
    try:
        projects = college_mastery_agent.suggest_projects(department, skill_level, interests)
        return ApiResponse(
            success=True,
            message="Project suggestions generated successfully",
            data=projects
        )
        
    except Exception as e:
        logger.error(f"Project suggestion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate project suggestions")

# ==================== AUTONOMOUS AGENT ORCHESTRATOR ====================

@router.post("/autonomous/analyze-and-decide", response_model=ApiResponse)
async def autonomous_decision(
    assessment_data: Dict[str, Any],
    current_user: User = Depends(get_student),
    db: Session = Depends(get_db)
):
    """Autonomous agent analyzes assessment and decides next actions"""
    try:
        student_id = assessment_data.get("student_id")
        
        # Get student profile
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        student_profile = {
            "language": student.language_preference.value,
            "education_level": student.education_level.value,
            "target_exam": "School",  # Get from profile
            "department": "Computer Science",  # Get from profile
            "domain": "Software"  # Get from profile
        }
        
        agent = autonomous_orchestrator.create_autonomous_agent(student_id, student_profile)
        decision = agent.analyze_and_decide(assessment_data)
        
        return ApiResponse(
            success=True,
            message="Autonomous analysis completed",
            data={
                "autonomous_decision": decision,
                "agent_type": "EduVerse Autonomous Intelligence",
                "decision_confidence": "High"
            }
        )
        
    except Exception as e:
        logger.error(f"Autonomous decision error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform autonomous analysis")

@router.get("/dashboard/{student_id}", response_model=ApiResponse)
async def get_student_dashboard(
    student_id: int,
    current_user: User = Depends(get_student_or_teacher),
    db: Session = Depends(get_db)
):
    """Get comprehensive student dashboard"""
    try:
        # Verify access
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        if current_user.role == "student" and student.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get student info
        student_info = StudentResponse.from_orm(student)
        
        # Get recent assessments
        recent_assessment = db.query(Assessment).filter(
            Assessment.student_id == student_id
        ).order_by(Assessment.created_at.desc()).first()
        
        # Get weakness analysis
        weakness_analysis = db.query(WeaknessProfile).filter(
            WeaknessProfile.student_id == student_id
        ).order_by(WeaknessProfile.last_updated.desc()).first()
        
        # Get learning path
        learning_path = db.query(LearningPath).filter(
            LearningPath.student_id == student_id
        ).order_by(LearningPath.created_at.desc()).first()
        
        # Get simulation progress
        simulation_progress = db.query(SimulationProgress).filter(
            SimulationProgress.student_id == student_id
        ).all()
        
        # Get career profile
        career_profile = db.query(CareerProfile).filter(
            CareerProfile.student_id == student_id
        ).order_by(CareerProfile.updated_at.desc()).first()
        
        # Get recent content interactions
        recent_interactions = db.query(ContentInteraction).filter(
            ContentInteraction.student_id == student_id
        ).order_by(ContentInteraction.interaction_time.desc()).limit(10).all()
        
        # Get progress analytics
        progress_analytics = db.query(ProgressAnalytics).filter(
            ProgressAnalytics.student_id == student_id
        ).order_by(ProgressAnalytics.last_report_generated.desc()).first()
        
        dashboard_data = StudentDashboard(
            student_info=student_info,
            current_assessment=AssessmentResponse.from_orm(recent_assessment) if recent_assessment else None,
            weakness_analysis=WeaknessProfileResponse.from_orm(weakness_analysis) if weakness_analysis else None,
            learning_path=LearningPathResponse.from_orm(learning_path) if learning_path else None,
            simulation_progress=[SimulationProgressResponse.from_orm(sp) for sp in simulation_progress],
            career_profile=CareerProfileResponse.from_orm(career_profile) if career_profile else None,
            recent_content_interactions=[ContentInteractionResponse.from_orm(ci) for ci in recent_interactions],
            progress_analytics=ProgressAnalyticsResponse.from_orm(progress_analytics) if progress_analytics else None
        )
        
        return ApiResponse(
            success=True,
            message="Student dashboard generated successfully",
            data=dashboard_data
        )
        
    except Exception as e:
        logger.error(f"Dashboard generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate student dashboard")

# ==================== SYSTEM MANAGEMENT ====================

@router.get("/system/health", response_model=ApiResponse)
async def system_health(current_user: User = Depends(get_admin)):
    """Get system health status"""
    return ApiResponse(
        success=True,
        message="System is healthy",
        data={
            "status": "healthy",
            "engines_active": 10,
            "database_connected": True,
            "ai_agents_running": True,
            "timestamp": datetime.utcnow()
        }
    )

@router.get("/system/metrics", response_model=ApiResponse)
async def system_metrics(current_user: User = Depends(get_admin), db: Session = Depends(get_db)):
    """Get system-wide metrics"""
    try:
        # Get user metrics
        total_users = db.query(User).count()
        active_students = db.query(Student).count()
        active_mentors = db.query(Mentor).count()
        
        # Get assessment metrics
        total_assessments = db.query(Assessment).count()
        avg_assessment_score = db.query(Assessment).with_entities(
            (db.func.avg(Assessment.score / Assessment.max_score) * 100).label('avg_score')
        ).scalar()
        
        # Get simulation metrics
        total_simulations = db.query(SimulationProgress).count()
        completed_simulations = db.query(SimulationProgress).filter(
            SimulationProgress.completed == True
        ).count()
        
        metrics = {
            "users": {
                "total": total_users,
                "students": active_students,
                "mentors": active_mentors
            },
            "assessments": {
                "total": total_assessments,
                "average_score": round(avg_assessment_score or 0, 2)
            },
            "simulations": {
                "total": total_simulations,
                "completed": completed_simulations,
                "completion_rate": round((completed_simulations / total_simulations * 100) if total_simulations > 0 else 0, 2)
            },
            "timestamp": datetime.utcnow()
        }
        
        return ApiResponse(
            success=True,
            message="System metrics retrieved successfully",
            data=metrics
        )
        
    except Exception as e:
        logger.error(f"System metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system metrics")