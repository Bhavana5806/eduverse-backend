from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models, schemas
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
    explainability_agent
)
from app.agents.autonomous_orchestrator import create_autonomous_agent
from typing import List

router = APIRouter()

# ============ ENGINE 1: Student Intelligence & Assessment ============

@router.post("/student/create", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create new student profile"""
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.post("/assessment/submit", response_model=schemas.AssessmentResponse)
def submit_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    """Submit assessment and get intelligent analysis"""
    
    # Save assessment
    db_assessment = models.Assessment(**assessment.dict())
    db.add(db_assessment)
    db.commit()
    
    # Analyze performance
    analysis = student_intelligence_agent.analyze_assessment(
        assessment.score,
        assessment.max_score,
        assessment.time_taken,
        assessment.difficulty
    )
    
    # Check if foundation rebuilding needed
    if analysis["weakness_detected"]:
        foundation_check = foundation_agent.check_simulation_trigger(1, assessment.topic)
        recommendation = f"Weakness detected. {foundation_check.get('reason', 'Start foundation rebuilding.')}"
    else:
        recommendation = "Great performance! Continue to next topic."
    
    return {
        "percentage": analysis["percentage"],
        "status": analysis["status"],
        "weakness_detected": analysis["weakness_detected"],
        "recommendation": recommendation
    }

@router.get("/student/{student_id}/weakness-analysis")
def get_weakness_analysis(student_id: int, db: Session = Depends(get_db)):
    """Get comprehensive weakness analysis"""
    
    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id
    ).all()
    
    if not assessments:
        raise HTTPException(status_code=404, detail="No assessments found")
    
    assessment_data = [
        {"topic": a.topic, "score": a.score, "max_score": a.max_score}
        for a in assessments
    ]
    
    profile = student_intelligence_agent.build_skill_profile(student_id, assessment_data)
    
    # Save to database
    db_weakness = models.WeaknessProfile(
        student_id=student_id,
        subject="General",
        weak_topics=profile["weak_topics"],
        strength_topics=profile["strong_topics"],
        priority_index=profile["priority_index"]
    )
    db.add(db_weakness)
    db.commit()
    
    return profile

# ============ ENGINE 2: Foundation Rebuilding ============

@router.post("/foundation/rebuild")
def rebuild_foundation(request: schemas.FoundationRequest, db: Session = Depends(get_db)):
    """Get foundation rebuilding plan"""
    
    learning_path = foundation_agent.generate_learning_path(
        request.weak_topic,
        "Weak"
    )
    
    visual_aids = foundation_agent.generate_visual_explanation(request.weak_topic)
    
    return {
        "student_id": request.student_id,
        "topic": request.weak_topic,
        "learning_path": learning_path,
        "visual_aids": visual_aids,
        "micro_concepts": learning_path["learning_path"]
    }

# ============ ENGINE 3: Simulation Intelligence ============

@router.post("/simulation/start", response_model=schemas.SimulationResponse)
def start_simulation(request: schemas.SimulationRequest, db: Session = Depends(get_db)):
    """Start adaptive simulation"""
    
    config = simulation_agent.get_simulation_config(
        request.simulation_type,
        request.difficulty,
        "English"  # Get from student profile
    )
    
    # Create simulation progress record
    db_sim = models.SimulationProgress(
        student_id=request.student_id,
        simulation_type=request.simulation_type,
        topic=request.topic,
        mastery_score=0.0
    )
    db.add(db_sim)
    db.commit()
    db.refresh(db_sim)
    
    return {
        "simulation_id": db_sim.id,
        "parameters": config,
        "guidance_level": config["difficulty"]["guidance"],
        "language": config["language"]
    }

@router.post("/simulation/{simulation_id}/complete")
def complete_simulation(simulation_id: int, performance: float, db: Session = Depends(get_db)):
    """Complete simulation and get reinforcement test"""
    
    sim = db.query(models.SimulationProgress).filter(
        models.SimulationProgress.id == simulation_id
    ).first()
    
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    # Generate reinforcement test
    test = simulation_agent.generate_reinforcement_test(sim.simulation_type, sim.topic)
    
    # Calculate mastery
    mastery = simulation_agent.calculate_mastery_score(sim.attempts + 1, performance, 80.0)
    
    sim.mastery_score = mastery["mastery_score"]
    sim.attempts += 1
    sim.completed = mastery["level"] == "Mastered"
    db.commit()
    
    return {
        "reinforcement_test": test,
        "mastery": mastery,
        "next_step": "Take reinforcement test" if not sim.completed else "Move to next topic"
    }

# ============ ENGINE 4: Question Intelligence & Prediction ============

@router.post("/exam/predict", response_model=schemas.ExamPredictionResponse)
def predict_exam_questions(request: schemas.ExamPredictionRequest, db: Session = Depends(get_db)):
    """Get exam question predictions"""
    
    priority_pack = prediction_agent.generate_priority_questions(
        request.exam_type,
        request.subject,
        request.student_weaknesses
    )
    
    if "error" in priority_pack:
        raise HTTPException(status_code=404, detail=priority_pack["error"])
    
    # Save prediction
    db_prediction = models.ExamPrediction(
        exam_type=request.exam_type,
        subject=request.subject,
        high_probability_topics=[q["topic"] for q in priority_pack["priority_question_pack"]],
        question_patterns={"patterns": "analyzed"},
        weightage_distribution={"distribution": "calculated"}
    )
    db.add(db_prediction)
    db.commit()
    
    return {
        "high_probability_topics": priority_pack["priority_question_pack"],
        "priority_questions": [q["topic"] for q in priority_pack["priority_question_pack"][:5]],
        "weightage_distribution": {"analyzed": True},
        "study_strategy": str(priority_pack["study_strategy"])
    }

# ============ ENGINE 5: Competitive & Government Exam ============

@router.post("/mock-test/generate")
def generate_mock_test(exam_type: str, difficulty: str, student_id: int, db: Session = Depends(get_db)):
    """Generate adaptive mock test"""
    
    # Get student weaknesses
    weakness_profile = db.query(models.WeaknessProfile).filter(
        models.WeaknessProfile.student_id == student_id
    ).first()
    
    weak_topics = weakness_profile.weak_topics if weakness_profile else []
    
    mock_test = competitive_exam_agent.generate_mock_test(exam_type, difficulty, weak_topics)
    
    return mock_test

@router.post("/mock-test/evaluate", response_model=schemas.MockTestResponse)
def evaluate_mock_test(test_data: schemas.MockTestCreate, db: Session = Depends(get_db)):
    """Evaluate mock test"""
    
    # Placeholder correct answers (in production, fetch from database)
    correct_answers = ["A"] * len(test_data.answers)
    
    config = competitive_exam_agent.EXAM_CONFIGS.get(test_data.exam_type, {})
    
    if not config:
        raise HTTPException(status_code=404, detail="Exam type not supported")
    
    evaluation = competitive_exam_agent.evaluate_mock_test(
        test_data.answers,
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
        test_data.exam_type,
        config["total_questions"] * config["marks_per_question"]
    )
    
    # Save mock test result
    db_mock = models.MockTest(
        student_id=test_data.student_id,
        exam_type=test_data.exam_type,
        score=evaluation["score"],
        accuracy=evaluation["accuracy"],
        speed_score=speed_analysis["speed_score"],
        rank_estimate=rank_est["estimated_rank"]
    )
    db.add(db_mock)
    db.commit()
    
    weak_areas = [topic for topic, perf in evaluation["topic_performance"].items() 
                  if perf["correct"] / perf["total"] < 0.6]
    
    improvement_tips = competitive_exam_agent.generate_improvement_strategy(
        weak_areas,
        evaluation["accuracy"],
        speed_analysis["speed_score"]
    )
    
    return {
        "score": evaluation["score"],
        "accuracy": evaluation["accuracy"],
        "speed_score": speed_analysis["speed_score"],
        "rank_estimate": rank_est["estimated_rank"],
        "weak_areas": weak_areas,
        "improvement_tips": [tip["area"] for tip in improvement_tips]
    }

# ============ ENGINE 7: Career Intelligence ============

@router.post("/career/analyze", response_model=schemas.CareerAnalysisResponse)
def analyze_career(request: schemas.CareerAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze career fit and provide recommendations"""
    
    career_matches = career_agent.analyze_career_fit(
        request.interests,
        request.strengths,
        {}
    )
    
    if not career_matches:
        raise HTTPException(status_code=404, detail="No matching careers found")
    
    top_career = career_matches[0]["career"]
    skill_gaps = career_agent.identify_skill_gaps(top_career, request.strengths)
    roadmap = career_agent.generate_learning_roadmap(top_career, skill_gaps["skill_gaps"])
    
    # Save career profile
    db_career = models.CareerProfile(
        student_id=request.student_id,
        interests=request.interests,
        strengths=request.strengths,
        recommended_careers=[c["career"] for c in career_matches[:3]],
        skill_gaps=skill_gaps["skill_gaps"],
        certifications=roadmap.get("certifications", [])
    )
    db.add(db_career)
    db.commit()
    
    return {
        "recommended_careers": career_matches[:5],
        "skill_gaps": skill_gaps["skill_gaps"],
        "certifications": roadmap.get("certifications", []),
        "learning_path": [phase["skill"] for phase in roadmap["phases"]]
    }

# ============ ENGINE 8: Multilingual & Accessibility ============

@router.post("/translate", response_model=schemas.TranslationResponse)
def translate_content(request: schemas.TranslationRequest):
    """Translate content to target language"""
    
    translation = multilingual_agent.translate_text(
        request.text,
        request.target_language
    )
    
    audio = multilingual_agent.generate_audio_narration(
        translation["translated_text"],
        request.target_language
    )
    
    return {
        "translated_text": translation["translated_text"],
        "audio_url": audio.get("audio_url")
    }

@router.get("/languages")
def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": multilingual_agent.SUPPORTED_LANGUAGES,
        "total": len(multilingual_agent.SUPPORTED_LANGUAGES)
    }

# ============ ENGINE 10: Explainability & Transparency ============

@router.get("/explain/topic-importance/{topic}")
def explain_topic_importance(topic: str, exam_type: str, probability: float = 75.0):
    """Explain why a topic is important"""
    return explainability_agent.explain_topic_importance(topic, exam_type, probability)

@router.get("/explain/career-suggestion/{career}")
def explain_career_suggestion(career: str, match_score: float, student_id: int):
    """Explain career suggestion"""
    return explainability_agent.explain_career_suggestion(
        career,
        match_score,
        {"interests": [], "strengths": [], "matching_skills": []}
    )

@router.get("/transparency-report/{student_id}")
def get_transparency_report(student_id: int):
    """Get comprehensive transparency report"""
    return explainability_agent.generate_transparency_report(student_id, "Last 30 days")

# ============ ENGINE 6: College Mastery & Department Excellence ============

@router.get("/college/learning-path/{department}/{subject}")
def get_subject_learning_path(department: str, subject: str, current_level: str = "Beginner"):
    """Get deep learning path for college subject"""
    return college_mastery_agent.generate_subject_learning_path(department, subject, current_level)

@router.get("/college/projects/{department}")
def get_project_suggestions(department: str, skill_level: str, interests: list = []):
    """Get project suggestions for college students"""
    return college_mastery_agent.suggest_projects(department, skill_level, interests)

@router.get("/college/placement-readiness/{student_id}")
def check_placement_readiness(student_id: int, target_role: str, department: str, db: Session = Depends(get_db)):
    """Check placement readiness"""
    # Get student skills from database (placeholder)
    student_skills = ["Programming", "Data Structures", "Algorithms"]
    return college_mastery_agent.assess_placement_readiness(student_skills, target_role, department)

@router.get("/college/certifications/{department}")
def get_certification_roadmap(department: str, target_role: str):
    """Get certification roadmap"""
    return college_mastery_agent.generate_certification_roadmap(department, target_role)

@router.get("/college/coding-practice/{skill_level}")
def get_coding_practice_plan(skill_level: str, target_companies: list = []):
    """Get coding practice strategy"""
    return college_mastery_agent.suggest_coding_practice(skill_level, target_companies)

@router.get("/college/domain-mastery/{student_id}")
def track_domain_mastery(student_id: int, department: str, completed_subjects: list = []):
    """Track domain mastery"""
    return college_mastery_agent.track_domain_mastery(student_id, department, completed_subjects)

# ============ ENGINE 9: Industry Integration & Credibility ============

@router.post("/industry/mentor/onboard")
def onboard_mentor(mentor_profile: dict):
    """Onboard industry mentor"""
    return industry_integration_agent.onboard_mentor(mentor_profile)

@router.get("/industry/mentor/find/{domain}")
def find_mentor(domain: str, expertise: str):
    """Find suitable mentor"""
    return industry_integration_agent.find_mentor(domain, expertise)

@router.get("/industry/expert-sessions")
def get_expert_sessions(interests: list = []):
    """Get industry expert sessions"""
    return industry_integration_agent.schedule_expert_session("Career", interests)

@router.get("/industry/challenges/{domain}")
def get_industry_challenges(domain: str, skill_level: str):
    """Get real-world industry challenges"""
    return industry_integration_agent.get_real_world_challenges(domain, skill_level)

@router.get("/industry/certifications/{target_industry}")
def get_industry_certifications(target_industry: str, student_skills: list = []):
    """Get industry-aligned certifications"""
    return industry_integration_agent.align_skill_certification(student_skills, target_industry)

@router.get("/industry/internship-pathways")
def get_internship_pathways(domain: str, year: int, skills: list = []):
    """Get internship pathway suggestions"""
    student_profile = {"domain": domain, "year": year, "skills": skills}
    return industry_integration_agent.suggest_internship_pathways(student_profile)

@router.get("/industry/credibility")
def get_platform_credibility():
    """Get platform credibility metrics"""
    return industry_integration_agent.build_system_credibility()

@router.get("/industry/readiness-report/{student_id}")
def get_industry_readiness(student_id: int, domain: str):
    """Get industry readiness report"""
    return industry_integration_agent.generate_industry_readiness_report(student_id, domain)

# ============ AUTONOMOUS AGENT ORCHESTRATOR ============

@router.post("/autonomous/analyze-and-decide")
def autonomous_decision(student_id: int, assessment_data: dict, db: Session = Depends(get_db)):
    """Autonomous agent analyzes assessment and decides next actions"""
    
    # Get student profile
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_profile = {
        "language": student.language,
        "education_level": student.education_level,
        "target_exam": "School",  # Get from profile
        "department": "Computer Science",  # Get from profile
        "domain": "Software"  # Get from profile
    }
    
    agent = create_autonomous_agent(student_id, student_profile)
    decision = agent.analyze_and_decide(assessment_data)
    
    return {
        "autonomous_decision": decision,
        "agent_type": "EduVerse Autonomous Intelligence",
        "decision_confidence": "High"
    }

@router.get("/autonomous/continuous-learning/{student_id}")
def continuous_learning_loop(student_id: int, db: Session = Depends(get_db)):
    """Autonomous continuous learning loop"""
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get all assessments
    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id
    ).all()
    
    assessment_data = [
        {"topic": a.topic, "score": a.score, "max_score": a.max_score}
        for a in assessments
    ]
    
    student_profile = {
        "language": student.language,
        "education_level": student.education_level
    }
    
    agent = create_autonomous_agent(student_id, student_profile)
    loop_state = agent.continuous_learning_loop({"assessments": assessment_data})
    
    return {
        "autonomous_loop": loop_state,
        "monitoring": "active",
        "adaptive": True
    }

@router.post("/autonomous/exam-strategy")
def autonomous_exam_strategy(student_id: int, exam_type: str, exam_date: str, db: Session = Depends(get_db)):
    """Autonomous exam preparation strategy"""
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_profile = {
        "language": student.language,
        "education_level": student.education_level,
        "subject": "Math"
    }
    
    agent = create_autonomous_agent(student_id, student_profile)
    strategy = agent.predict_and_prepare(exam_type, exam_date)
    
    return {
        "autonomous_strategy": strategy,
        "personalized": True,
        "adaptive": True
    }

@router.post("/autonomous/career-pathway")
def autonomous_career_pathway(student_id: int, interests: list, current_skills: list, db: Session = Depends(get_db)):
    """Autonomous career pathway orchestration"""
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_profile = {
        "language": student.language,
        "education_level": student.education_level,
        "department": "Computer Science",
        "domain": "Software"
    }
    
    agent = create_autonomous_agent(student_id, student_profile)
    pathway = agent.career_pathway_orchestration(interests, current_skills)
    
    return {
        "autonomous_pathway": pathway,
        "orchestrated": True,
        "end_to_end": True
    }

@router.post("/autonomous/adaptive-difficulty")
def adaptive_difficulty(student_id: int, db: Session = Depends(get_db)):
    """Autonomous difficulty adjustment"""
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get performance history
    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id
    ).order_by(models.Assessment.created_at.desc()).limit(10).all()
    
    performance_history = [
        {"score": (a.score / a.max_score) * 100, "topic": a.topic}
        for a in assessments
    ]
    
    student_profile = {
        "language": student.language,
        "education_level": student.education_level
    }
    
    agent = create_autonomous_agent(student_id, student_profile)
    adjustment = agent.adaptive_difficulty_controller(performance_history)
    
    return {
        "autonomous_adjustment": adjustment,
        "real_time": True,
        "adaptive": True
    }
