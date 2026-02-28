"""
Engine 1: Student Intelligence & Assessment Engine
Diagnoses strengths, weaknesses, and builds dynamic skill profiles
"""

def analyze_assessment(score: float, max_score: float, time_taken: int, difficulty: str):
    percentage = (score / max_score) * 100
    
    # Performance classification
    if percentage >= 90:
        status = "Excellent"
        weakness_detected = False
    elif percentage >= 75:
        status = "Good"
        weakness_detected = False
    elif percentage >= 60:
        status = "Average"
        weakness_detected = True
    elif percentage >= 40:
        status = "Weak"
        weakness_detected = True
    else:
        status = "Critical"
        weakness_detected = True
    
    # Time efficiency analysis
    expected_time = {"Easy": 300, "Medium": 600, "Hard": 900}
    time_efficiency = "Efficient" if time_taken <= expected_time.get(difficulty, 600) else "Needs Improvement"
    
    return {
        "percentage": percentage,
        "status": status,
        "weakness_detected": weakness_detected,
        "time_efficiency": time_efficiency
    }

def generate_weakness_heatmap(assessments: list):
    """Generate weakness heatmap from multiple assessments"""
    topic_scores = {}
    
    for assessment in assessments:
        topic = assessment["topic"]
        percentage = (assessment["score"] / assessment["max_score"]) * 100
        
        if topic not in topic_scores:
            topic_scores[topic] = []
        topic_scores[topic].append(percentage)
    
    heatmap = {}
    for topic, scores in topic_scores.items():
        avg_score = sum(scores) / len(scores)
        if avg_score < 60:
            heatmap[topic] = {"level": "Critical", "score": avg_score, "priority": "High"}
        elif avg_score < 75:
            heatmap[topic] = {"level": "Weak", "score": avg_score, "priority": "Medium"}
        else:
            heatmap[topic] = {"level": "Strong", "score": avg_score, "priority": "Low"}
    
    return heatmap

def build_skill_profile(student_id: int, assessments: list):
    """Build comprehensive skill profile"""
    heatmap = generate_weakness_heatmap(assessments)
    
    weak_topics = [topic for topic, data in heatmap.items() if data["priority"] in ["High", "Medium"]]
    strong_topics = [topic for topic, data in heatmap.items() if data["priority"] == "Low"]
    
    priority_index = sorted(
        [{"topic": topic, "priority": data["priority"], "score": data["score"]} 
         for topic, data in heatmap.items()],
        key=lambda x: x["score"]
    )
    
    return {
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "priority_index": priority_index,
        "overall_performance": sum([d["score"] for d in heatmap.values()]) / len(heatmap) if heatmap else 0
    }
