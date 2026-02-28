"""
Engine 2: Foundation Rebuilding Engine
Breaks down weak concepts and provides step-by-step learning
"""

CONCEPT_BREAKDOWN = {
    "Algebra": {
        "micro_concepts": ["Variables", "Equations", "Linear Equations", "Quadratic Equations"],
        "prerequisites": ["Basic Arithmetic", "Number Systems"]
    },
    "Calculus": {
        "micro_concepts": ["Limits", "Derivatives", "Integration", "Applications"],
        "prerequisites": ["Algebra", "Trigonometry"]
    },
    "Data Structures": {
        "micro_concepts": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs"],
        "prerequisites": ["Programming Basics", "Complexity Analysis"]
    }
}

def breakdown_concept(topic: str):
    """Break down topic into micro-concepts"""
    concept_data = CONCEPT_BREAKDOWN.get(topic, {
        "micro_concepts": [f"{topic} - Basics", f"{topic} - Intermediate", f"{topic} - Advanced"],
        "prerequisites": ["Foundational Knowledge"]
    })
    
    return concept_data

def generate_learning_path(weak_topic: str, current_level: str):
    """Generate step-by-step learning path"""
    breakdown = breakdown_concept(weak_topic)
    
    learning_steps = []
    for i, concept in enumerate(breakdown["micro_concepts"]):
        learning_steps.append({
            "step": i + 1,
            "concept": concept,
            "mode": "Beginner" if current_level == "Weak" else "Intermediate",
            "resources": [
                {"type": "video", "title": f"Introduction to {concept}"},
                {"type": "text", "title": f"{concept} - Detailed Explanation"},
                {"type": "practice", "title": f"{concept} - Practice Problems"}
            ]
        })
    
    return {
        "topic": weak_topic,
        "prerequisites": breakdown["prerequisites"],
        "learning_path": learning_steps,
        "estimated_time": len(learning_steps) * 30  # 30 mins per concept
    }

def check_simulation_trigger(failure_count: int, topic: str):
    """Check if simulation should be triggered"""
    if failure_count >= 2:
        return {
            "trigger_simulation": True,
            "simulation_type": get_simulation_type(topic),
            "reason": "Repeated failure detected - experiential learning recommended"
        }
    return {"trigger_simulation": False}

def get_simulation_type(topic: str):
    """Map topic to appropriate simulation"""
    simulation_map = {
        "Chemistry": "virtual_lab",
        "Physics": "motion_simulator",
        "Algebra": "graph_visualizer",
        "Data Structures": "ds_visualizer",
        "Circuits": "circuit_builder"
    }
    return simulation_map.get(topic, "interactive_tutorial")

def generate_visual_explanation(topic: str):
    """Generate visual explanation resources"""
    return {
        "diagrams": [f"{topic}_diagram_1.png", f"{topic}_diagram_2.png"],
        "animations": [f"{topic}_animation.mp4"],
        "interactive": f"{topic}_interactive_demo"
    }
