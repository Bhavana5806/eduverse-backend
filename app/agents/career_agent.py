"""
Engine 7: Career Intelligence & Global Demand Engine
Career path recommendation based on skills and global trends
"""

CAREER_DATABASE = {
    "Software Engineer": {
        "required_skills": ["Programming", "Data Structures", "Algorithms", "Problem Solving"],
        "demand": "Very High",
        "avg_salary": "$95,000",
        "growth_rate": "22%",
        "certifications": ["AWS Certified", "Google Cloud", "Azure"],
        "education": ["Computer Science", "Software Engineering", "IT"]
    },
    "Data Scientist": {
        "required_skills": ["Statistics", "Machine Learning", "Python", "Data Analysis"],
        "demand": "Very High",
        "avg_salary": "$120,000",
        "growth_rate": "31%",
        "certifications": ["TensorFlow", "Data Science Professional", "ML Specialization"],
        "education": ["Computer Science", "Statistics", "Mathematics"]
    },
    "AI/ML Engineer": {
        "required_skills": ["Deep Learning", "Neural Networks", "Python", "Mathematics"],
        "demand": "Extremely High",
        "avg_salary": "$130,000",
        "growth_rate": "40%",
        "certifications": ["Deep Learning Specialization", "AI Engineer", "MLOps"],
        "education": ["Computer Science", "AI", "Mathematics"]
    },
    "Mechanical Engineer": {
        "required_skills": ["CAD", "Thermodynamics", "Mechanics", "Design"],
        "demand": "High",
        "avg_salary": "$85,000",
        "growth_rate": "7%",
        "certifications": ["PE License", "Six Sigma", "AutoCAD"],
        "education": ["Mechanical Engineering"]
    },
    "Civil Engineer": {
        "required_skills": ["Structural Analysis", "CAD", "Project Management"],
        "demand": "High",
        "avg_salary": "$82,000",
        "growth_rate": "8%",
        "certifications": ["PE License", "PMP", "LEED"],
        "education": ["Civil Engineering"]
    },
    "Doctor": {
        "required_skills": ["Medical Knowledge", "Diagnosis", "Patient Care", "Communication"],
        "demand": "Very High",
        "avg_salary": "$200,000",
        "growth_rate": "18%",
        "certifications": ["Medical License", "Board Certification", "Specialization"],
        "education": ["MBBS", "MD", "Medical Science"]
    },
    "Financial Analyst": {
        "required_skills": ["Finance", "Excel", "Data Analysis", "Economics"],
        "demand": "High",
        "avg_salary": "$85,000",
        "growth_rate": "6%",
        "certifications": ["CFA", "FRM", "CPA"],
        "education": ["Finance", "Economics", "Business"]
    }
}

GOVERNMENT_EXAMS = {
    "UPSC": {
        "positions": ["IAS", "IPS", "IFS"],
        "subjects": ["General Studies", "Optional Subject", "Essay"],
        "preparation_time": "12-18 months"
    },
    "SSC": {
        "positions": ["Tax Assistant", "Inspector", "Auditor"],
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness"],
        "preparation_time": "6-12 months"
    },
    "Banking": {
        "positions": ["PO", "Clerk", "SO"],
        "subjects": ["Reasoning", "Quantitative", "English", "Banking Awareness"],
        "preparation_time": "6-9 months"
    }
}

def analyze_career_fit(student_interests: list, student_strengths: list, performance_data: dict):
    """Analyze career fit based on student profile"""
    career_matches = []
    
    for career, details in CAREER_DATABASE.items():
        match_score = 0
        required_skills = details["required_skills"]
        
        # Calculate match based on interests and strengths
        interest_match = len(set(student_interests) & set(required_skills)) / len(required_skills)
        strength_match = len(set(student_strengths) & set(required_skills)) / len(required_skills)
        
        match_score = (interest_match * 0.4 + strength_match * 0.6) * 100
        
        if match_score >= 40:  # Threshold for recommendation
            career_matches.append({
                "career": career,
                "match_score": round(match_score, 2),
                "demand": details["demand"],
                "avg_salary": details["avg_salary"],
                "growth_rate": details["growth_rate"],
                "required_skills": required_skills,
                "education_path": details["education"]
            })
    
    # Sort by match score
    career_matches.sort(key=lambda x: x["match_score"], reverse=True)
    
    return career_matches

def identify_skill_gaps(target_career: str, current_skills: list):
    """Identify skill gaps for target career"""
    career_data = CAREER_DATABASE.get(target_career)
    
    if not career_data:
        return {"error": "Career not found"}
    
    required_skills = set(career_data["required_skills"])
    current_skills_set = set(current_skills)
    
    skill_gaps = list(required_skills - current_skills_set)
    existing_skills = list(required_skills & current_skills_set)
    
    return {
        "target_career": target_career,
        "required_skills": list(required_skills),
        "existing_skills": existing_skills,
        "skill_gaps": skill_gaps,
        "completion_percentage": round((len(existing_skills) / len(required_skills)) * 100, 2)
    }

def generate_learning_roadmap(target_career: str, skill_gaps: list):
    """Generate personalized learning roadmap"""
    career_data = CAREER_DATABASE.get(target_career, {})
    
    roadmap = {
        "target_career": target_career,
        "estimated_time": f"{len(skill_gaps) * 2} months",
        "phases": []
    }
    
    for i, skill in enumerate(skill_gaps):
        roadmap["phases"].append({
            "phase": i + 1,
            "skill": skill,
            "duration": "2 months",
            "resources": [
                {"type": "course", "name": f"{skill} Fundamentals"},
                {"type": "practice", "name": f"{skill} Projects"},
                {"type": "certification", "name": f"{skill} Certification"}
            ],
            "milestones": [
                f"Complete {skill} basics",
                f"Build {skill} project",
                f"Pass {skill} assessment"
            ]
        })
    
    roadmap["certifications"] = career_data.get("certifications", [])
    
    return roadmap

def recommend_higher_studies(current_education: str, target_career: str):
    """Recommend higher studies options"""
    career_data = CAREER_DATABASE.get(target_career, {})
    required_education = career_data.get("education", [])
    
    recommendations = {
        "target_career": target_career,
        "current_education": current_education,
        "recommended_programs": [],
        "universities": []
    }
    
    for edu in required_education:
        if edu not in current_education:
            recommendations["recommended_programs"].append({
                "program": edu,
                "degree_type": "Masters" if "Bachelor" in current_education else "Bachelor",
                "duration": "2 years",
                "relevance": "High"
            })
    
    return recommendations

def suggest_government_exam_path(student_interests: list, education_background: str):
    """Suggest suitable government exams"""
    suggestions = []
    
    for exam, details in GOVERNMENT_EXAMS.items():
        suggestions.append({
            "exam": exam,
            "positions": details["positions"],
            "subjects": details["subjects"],
            "preparation_time": details["preparation_time"],
            "suitability": "High" if any(interest in str(details) for interest in student_interests) else "Medium"
        })
    
    return suggestions

def analyze_placement_readiness(student_skills: list, target_companies: list):
    """Analyze placement readiness"""
    required_skills_by_tier = {
        "Tier1": ["Data Structures", "Algorithms", "System Design", "Problem Solving", "Communication"],
        "Tier2": ["Programming", "Data Structures", "Algorithms", "Problem Solving"],
        "Tier3": ["Programming", "Basic CS Concepts", "Communication"]
    }
    
    readiness = {}
    
    for tier, required in required_skills_by_tier.items():
        match_count = len(set(student_skills) & set(required))
        readiness[tier] = {
            "readiness_percentage": round((match_count / len(required)) * 100, 2),
            "missing_skills": list(set(required) - set(student_skills)),
            "status": "Ready" if match_count >= len(required) * 0.8 else "Needs Preparation"
        }
    
    return {
        "overall_readiness": readiness,
        "recommendation": "Focus on missing skills before applying",
        "estimated_preparation_time": f"{len(readiness['Tier1']['missing_skills']) * 1} months"
    }
