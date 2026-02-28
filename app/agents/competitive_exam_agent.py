"""
Engine 5: Competitive & Government Exam Engine
Mock tests, strategy, and rank estimation
"""

import random

EXAM_CONFIGS = {
    "JEE_Main": {
        "total_questions": 90,
        "duration": 180,  # minutes
        "negative_marking": -1,
        "sections": ["Physics", "Chemistry", "Math"],
        "marks_per_question": 4
    },
    "NEET": {
        "total_questions": 180,
        "duration": 180,
        "negative_marking": -1,
        "sections": ["Physics", "Chemistry", "Biology"],
        "marks_per_question": 4
    },
    "UPSC_Prelims": {
        "total_questions": 100,
        "duration": 120,
        "negative_marking": -0.33,
        "sections": ["General Studies", "CSAT"],
        "marks_per_question": 2
    },
    "SSC_CGL": {
        "total_questions": 100,
        "duration": 60,
        "negative_marking": -0.5,
        "sections": ["Reasoning", "Quantitative", "English", "General Awareness"],
        "marks_per_question": 2
    }
}

def generate_mock_test(exam_type: str, difficulty: str, student_weak_topics: list):
    """Generate adaptive mock test"""
    config = EXAM_CONFIGS.get(exam_type)
    
    if not config:
        return {"error": "Exam type not supported"}
    
    # Adjust question distribution based on weaknesses
    questions = []
    weak_topic_count = int(config["total_questions"] * 0.4)  # 40% from weak topics
    
    for i in range(config["total_questions"]):
        if i < weak_topic_count and student_weak_topics:
            topic = random.choice(student_weak_topics)
            question_difficulty = "medium"  # Focus on medium difficulty for weak topics
        else:
            topic = random.choice(config["sections"])
            question_difficulty = difficulty
        
        questions.append({
            "id": i + 1,
            "topic": topic,
            "difficulty": question_difficulty,
            "marks": config["marks_per_question"],
            "negative_marks": config["negative_marking"]
        })
    
    return {
        "exam_type": exam_type,
        "total_questions": config["total_questions"],
        "duration_minutes": config["duration"],
        "questions": questions,
        "instructions": generate_instructions(exam_type, config)
    }

def generate_instructions(exam_type: str, config: dict):
    """Generate exam instructions"""
    return {
        "marking_scheme": f"+{config['marks_per_question']} for correct, {config['negative_marking']} for incorrect",
        "time_management": f"Aim for {config['duration'] / config['total_questions']:.1f} minutes per question",
        "strategy": "Attempt easy questions first, then medium, then hard"
    }

def evaluate_mock_test(answers: list, correct_answers: list, config: dict):
    """Evaluate mock test with detailed analysis"""
    correct_count = 0
    incorrect_count = 0
    unattempted_count = 0
    total_marks = 0
    
    topic_performance = {}
    
    for i, answer in enumerate(answers):
        question = answer.get("question_id")
        user_answer = answer.get("answer")
        correct_answer = correct_answers[i]
        topic = answer.get("topic")
        
        if user_answer is None:
            unattempted_count += 1
        elif user_answer == correct_answer:
            correct_count += 1
            total_marks += config["marks_per_question"]
            topic_performance[topic] = topic_performance.get(topic, {"correct": 0, "total": 0})
            topic_performance[topic]["correct"] += 1
            topic_performance[topic]["total"] += 1
        else:
            incorrect_count += 1
            total_marks += config["negative_marking"]
            topic_performance[topic] = topic_performance.get(topic, {"correct": 0, "total": 0})
            topic_performance[topic]["total"] += 1
    
    accuracy = (correct_count / (correct_count + incorrect_count)) * 100 if (correct_count + incorrect_count) > 0 else 0
    
    return {
        "score": total_marks,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "unattempted": unattempted_count,
        "accuracy": round(accuracy, 2),
        "topic_performance": topic_performance
    }

def analyze_speed_vs_accuracy(time_taken: int, accuracy: float, total_questions: int):
    """Analyze speed vs accuracy trade-off"""
    avg_time_per_question = time_taken / total_questions
    
    if accuracy >= 85 and avg_time_per_question <= 1.5:
        analysis = "Excellent balance of speed and accuracy"
        recommendation = "Maintain current pace"
    elif accuracy >= 85 and avg_time_per_question > 1.5:
        analysis = "High accuracy but slow pace"
        recommendation = "Practice speed drills while maintaining accuracy"
    elif accuracy < 70 and avg_time_per_question <= 1.5:
        analysis = "Fast but compromising accuracy"
        recommendation = "Slow down and focus on accuracy first"
    else:
        analysis = "Needs improvement in both speed and accuracy"
        recommendation = "Practice more mock tests with time management"
    
    return {
        "avg_time_per_question": round(avg_time_per_question, 2),
        "analysis": analysis,
        "recommendation": recommendation,
        "speed_score": min(100, (1.5 / avg_time_per_question) * 100) if avg_time_per_question > 0 else 0
    }

def estimate_rank(score: float, exam_type: str, total_marks: float):
    """Estimate rank based on score"""
    percentage = (score / total_marks) * 100
    
    # Simplified rank estimation (in production, use historical data)
    rank_estimates = {
        "JEE_Main": {
            90: 1000,
            80: 10000,
            70: 50000,
            60: 100000,
            50: 200000
        },
        "NEET": {
            90: 500,
            80: 5000,
            70: 25000,
            60: 75000,
            50: 150000
        }
    }
    
    estimates = rank_estimates.get(exam_type, {90: 100, 80: 1000, 70: 5000, 60: 10000, 50: 20000})
    
    for threshold, rank in sorted(estimates.items(), reverse=True):
        if percentage >= threshold:
            return {
                "estimated_rank": rank,
                "percentile": round(100 - (rank / 1000000) * 100, 2),
                "message": f"Based on {percentage:.1f}%, estimated rank: {rank}"
            }
    
    return {"estimated_rank": 500000, "percentile": 50, "message": "Keep practicing to improve rank"}

def generate_improvement_strategy(weak_areas: list, accuracy: float, speed_score: float):
    """Generate personalized improvement strategy"""
    strategies = []
    
    if accuracy < 70:
        strategies.append({
            "area": "Accuracy",
            "priority": "High",
            "actions": [
                "Review fundamental concepts",
                "Practice topic-wise questions",
                "Analyze mistakes thoroughly"
            ]
        })
    
    if speed_score < 60:
        strategies.append({
            "area": "Speed",
            "priority": "High",
            "actions": [
                "Practice timed mini-tests",
                "Learn shortcut techniques",
                "Improve calculation speed"
            ]
        })
    
    if weak_areas:
        strategies.append({
            "area": "Weak Topics",
            "priority": "Critical",
            "topics": weak_areas,
            "actions": [
                f"Deep dive into {', '.join(weak_areas[:3])}",
                "Complete topic-wise practice sets",
                "Take topic-specific tests"
            ]
        })
    
    return strategies
