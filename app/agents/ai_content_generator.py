"""
AI Content Generation Agent using Google Gemini
Generates lectures, notes, questions, simulations autonomously
"""

import google.generativeai as genai
import os
from typing import List, Dict

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_lecture_content(topic: str, level: str, language: str = "English") -> Dict:
    """Autonomously generate lecture content for any topic"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create a comprehensive lecture on: {topic}
    Level: {level}
    Language: {language}
    
    Include:
    1. Introduction (2-3 paragraphs)
    2. Key Concepts (5-7 points)
    3. Detailed Explanation
    4. Real-world Examples
    5. Common Misconceptions
    6. Summary
    
    Make it engaging and easy to understand.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "topic": topic,
        "level": level,
        "language": language,
        "content": response.text,
        "type": "lecture"
    }

def generate_study_notes(topic: str, level: str) -> Dict:
    """Auto-generate comprehensive study notes"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create detailed study notes for: {topic}
    Level: {level}
    
    Format:
    1. Topic Overview
    2. Key Definitions
    3. Important Formulas/Concepts
    4. Step-by-step Explanations
    5. Tips and Tricks
    6. Practice Points
    
    Make it concise but comprehensive.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "topic": topic,
        "notes": response.text,
        "format": "markdown"
    }

def generate_questions(topic: str, difficulty: str, count: int = 10) -> List[Dict]:
    """Autonomously generate assessment questions"""
    
    if not GEMINI_API_KEY:
        return [{"error": "Gemini API key not configured"}]
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Generate {count} {difficulty} level questions on: {topic}
    
    For each question provide:
    1. Question text
    2. 4 options (A, B, C, D)
    3. Correct answer
    4. Explanation
    
    Format as JSON array.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "topic": topic,
        "difficulty": difficulty,
        "questions": response.text,
        "count": count
    }

def generate_simulation_description(topic: str, subject: str) -> Dict:
    """Generate simulation parameters and description"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Design an interactive simulation for: {topic} in {subject}
    
    Provide:
    1. Simulation objective
    2. Variables to control
    3. Expected outcomes
    4. Step-by-step procedure
    5. Learning outcomes
    6. Visual elements needed
    
    Make it interactive and educational.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "topic": topic,
        "subject": subject,
        "simulation_design": response.text,
        "type": "interactive"
    }

def generate_complete_syllabus_content(syllabus: List[str], level: str) -> Dict:
    """Autonomously generate complete content for entire syllabus"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    content_map = {}
    
    for topic in syllabus:
        content_map[topic] = {
            "lecture": generate_lecture_content(topic, level),
            "notes": generate_study_notes(topic, level),
            "questions": generate_questions(topic, "Medium", 10),
            "simulation": generate_simulation_description(topic, "General")
        }
    
    return {
        "syllabus": syllabus,
        "level": level,
        "content": content_map,
        "status": "generated"
    }

def autonomous_learning_path(student_profile: Dict, syllabus: List[str]) -> Dict:
    """Create complete autonomous learning path"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    model = genai.GenerativeModel('gemini-pro')
    
    weak_topics = student_profile.get("weak_topics", [])
    strong_topics = student_profile.get("strong_topics", [])
    
    prompt = f"""
    Create a personalized learning path for a student with:
    Weak topics: {weak_topics}
    Strong topics: {strong_topics}
    Full syllabus: {syllabus}
    
    Provide:
    1. Learning sequence (prioritized topics)
    2. Time allocation for each topic
    3. Recommended resources
    4. Assessment checkpoints
    5. Revision strategy
    
    Make it adaptive and personalized.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "student_profile": student_profile,
        "learning_path": response.text,
        "autonomous": True
    }

def generate_video_script(topic: str, duration: int = 10) -> Dict:
    """Generate script for lecture video"""
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create a {duration}-minute video lecture script for: {topic}
    
    Include:
    1. Opening hook (30 seconds)
    2. Introduction (1 minute)
    3. Main content with examples ({duration-3} minutes)
    4. Summary (1 minute)
    5. Call to action (30 seconds)
    
    Add [VISUAL] cues for animations/graphics.
    Make it engaging and clear.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "topic": topic,
        "duration": duration,
        "script": response.text,
        "format": "video"
    }
