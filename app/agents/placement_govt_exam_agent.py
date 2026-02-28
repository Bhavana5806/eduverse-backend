"""
Placement & Government Exam Mastery Agent
Prepares students for Industry 4.0 + All Government Exams
"""

INDUSTRY_4_0_SKILLS = {
    "AI_ML": {
        "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Deep Learning", "NLP", "Computer Vision"],
        "projects": ["Image Classification", "Chatbot", "Recommendation System", "Sentiment Analysis"],
        "certifications": ["TensorFlow Developer", "AWS ML Specialty", "Google ML Engineer"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "NVIDIA"]
    },
    "Cloud_Computing": {
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD"],
        "projects": ["Microservices Architecture", "Serverless App", "Container Orchestration"],
        "certifications": ["AWS Solutions Architect", "Azure Administrator", "GCP Professional"],
        "companies": ["Amazon", "Microsoft", "Google", "IBM", "Oracle"]
    },
    "Data_Science": {
        "skills": ["Python", "R", "SQL", "Pandas", "NumPy", "Tableau", "Power BI", "Statistics"],
        "projects": ["Data Pipeline", "Dashboard", "Predictive Model", "A/B Testing"],
        "certifications": ["Data Science Professional", "Tableau Certified", "Google Data Analytics"],
        "companies": ["McKinsey", "Deloitte", "Accenture", "Amazon", "Netflix"]
    },
    "Cybersecurity": {
        "skills": ["Network Security", "Ethical Hacking", "Penetration Testing", "SIEM", "Cryptography"],
        "projects": ["Vulnerability Scanner", "Security Audit", "Firewall Configuration"],
        "certifications": ["CEH", "CISSP", "CompTIA Security+", "OSCP"],
        "companies": ["Cisco", "Palo Alto", "CrowdStrike", "Government Agencies"]
    },
    "IoT": {
        "skills": ["Arduino", "Raspberry Pi", "MQTT", "Sensors", "Edge Computing", "5G"],
        "projects": ["Smart Home", "Industrial Automation", "Wearable Device"],
        "certifications": ["IoT Specialist", "AWS IoT", "Cisco IoT"],
        "companies": ["Bosch", "Siemens", "GE", "Samsung", "Intel"]
    },
    "Blockchain": {
        "skills": ["Solidity", "Ethereum", "Smart Contracts", "Web3", "DeFi", "NFT"],
        "projects": ["DApp", "Token Creation", "Smart Contract", "Crypto Wallet"],
        "certifications": ["Blockchain Developer", "Ethereum Developer", "Hyperledger"],
        "companies": ["Coinbase", "Binance", "ConsenSys", "IBM Blockchain"]
    }
}

GOVERNMENT_EXAMS = {
    # Medical Entrance
    "NEET": {
        "full_name": "National Eligibility cum Entrance Test",
        "subjects": ["Physics", "Chemistry", "Biology"],
        "total_questions": 180,
        "duration": 180,
        "negative_marking": -1,
        "syllabus": ["Class 11", "Class 12"],
        "preparation_time": "18-24 months",
        "success_strategy": "NCERT mastery + Previous papers + Mock tests"
    },
    "AIIMS": {
        "full_name": "All India Institute of Medical Sciences",
        "subjects": ["Physics", "Chemistry", "Biology", "General Knowledge"],
        "total_questions": 200,
        "duration": 210,
        "negative_marking": -0.33,
        "preparation_time": "18-24 months",
        "success_strategy": "NCERT + AIIMS previous papers + Current affairs"
    },
    "JIPMER": {
        "full_name": "Jawaharlal Institute of Postgraduate Medical Education",
        "subjects": ["Physics", "Chemistry", "Biology", "English", "Logical Reasoning"],
        "total_questions": 200,
        "duration": 150,
        "negative_marking": -0.33,
        "preparation_time": "18-24 months",
        "success_strategy": "Speed + Accuracy + NCERT mastery"
    },
    
    # Engineering Entrance
    "JEE_Main": {
        "full_name": "Joint Entrance Examination Main",
        "subjects": ["Physics", "Chemistry", "Mathematics"],
        "total_questions": 90,
        "duration": 180,
        "negative_marking": -1,
        "syllabus": ["Class 11", "Class 12"],
        "preparation_time": "18-24 months",
        "success_strategy": "Concept clarity + Problem solving + Time management"
    },
    "JEE_Advanced": {
        "full_name": "Joint Entrance Examination Advanced",
        "subjects": ["Physics", "Chemistry", "Mathematics"],
        "total_questions": 54,
        "duration": 180,
        "negative_marking": "Partial",
        "syllabus": ["Class 11", "Class 12"],
        "preparation_time": "After JEE Main",
        "success_strategy": "Advanced problem solving + IIT previous papers"
    },
    "BITSAT": {
        "full_name": "Birla Institute of Technology and Science Admission Test",
        "subjects": ["Physics", "Chemistry", "Mathematics", "English", "Logical Reasoning"],
        "total_questions": 150,
        "duration": 180,
        "negative_marking": -1,
        "preparation_time": "12 months"
    },
    "VITEEE": {
        "full_name": "VIT Engineering Entrance Examination",
        "subjects": ["Physics", "Chemistry", "Mathematics", "English"],
        "total_questions": 125,
        "duration": 150,
        "preparation_time": "6-12 months"
    },
    
    # Civil Services
    "UPSC_CSE": {
        "full_name": "Union Public Service Commission Civil Services",
        "subjects": ["General Studies", "Optional Subject", "Essay", "Interview"],
        "stages": ["Prelims", "Mains", "Interview"],
        "preparation_time": "12-18 months",
        "success_strategy": "NCERT + Current affairs + Answer writing + Ethics"
    },
    "TNPSC_Group1": {
        "full_name": "Tamil Nadu Public Service Commission Group 1",
        "subjects": ["General Studies", "Aptitude", "Tamil"],
        "preparation_time": "12 months",
        "success_strategy": "TN specific GK + Previous papers + Current affairs"
    },
    "TNPSC_Group2": {
        "full_name": "Tamil Nadu PSC Group 2",
        "subjects": ["General Studies", "Aptitude"],
        "preparation_time": "8-10 months"
    },
    "TNPSC_Group4": {
        "full_name": "Tamil Nadu PSC Group 4",
        "subjects": ["General Studies", "Aptitude", "Tamil"],
        "preparation_time": "6 months"
    },
    
    # Central Government
    "SSC_CGL": {
        "full_name": "Staff Selection Commission Combined Graduate Level",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness"],
        "tiers": ["Tier 1", "Tier 2", "Tier 3"],
        "preparation_time": "6-12 months",
        "success_strategy": "Speed + Accuracy + Previous papers"
    },
    "SSC_CHSL": {
        "full_name": "SSC Combined Higher Secondary Level",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness"],
        "preparation_time": "4-6 months"
    },
    "SSC_MTS": {
        "full_name": "SSC Multi Tasking Staff",
        "subjects": ["Reasoning", "Numerical Ability", "General Awareness", "English"],
        "preparation_time": "3-4 months"
    },
    "SSC_GD": {
        "full_name": "SSC General Duty Constable",
        "subjects": ["Reasoning", "Numerical Ability", "General Awareness", "English"],
        "preparation_time": "3-4 months"
    },
    
    # Banking
    "IBPS_PO": {
        "full_name": "Institute of Banking Personnel Selection PO",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness", "Computer"],
        "stages": ["Prelims", "Mains", "Interview"],
        "preparation_time": "6-9 months",
        "success_strategy": "Banking awareness + Speed + Mock tests"
    },
    "IBPS_Clerk": {
        "full_name": "IBPS Clerk",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness", "Computer"],
        "preparation_time": "4-6 months"
    },
    "SBI_PO": {
        "full_name": "State Bank of India Probationary Officer",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness", "Computer"],
        "preparation_time": "6-9 months"
    },
    "SBI_Clerk": {
        "full_name": "SBI Clerk",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness", "Computer"],
        "preparation_time": "4-6 months"
    },
    "RBI_Grade_B": {
        "full_name": "Reserve Bank of India Grade B",
        "subjects": ["General Awareness", "English", "Quantitative", "Reasoning", "Economic & Social Issues"],
        "preparation_time": "9-12 months"
    },
    
    # Railway
    "RRB_NTPC": {
        "full_name": "Railway Non-Technical Popular Categories",
        "subjects": ["Mathematics", "Reasoning", "General Science", "General Awareness"],
        "preparation_time": "4-6 months",
        "success_strategy": "Railway specific GK + Speed + Previous papers"
    },
    "RRB_JE": {
        "full_name": "Railway Junior Engineer",
        "subjects": ["Mathematics", "Reasoning", "General Science", "Technical"],
        "preparation_time": "6 months"
    },
    "RRB_Group_D": {
        "full_name": "Railway Group D",
        "subjects": ["Mathematics", "Reasoning", "General Science", "General Awareness"],
        "preparation_time": "3-4 months"
    },
    
    # Defense
    "NDA": {
        "full_name": "National Defence Academy",
        "subjects": ["Mathematics", "General Ability Test"],
        "stages": ["Written", "SSB Interview"],
        "preparation_time": "12 months"
    },
    "CDS": {
        "full_name": "Combined Defence Services",
        "subjects": ["English", "General Knowledge", "Elementary Mathematics"],
        "preparation_time": "6-9 months"
    },
    "AFCAT": {
        "full_name": "Air Force Common Admission Test",
        "subjects": ["General Awareness", "Verbal Ability", "Numerical Ability", "Reasoning"],
        "preparation_time": "6 months"
    },
    
    # Teaching
    "CTET": {
        "full_name": "Central Teacher Eligibility Test",
        "subjects": ["Child Development", "Language", "Mathematics", "EVS", "Social Studies"],
        "preparation_time": "3-4 months"
    },
    "UGC_NET": {
        "full_name": "University Grants Commission NET",
        "subjects": ["Teaching Aptitude", "Research Aptitude", "Subject Specific"],
        "preparation_time": "6-9 months"
    },
    
    # Insurance
    "LIC_AAO": {
        "full_name": "Life Insurance Corporation Assistant Administrative Officer",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness", "Insurance"],
        "preparation_time": "6 months"
    },
    "NIACL_AO": {
        "full_name": "National Insurance Academy Assistant Officer",
        "subjects": ["Reasoning", "Quantitative", "English", "General Awareness"],
        "preparation_time": "4-6 months"
    },
    
    # Police & Law
    "CLAT": {
        "full_name": "Common Law Admission Test",
        "subjects": ["English", "Current Affairs", "Legal Reasoning", "Logical Reasoning", "Quantitative"],
        "preparation_time": "12 months"
    },
    "State_Police": {
        "full_name": "State Police Constable/SI",
        "subjects": ["Reasoning", "Numerical Ability", "General Knowledge", "State GK"],
        "preparation_time": "4-6 months"
    },
    
    # Others
    "GATE": {
        "full_name": "Graduate Aptitude Test in Engineering",
        "subjects": ["Engineering Mathematics", "General Aptitude", "Technical Subject"],
        "preparation_time": "6-9 months"
    },
    "CAT": {
        "full_name": "Common Admission Test",
        "subjects": ["Verbal Ability", "Data Interpretation", "Logical Reasoning", "Quantitative Ability"],
        "preparation_time": "9-12 months"
    },
    "NIFT": {
        "full_name": "National Institute of Fashion Technology",
        "subjects": ["General Ability", "Creative Ability", "Situation Test"],
        "preparation_time": "6-9 months"
    }
}

def generate_placement_roadmap(student_profile: dict, target_domain: str) -> dict:
    """Generate complete placement preparation roadmap"""
    
    domain_data = INDUSTRY_4_0_SKILLS.get(target_domain, {})
    
    if not domain_data:
        return {"error": "Domain not found"}
    
    current_skills = student_profile.get("skills", [])
    required_skills = domain_data["skills"]
    
    skill_gaps = list(set(required_skills) - set(current_skills))
    
    roadmap = {
        "target_domain": target_domain,
        "timeline": "6 months intensive",
        "phases": []
    }
    
    # Phase 1: Skill Development (3 months)
    roadmap["phases"].append({
        "phase": 1,
        "name": "Skill Mastery",
        "duration": "3 months",
        "focus": skill_gaps[:5],
        "daily_hours": 6,
        "activities": [
            "Online courses (Coursera, Udemy)",
            "Hands-on projects",
            "Daily coding practice",
            "Documentation reading"
        ]
    })
    
    # Phase 2: Project Building (2 months)
    roadmap["phases"].append({
        "phase": 2,
        "name": "Portfolio Development",
        "duration": "2 months",
        "projects": domain_data["projects"],
        "activities": [
            "Build 3-4 industry-level projects",
            "GitHub portfolio",
            "Technical blog writing",
            "Open source contributions"
        ]
    })
    
    # Phase 3: Interview Prep (1 month)
    roadmap["phases"].append({
        "phase": 3,
        "name": "Interview Mastery",
        "duration": "1 month",
        "activities": [
            "DSA practice (LeetCode 200+ problems)",
            "System design study",
            "Mock interviews",
            "Resume optimization",
            "LinkedIn profile building"
        ]
    })
    
    roadmap["certifications"] = domain_data["certifications"]
    roadmap["target_companies"] = domain_data["companies"]
    roadmap["expected_package"] = "8-15 LPA for freshers"
    
    return roadmap

def generate_govt_exam_strategy(exam_name: str, student_profile: dict) -> dict:
    """Generate comprehensive government exam preparation strategy"""
    
    exam_data = GOVERNMENT_EXAMS.get(exam_name, {})
    
    if not exam_data:
        return {"error": "Exam not found"}
    
    strategy = {
        "exam": exam_name,
        "full_name": exam_data.get("full_name", ""),
        "preparation_plan": []
    }
    
    # Get preparation time
    prep_time = exam_data.get("preparation_time", "12 months")
    
    # Phase-wise strategy
    if "NEET" in exam_name or "JEE" in exam_name or "AIIMS" in exam_name or "JIPMER" in exam_name:
        strategy["preparation_plan"] = [
            {
                "phase": "Foundation (6 months)",
                "focus": "NCERT complete + Concept clarity",
                "daily_hours": 8,
                "subjects": exam_data["subjects"]
            },
            {
                "phase": "Advanced (6 months)",
                "focus": "Reference books + Problem solving",
                "daily_hours": 10,
                "resources": ["HC Verma", "RD Sharma", "Trueman's Biology"]
            },
            {
                "phase": "Revision (4 months)",
                "focus": "Previous papers + Mock tests",
                "daily_hours": 12,
                "target": "50+ mock tests"
            },
            {
                "phase": "Final Sprint (2 months)",
                "focus": "Weak topics + Speed + Accuracy",
                "daily_hours": 14,
                "strategy": "Exam simulation daily"
            }
        ]
    
    elif "UPSC" in exam_name or "TNPSC" in exam_name:
        strategy["preparation_plan"] = [
            {
                "phase": "Foundation (4 months)",
                "focus": "NCERT Class 6-12 + Basic books",
                "daily_hours": 6
            },
            {
                "phase": "Advanced (6 months)",
                "focus": "Standard books + Current affairs",
                "daily_hours": 8,
                "resources": ["Laxmikanth", "Spectrum", "The Hindu"]
            },
            {
                "phase": "Answer Writing (2 months)",
                "focus": "Mains preparation + Essay",
                "daily_hours": 6,
                "practice": "Daily answer writing"
            }
        ]
    
    else:  # SSC, Banking, Railway
        strategy["preparation_plan"] = [
            {
                "phase": "Basics (2 months)",
                "focus": "Fundamentals of all subjects",
                "daily_hours": 4
            },
            {
                "phase": "Practice (3 months)",
                "focus": "Topic-wise practice + Speed",
                "daily_hours": 6,
                "target": "1000+ questions"
            },
            {
                "phase": "Mock Tests (1 month)",
                "focus": "Full-length tests + Analysis",
                "daily_hours": 8,
                "target": "30+ mock tests"
            }
        ]
    
    strategy["success_strategy"] = exam_data.get("success_strategy", "")
    strategy["exam_pattern"] = {
        "subjects": exam_data.get("subjects", []),
        "total_questions": exam_data.get("total_questions", "Varies"),
        "duration": exam_data.get("duration", "Varies"),
        "negative_marking": exam_data.get("negative_marking", "Yes")
    }
    
    return strategy

def get_all_exam_options() -> dict:
    """Get complete list of all supported exams"""
    return {
        "medical": ["NEET", "AIIMS", "JIPMER"],
        "engineering": ["JEE_Main", "JEE_Advanced"],
        "civil_services": ["UPSC_CSE", "TNPSC"],
        "central_govt": ["SSC_CGL", "Railway_RRB", "Banking_PO"],
        "total_exams": len(GOVERNMENT_EXAMS),
        "all_exams": list(GOVERNMENT_EXAMS.keys())
    }

def generate_dual_preparation_plan(placement_domain: str, govt_exam: str) -> dict:
    """Prepare for both placement AND government exam simultaneously"""
    
    return {
        "strategy": "Dual Track Preparation",
        "morning_session": {
            "time": "6 AM - 10 AM",
            "focus": f"Government Exam ({govt_exam})",
            "activities": ["Subject study", "Previous papers", "Current affairs"]
        },
        "afternoon_session": {
            "time": "2 PM - 6 PM",
            "focus": f"Placement Prep ({placement_domain})",
            "activities": ["Coding practice", "Projects", "Skill development"]
        },
        "evening_session": {
            "time": "7 PM - 10 PM",
            "focus": "Revision + Mock Tests",
            "activities": ["Both tracks revision", "Mock tests", "Analysis"]
        },
        "success_rate": "70% with disciplined approach",
        "timeline": "12 months intensive"
    }

def get_industry_4_0_domains() -> dict:
    """Get all Industry 4.0 domains"""
    return {
        "domains": list(INDUSTRY_4_0_SKILLS.keys()),
        "total_domains": len(INDUSTRY_4_0_SKILLS),
        "trending": ["AI_ML", "Cloud_Computing", "Data_Science", "Cybersecurity"]
    }


# NxtWave-Style Training Methodology
NXTWAVE_TRAINING_MODEL = {
    "philosophy": "Industry 4.0 Ready + 100% Placement Focused",
    "unique_features": [
        "Live coding sessions",
        "Real-world projects",
        "Industry mentorship",
        "Interview guarantee",
        "Placement assistance",
        "Continuous assessment"
    ],
    "training_tracks": {
        "CCBP_4_0": {
            "name": "Certified Coding & Backend Professional 4.0",
            "duration": "12 months",
            "modules": [
                "Python Programming",
                "Data Structures & Algorithms",
                "Database Management",
                "Backend Development",
                "System Design",
                "DevOps Basics"
            ],
            "projects": 15,
            "assessments": 50,
            "mock_interviews": 10,
            "guaranteed_package": "4-8 LPA"
        },
        "Full_Stack": {
            "name": "Full Stack Development",
            "duration": "10 months",
            "modules": [
                "HTML/CSS/JavaScript",
                "React.js",
                "Node.js",
                "MongoDB",
                "REST APIs",
                "Deployment"
            ],
            "projects": 12,
            "guaranteed_package": "5-10 LPA"
        },
        "Data_Science": {
            "name": "Data Science & AI",
            "duration": "12 months",
            "modules": [
                "Python",
                "Statistics",
                "Machine Learning",
                "Deep Learning",
                "NLP",
                "Computer Vision"
            ],
            "projects": 10,
            "guaranteed_package": "6-12 LPA"
        }
    }
}

def generate_nxtwave_style_training(domain: str, student_level: str) -> dict:
    """Generate NxtWave-style comprehensive training plan"""
    
    training = {
        "program": f"EduVerse {domain} Mastery Program",
        "methodology": "Learn by Doing - Industry 4.0 Ready",
        "structure": {
            "daily_schedule": {
                "morning": "Live coding session (2 hours)",
                "afternoon": "Self-paced learning (3 hours)",
                "evening": "Project work (2 hours)",
                "night": "Practice & revision (1 hour)"
            },
            "weekly_structure": {
                "monday_friday": "New concepts + coding",
                "saturday": "Project building",
                "sunday": "Assessment + mock interview"
            }
        },
        "learning_approach": [
            "Watch: Video lectures",
            "Code: Hands-on coding",
            "Build: Real projects",
            "Test: Assessments",
            "Interview: Mock interviews"
        ],
        "support_system": {
            "mentorship": "1-on-1 industry mentor",
            "doubt_clearing": "24/7 support",
            "peer_learning": "Community forum",
            "career_guidance": "Dedicated placement team"
        },
        "assessment_model": {
            "daily_quizzes": True,
            "weekly_tests": True,
            "monthly_projects": True,
            "final_capstone": True,
            "continuous_evaluation": True
        },
        "placement_preparation": {
            "resume_building": "Professional resume",
            "linkedin_optimization": "Profile building",
            "mock_interviews": "10+ sessions",
            "aptitude_training": "Quantitative + Logical",
            "soft_skills": "Communication + Presentation",
            "company_specific_prep": "Target company training"
        },
        "guaranteed_outcomes": {
            "skills_mastered": f"{domain} industry-ready skills",
            "projects_completed": "10-15 real-world projects",
            "interview_ready": "100% placement assistance",
            "expected_package": "4-12 LPA based on performance"
        }
    }
    
    return training

def get_complete_exam_list() -> dict:
    """Get categorized list of ALL 40+ exams"""
    return {
        "total_exams": len(GOVERNMENT_EXAMS),
        "categories": {
            "Medical": ["NEET", "AIIMS", "JIPMER"],
            "Engineering": ["JEE_Main", "JEE_Advanced", "BITSAT", "VITEEE", "GATE"],
            "Civil_Services": ["UPSC_CSE", "TNPSC_Group1", "TNPSC_Group2", "TNPSC_Group4"],
            "SSC": ["SSC_CGL", "SSC_CHSL", "SSC_MTS", "SSC_GD"],
            "Banking": ["IBPS_PO", "IBPS_Clerk", "SBI_PO", "SBI_Clerk", "RBI_Grade_B"],
            "Railway": ["RRB_NTPC", "RRB_JE", "RRB_Group_D"],
            "Defense": ["NDA", "CDS", "AFCAT"],
            "Teaching": ["CTET", "UGC_NET"],
            "Insurance": ["LIC_AAO", "NIACL_AO"],
            "Law": ["CLAT", "State_Police"],
            "Management": ["CAT"],
            "Others": ["NIFT"]
        },
        "all_exams": list(GOVERNMENT_EXAMS.keys())
    }
