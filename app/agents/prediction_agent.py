"""
Engine 4: Question Intelligence & Prediction Engine
Pattern-based exam question prediction system
"""

# Sample historical data (in production, this would come from database)
EXAM_PATTERNS = {
    "CBSE_Math_Class10": {
        "topic_frequency": {
            "Algebra": 25,
            "Geometry": 20,
            "Trigonometry": 15,
            "Statistics": 15,
            "Probability": 10,
            "Coordinate Geometry": 15
        },
        "question_types": {
            "MCQ": 20,
            "Short Answer": 30,
            "Long Answer": 30,
            "Case Study": 20
        },
        "mark_distribution": {
            "1_mark": 20,
            "2_mark": 24,
            "3_mark": 24,
            "5_mark": 32
        }
    },
    "JEE_Physics": {
        "topic_frequency": {
            "Mechanics": 30,
            "Electromagnetism": 25,
            "Optics": 15,
            "Modern Physics": 15,
            "Thermodynamics": 15
        },
        "question_types": {
            "Single Correct": 40,
            "Multiple Correct": 30,
            "Numerical": 30
        }
    }
}

def analyze_exam_patterns(exam_type: str, subject: str, years: int = 10):
    """Analyze historical exam patterns"""
    pattern_key = f"{exam_type}_{subject}"
    patterns = EXAM_PATTERNS.get(pattern_key, {})
    
    if not patterns:
        return {"error": "Pattern data not available"}
    
    # Calculate probability scores
    topic_freq = patterns.get("topic_frequency", {})
    total_freq = sum(topic_freq.values())
    
    topic_probability = {
        topic: {
            "frequency": freq,
            "probability": round((freq / total_freq) * 100, 2),
            "importance": "High" if freq / total_freq > 0.2 else "Medium" if freq / total_freq > 0.1 else "Low"
        }
        for topic, freq in topic_freq.items()
    }
    
    return {
        "exam_type": exam_type,
        "subject": subject,
        "analysis_period": f"{years} years",
        "topic_probability": topic_probability,
        "question_types": patterns.get("question_types", {}),
        "mark_distribution": patterns.get("mark_distribution", {})
    }

def generate_priority_questions(exam_type: str, subject: str, student_weaknesses: list):
    """Generate smart priority question pack"""
    patterns = analyze_exam_patterns(exam_type, subject)
    
    if "error" in patterns:
        return patterns
    
    # Combine high-probability topics with student weaknesses
    high_prob_topics = [
        topic for topic, data in patterns["topic_probability"].items()
        if data["importance"] in ["High", "Medium"]
    ]
    
    priority_topics = list(set(high_prob_topics + student_weaknesses))
    
    question_pack = []
    for topic in priority_topics:
        is_weakness = topic in student_weaknesses
        prob_data = patterns["topic_probability"].get(topic, {})
        
        question_pack.append({
            "topic": topic,
            "priority": "Critical" if is_weakness and prob_data.get("importance") == "High" else "High" if is_weakness or prob_data.get("importance") == "High" else "Medium",
            "probability": prob_data.get("probability", 0),
            "is_weakness": is_weakness,
            "recommended_questions": 10 if is_weakness else 5,
            "focus_areas": [f"{topic} - Concept", f"{topic} - Application", f"{topic} - Problem Solving"]
        })
    
    # Sort by priority
    priority_order = {"Critical": 0, "High": 1, "Medium": 2}
    question_pack.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return {
        "exam_type": exam_type,
        "subject": subject,
        "priority_question_pack": question_pack,
        "total_topics": len(question_pack),
        "study_strategy": generate_study_strategy(question_pack)
    }

def generate_study_strategy(question_pack: list):
    """Generate personalized study strategy"""
    critical_topics = [q["topic"] for q in question_pack if q["priority"] == "Critical"]
    high_topics = [q["topic"] for q in question_pack if q["priority"] == "High"]
    
    strategy = {
        "phase_1": {
            "duration": "Week 1-2",
            "focus": critical_topics[:3] if critical_topics else high_topics[:3],
            "action": "Deep learning + Practice"
        },
        "phase_2": {
            "duration": "Week 3-4",
            "focus": high_topics,
            "action": "Problem solving + Mock tests"
        },
        "phase_3": {
            "duration": "Week 5+",
            "focus": "All topics",
            "action": "Revision + Full mock tests"
        }
    }
    
    return strategy

def predict_important_derivations(subject: str, exam_type: str):
    """Predict important derivations/formulas"""
    derivations = {
        "Physics": [
            "Equations of Motion",
            "Work-Energy Theorem",
            "Lens Formula",
            "Ohm's Law Applications"
        ],
        "Math": [
            "Quadratic Formula Derivation",
            "Trigonometric Identities",
            "Area under Curve",
            "Distance Formula"
        ]
    }
    
    return derivations.get(subject, [])

def generate_case_study_patterns(exam_type: str):
    """Predict case study patterns"""
    return {
        "common_themes": ["Real-world applications", "Data interpretation", "Problem-solving scenarios"],
        "preparation_tips": [
            "Practice reading comprehension",
            "Analyze data quickly",
            "Connect theory to practical situations"
        ]
    }
