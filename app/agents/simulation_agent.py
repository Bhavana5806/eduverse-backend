"""
Engine 3: Hybrid Simulation Intelligence Engine
Provides experiential learning through adaptive simulations
"""

SIMULATION_MODULES = {
    "chemistry_lab": {
        "name": "Chemistry Virtual Lab",
        "topics": ["Acids & Bases", "Chemical Reactions", "Titration"],
        "parameters": ["temperature", "concentration", "volume"]
    },
    "physics_motion": {
        "name": "Physics Motion Simulator",
        "topics": ["Kinematics", "Projectile Motion", "Circular Motion"],
        "parameters": ["velocity", "acceleration", "angle"]
    },
    "math_graph": {
        "name": "Math Graph Visualizer",
        "topics": ["Linear Functions", "Quadratic Functions", "Trigonometry"],
        "parameters": ["slope", "intercept", "amplitude"]
    },
    "ds_visualizer": {
        "name": "Data Structures Visualizer",
        "topics": ["Arrays", "Trees", "Graphs", "Sorting"],
        "parameters": ["size", "operation", "speed"]
    },
    "neural_network": {
        "name": "Neural Network Simulator",
        "topics": ["Perceptron", "Backpropagation", "CNN"],
        "parameters": ["layers", "learning_rate", "epochs"]
    },
    "database_query": {
        "name": "Database Query Visualizer",
        "topics": ["SELECT", "JOIN", "Indexing"],
        "parameters": ["table_size", "query_complexity"]
    },
    "circuit_builder": {
        "name": "Circuit Builder",
        "topics": ["Series Circuit", "Parallel Circuit", "Logic Gates"],
        "parameters": ["voltage", "resistance", "components"]
    }
}

def get_simulation_config(simulation_type: str, student_level: str, language: str):
    """Get adaptive simulation configuration"""
    module = SIMULATION_MODULES.get(simulation_type, SIMULATION_MODULES["math_graph"])
    
    # Adjust difficulty based on student level
    difficulty_map = {
        "Beginner": {"speed": "slow", "guidance": "high", "hints": True},
        "Intermediate": {"speed": "medium", "guidance": "medium", "hints": True},
        "Advanced": {"speed": "fast", "guidance": "low", "hints": False}
    }
    
    config = difficulty_map.get(student_level, difficulty_map["Beginner"])
    
    return {
        "simulation_name": module["name"],
        "topics": module["topics"],
        "parameters": module["parameters"],
        "difficulty": config,
        "language": language,
        "narration_enabled": True,
        "subtitles": True
    }

def adjust_simulation_parameters(student_performance: float, current_difficulty: str):
    """AI-controlled parameter adjustment"""
    if student_performance >= 80:
        # Increase difficulty
        return {
            "action": "increase_difficulty",
            "new_speed": "faster",
            "new_guidance": "reduced",
            "message": "Great progress! Increasing challenge level."
        }
    elif student_performance < 50:
        # Decrease difficulty
        return {
            "action": "decrease_difficulty",
            "new_speed": "slower",
            "new_guidance": "increased",
            "message": "Let's slow down and add more guidance."
        }
    else:
        return {
            "action": "maintain",
            "message": "Continue at current pace."
        }

def generate_reinforcement_test(simulation_type: str, topic: str):
    """Generate quick test after simulation"""
    return {
        "test_type": "reinforcement",
        "topic": topic,
        "questions": [
            {
                "id": 1,
                "question": f"Apply what you learned in {topic}",
                "type": "practical",
                "difficulty": "medium"
            },
            {
                "id": 2,
                "question": f"Explain the concept of {topic}",
                "type": "conceptual",
                "difficulty": "easy"
            }
        ],
        "time_limit": 300,  # 5 minutes
        "passing_score": 70
    }

def calculate_mastery_score(simulation_attempts: int, test_score: float, time_efficiency: float):
    """Calculate overall mastery score"""
    attempt_penalty = max(0, (simulation_attempts - 1) * 5)
    mastery = (test_score * 0.7 + time_efficiency * 0.3) - attempt_penalty
    
    return {
        "mastery_score": max(0, min(100, mastery)),
        "level": "Mastered" if mastery >= 80 else "Proficient" if mastery >= 60 else "Learning",
        "recommendation": "Move to next topic" if mastery >= 80 else "Practice more"
    }
