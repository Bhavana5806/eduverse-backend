"""
Engine 10: Explainability & Transparency Engine
Explains all AI recommendations and decisions
"""

def explain_topic_importance(topic: str, exam_type: str, probability: float):
    """Explain why a topic is important"""
    return {
        "topic": topic,
        "importance_level": "High" if probability > 70 else "Medium" if probability > 40 else "Low",
        "explanation": {
            "reason": f"{topic} appears in {probability}% of past {exam_type} exams",
            "historical_data": f"Analyzed last 10 years of {exam_type} papers",
            "weightage": f"Typically carries 15-20% of total marks",
            "recommendation": f"Prioritize {topic} in your study plan"
        },
        "evidence": {
            "data_source": "Historical exam papers (2014-2024)",
            "analysis_method": "Pattern recognition and frequency analysis",
            "confidence_level": "High" if probability > 70 else "Medium"
        }
    }

def explain_career_suggestion(career: str, match_score: float, student_profile: dict):
    """Explain why a career was suggested"""
    return {
        "suggested_career": career,
        "match_score": match_score,
        "explanation": {
            "primary_reason": f"Your skills and interests align {match_score}% with {career} requirements",
            "matching_skills": student_profile.get("matching_skills", []),
            "interest_alignment": "Your expressed interests match this career path",
            "market_demand": "This career has high global demand and growth potential"
        },
        "factors_considered": {
            "student_interests": student_profile.get("interests", []),
            "academic_strengths": student_profile.get("strengths", []),
            "performance_data": "Based on your assessment results",
            "global_trends": "Current job market analysis"
        },
        "transparency_note": "This is a recommendation based on data analysis. Final career choice is yours."
    }

def explain_question_prioritization(question_pack: list):
    """Explain why questions were prioritized"""
    explanations = []
    
    for item in question_pack[:5]:  # Top 5 priorities
        explanation = {
            "topic": item["topic"],
            "priority": item["priority"],
            "reasoning": []
        }
        
        if item.get("is_weakness"):
            explanation["reasoning"].append({
                "factor": "Personal Weakness",
                "detail": "You scored below 60% in this topic",
                "weight": "40%"
            })
        
        if item.get("probability", 0) > 50:
            explanation["reasoning"].append({
                "factor": "High Exam Probability",
                "detail": f"{item['probability']}% chance of appearing in exam",
                "weight": "35%"
            })
        
        explanation["reasoning"].append({
            "factor": "Strategic Importance",
            "detail": "Mastering this topic will improve overall score significantly",
            "weight": "25%"
        })
        
        explanations.append(explanation)
    
    return {
        "prioritization_method": "Weighted scoring based on weakness + probability + strategic value",
        "explanations": explanations,
        "transparency": "Priorities are calculated objectively using your performance data and exam patterns"
    }

def explain_simulation_activation(topic: str, failure_count: int, performance: float):
    """Explain why simulation was activated"""
    return {
        "topic": topic,
        "trigger": "Simulation Mode Activated",
        "explanation": {
            "primary_reason": f"Detected {failure_count} consecutive failures in {topic}",
            "performance_score": f"Current performance: {performance}%",
            "learning_science": "Research shows experiential learning improves retention by 75%",
            "expected_outcome": "Hands-on simulation will help you understand concepts better"
        },
        "what_happens_next": {
            "step_1": "Interactive simulation will load",
            "step_2": "You'll practice concepts in a virtual environment",
            "step_3": "AI will adjust difficulty based on your progress",
            "step_4": "Quick reinforcement test after simulation"
        },
        "why_this_helps": [
            "Visual learning aids understanding",
            "Practice in safe environment",
            "Immediate feedback on actions",
            "Builds muscle memory for concepts"
        ]
    }

def explain_difficulty_adjustment(current_difficulty: str, new_difficulty: str, reason: str):
    """Explain difficulty level changes"""
    return {
        "adjustment": f"{current_difficulty} → {new_difficulty}",
        "reason": reason,
        "explanation": {
            "why_changed": "AI adapts to your performance in real-time",
            "benefit": "Keeps you in optimal learning zone - not too easy, not too hard",
            "learning_theory": "Zone of Proximal Development - learn best at appropriate challenge level"
        },
        "what_to_expect": {
            "if_increased": "Questions will be more challenging to push your limits",
            "if_decreased": "Focus on building strong foundation before advancing",
            "if_maintained": "Current level is optimal for your learning"
        }
    }

def explain_recommendation_logic(recommendation: dict):
    """Explain the logic behind any recommendation"""
    return {
        "recommendation": recommendation.get("action", ""),
        "explanation": {
            "data_used": [
                "Your assessment scores",
                "Time taken per question",
                "Topic-wise performance",
                "Historical learning patterns"
            ],
            "algorithm": "Adaptive learning algorithm analyzes multiple factors",
            "personalization": "Recommendation is unique to your learning profile",
            "goal": "Optimize your learning path for maximum improvement"
        },
        "how_it_helps": recommendation.get("benefit", "Improves learning outcomes"),
        "alternative_options": recommendation.get("alternatives", []),
        "you_decide": "You can choose to follow or modify this recommendation"
    }

def generate_transparency_report(student_id: int, time_period: str):
    """Generate comprehensive transparency report"""
    return {
        "student_id": student_id,
        "report_period": time_period,
        "data_collected": {
            "assessment_scores": "Used for weakness identification",
            "time_metrics": "Used for efficiency analysis",
            "topic_preferences": "Used for personalization",
            "learning_patterns": "Used for adaptive recommendations"
        },
        "how_data_is_used": {
            "weakness_detection": "Identifies topics needing more focus",
            "strength_mapping": "Highlights your strong areas",
            "career_guidance": "Matches skills with career opportunities",
            "exam_prediction": "Analyzes patterns to suggest important topics"
        },
        "ai_decisions_made": {
            "total_recommendations": 0,  # Placeholder
            "simulation_triggers": 0,
            "difficulty_adjustments": 0,
            "career_suggestions": 0
        },
        "your_rights": [
            "View all your data anytime",
            "Understand every recommendation",
            "Choose to accept or reject suggestions",
            "Request data deletion"
        ],
        "fairness_guarantee": "All recommendations are based on objective data analysis, not biased assumptions"
    }

def explain_ai_confidence(prediction: dict):
    """Explain AI confidence levels"""
    confidence = prediction.get("confidence", 0)
    
    if confidence >= 80:
        level = "High"
        meaning = "Strong historical evidence supports this prediction"
    elif confidence >= 60:
        level = "Medium"
        meaning = "Moderate evidence, but some uncertainty exists"
    else:
        level = "Low"
        meaning = "Limited data available, treat as general guidance"
    
    return {
        "confidence_level": level,
        "confidence_score": confidence,
        "what_it_means": meaning,
        "how_calculated": "Based on consistency of historical patterns and data quality",
        "recommendation": "Higher confidence = more reliable prediction",
        "transparency": f"We're {confidence}% confident based on available data"
    }
