"""
AI Content Generation Service for EduVerse AI
Generates educational content, explanations, and interactive materials using Google Generative AI
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any
import logging
import json
from datetime import datetime
from app.core.config import settings
from app.db.enhanced_models import ContentRepository
from app.db.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

class AIContentGenerator:
    """AI-powered content generation service"""
    
    def __init__(self):
        """Initialize the AI content generator"""
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.vision_model = genai.GenerativeModel('gemini-pro-vision')
            logger.info("AI Content Generator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Content Generator: {str(e)}")
            raise
    
    def generate_explanation(self, topic: str, difficulty: str, language: str = "English") -> Dict[str, Any]:
        """Generate detailed explanation for a topic"""
        try:
            prompt = f"""
            Generate a comprehensive explanation for the topic: {topic}
            
            Requirements:
            - Difficulty level: {difficulty}
            - Target language: {language}
            - Include real-world examples and analogies
            - Break down complex concepts into simple steps
            - Provide visual description suggestions
            - Include common misconceptions and how to avoid them
            - Format as educational content suitable for students
            
            Output format:
            {{
                "title": "Topic Title",
                "introduction": "Brief introduction",
                "explanation": "Detailed explanation with examples",
                "visual_descriptions": ["Description 1", "Description 2"],
                "examples": [
                    {{
                        "title": "Example Title",
                        "description": "Example description",
                        "solution": "Step-by-step solution"
                    }}
                ],
                "common_mistakes": ["Mistake 1", "Mistake 2"],
                "summary": "Key takeaways"
            }}
            """
            
            response = self.model.generate_content(prompt)
            content = json.loads(response.text)
            
            return {
                "success": True,
                "content": content,
                "metadata": {
                    "topic": topic,
                    "difficulty": difficulty,
                    "language": language,
                    "generated_at": datetime.utcnow().isoformat(),
                    "model": "gemini-pro"
                }
            }
            
        except Exception as e:
            logger.error(f"Content generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def generate_practice_problems(self, topic: str, difficulty: str, count: int = 5) -> Dict[str, Any]:
        """Generate practice problems for a topic"""
        try:
            prompt = f"""
            Generate {count} practice problems for the topic: {topic}
            
            Requirements:
            - Difficulty level: {difficulty}
            - Include problems of varying complexity
            - Provide clear problem statements
            - Include step-by-step solutions
            - Add hints for challenging problems
            - Format for educational use
            
            Output format:
            {{
                "problems": [
                    {{
                        "id": 1,
                        "title": "Problem Title",
                        "statement": "Problem statement",
                        "hints": ["Hint 1", "Hint 2"],
                        "solution": "Step-by-step solution",
                        "difficulty": "Easy/Medium/Hard",
                        "concepts": ["Concept 1", "Concept 2"]
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            problems = json.loads(response.text)
            
            return {
                "success": True,
                "problems": problems["problems"],
                "metadata": {
                    "topic": topic,
                    "difficulty": difficulty,
                    "count": count,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Practice problems generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "problems": []
            }
    
    def generate_simulation_script(self, simulation_type: str, topic: str) -> Dict[str, Any]:
        """Generate interactive simulation script"""
        try:
            prompt = f"""
            Generate an interactive simulation script for: {simulation_type} on topic: {topic}
            
            Requirements:
            - Create engaging, interactive learning experience
            - Include user input points and decision trees
            - Provide real-time feedback mechanisms
            - Include learning objectives and outcomes
            - Suggest visual elements and animations
            - Format for web-based simulation
            
            Output format:
            {{
                "simulation_title": "Simulation Title",
                "learning_objectives": ["Objective 1", "Objective 2"],
                "script": [
                    {{
                        "step": 1,
                        "type": "introduction/explanation/interaction/feedback",
                        "content": "Script content",
                        "user_input": true/false,
                        "options": ["Option 1", "Option 2"],
                        "feedback": "Feedback text"
                    }}
                ],
                "visual_elements": ["Element 1", "Element 2"],
                "interactivity": {{
                    "input_types": ["slider", "button", "dropdown"],
                    "feedback_types": ["immediate", "delayed"]
                }}
            }}
            """
            
            response = self.model.generate_content(prompt)
            simulation = json.loads(response.text)
            
            return {
                "success": True,
                "simulation": simulation,
                "metadata": {
                    "simulation_type": simulation_type,
                    "topic": topic,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Simulation script generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "simulation": None
            }
    
    def generate_exam_questions(self, exam_type: str, subject: str, topic: str, count: int = 10) -> Dict[str, Any]:
        """Generate exam questions with answers and explanations"""
        try:
            prompt = f"""
            Generate {count} exam questions for {exam_type} exam in {subject} on topic: {topic}
            
            Requirements:
            - Match the exam pattern and difficulty level
            - Include multiple question types (MCQ, short answer, long answer)
            - Provide correct answers with detailed explanations
            - Include marking scheme for subjective questions
            - Add time allocation suggestions
            - Format for exam preparation
            
            Output format:
            {{
                "questions": [
                    {{
                        "id": 1,
                        "type": "MCQ/Short Answer/Long Answer/Numerical",
                        "question": "Question text",
                        "options": ["Option A", "Option B"] (for MCQ),
                        "correct_answer": "Correct answer",
                        "explanation": "Detailed explanation",
                        "marks": 2,
                        "time_allocation": "2 minutes",
                        "difficulty": "Easy/Medium/Hard"
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            questions = json.loads(response.text)
            
            return {
                "success": True,
                "questions": questions["questions"],
                "metadata": {
                    "exam_type": exam_type,
                    "subject": subject,
                    "topic": topic,
                    "count": count,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Exam questions generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "questions": []
            }
    
    def generate_career_guidance(self, interests: List[str], skills: List[str], education_level: str) -> Dict[str, Any]:
        """Generate personalized career guidance"""
        try:
            prompt = f"""
            Generate career guidance based on:
            - Interests: {', '.join(interests)}
            - Skills: {', '.join(skills)}
            - Education Level: {education_level}
            
            Requirements:
            - Suggest relevant career paths
            - Provide skill gap analysis
            - Recommend learning resources
            - Include industry trends and opportunities
            - Format for career counseling
            
            Output format:
            {{
                "career_paths": [
                    {{
                        "career": "Career Name",
                        "match_score": 85,
                        "description": "Career description",
                        "required_skills": ["Skill 1", "Skill 2"],
                        "growth_opportunities": "Growth description",
                        "salary_range": "$50k - $100k"
                    }}
                ],
                "skill_gaps": [
                    {{
                        "current_skill": "Skill name",
                        "target_level": "Advanced",
                        "improvement_plan": "Plan description"
                    }}
                ],
                "learning_recommendations": [
                    {{
                        "resource_type": "Course/Book/Certification",
                        "title": "Resource title",
                        "provider": "Provider name",
                        "duration": "3 months",
                        "difficulty": "Intermediate"
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            guidance = json.loads(response.text)
            
            return {
                "success": True,
                "guidance": guidance,
                "metadata": {
                    "interests": interests,
                    "skills": skills,
                    "education_level": education_level,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Career guidance generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "guidance": None
            }
    
    def generate_multilingual_content(self, content: str, target_languages: List[str]) -> Dict[str, Any]:
        """Generate multilingual versions of content"""
        try:
            translations = {}
            
            for language in target_languages:
                prompt = f"""
                Translate the following educational content to {language}:
                
                Content: {content}
                
                Requirements:
                - Maintain educational accuracy
                - Use appropriate terminology
                - Preserve formatting and structure
                - Adapt examples for cultural relevance
                
                Return only the translated content.
                """
                
                response = self.model.generate_content(prompt)
                translations[language] = response.text
            
            return {
                "success": True,
                "translations": translations,
                "metadata": {
                    "source_language": "English",
                    "target_languages": target_languages,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Multilingual content generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "translations": {}
            }
    
    def analyze_image_and_generate_content(self, image_path: str, topic: str) -> Dict[str, Any]:
        """Analyze image and generate educational content"""
        try:
            # This would require image upload functionality
            # For now, return a placeholder structure
            prompt = f"""
            Analyze the educational image related to {topic} and generate:
            - Detailed description of the image
            - Key concepts illustrated
            - Questions that can be asked based on the image
            - Explanations of visual elements
            
            Output format:
            {{
                "image_description": "Description of the image",
                "key_concepts": ["Concept 1", "Concept 2"],
                "visual_explanations": [
                    {{
                        "element": "Visual element",
                        "explanation": "Explanation"
                    }}
                ],
                "discussion_questions": ["Question 1", "Question 2"],
                "learning_activities": ["Activity 1", "Activity 2"]
            }}
            """
            
            # In a real implementation, you would use:
            # image = genai.upload_file(image_path)
            # response = self.vision_model.generate_content([prompt, image])
            
            # For now, return a mock response structure
            return {
                "success": True,
                "content": {
                    "image_description": "Educational image analysis",
                    "key_concepts": [topic],
                    "visual_explanations": [],
                    "discussion_questions": [],
                    "learning_activities": []
                },
                "metadata": {
                    "topic": topic,
                    "image_path": image_path,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Image analysis error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def generate_adaptive_learning_path(self, student_profile: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Generate personalized learning path based on student profile"""
        try:
            prompt = f"""
            Generate an adaptive learning path for a student with profile:
            - Education Level: {student_profile.get('education_level', 'Not specified')}
            - Current Level: {student_profile.get('current_level', 'Beginner')}
            - Learning Style: {student_profile.get('learning_style', 'Visual')}
            - Weak Areas: {', '.join(student_profile.get('weak_areas', []))}
            - Strong Areas: {', '.join(student_profile.get('strong_areas', []))}
            - Goals: {student_profile.get('goals', 'General understanding')}
            
            Topic: {topic}
            
            Requirements:
            - Create step-by-step learning path
            - Include estimated time for each step
            - Suggest appropriate resources
            - Include assessment checkpoints
            - Adapt based on student profile
            
            Output format:
            {{
                "learning_path": [
                    {{
                        "step": 1,
                        "title": "Step title",
                        "content_type": "Video/Text/Interactive/Simulation",
                        "estimated_time": "30 minutes",
                        "resources": ["Resource 1", "Resource 2"],
                        "assessment": "Quiz/Exercise/Project",
                        "success_criteria": "Criteria for completion"
                    }}
                ],
                "total_duration": "Total estimated time",
                "milestones": ["Milestone 1", "Milestone 2"],
                "adaptation_rules": ["Rule 1", "Rule 2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            learning_path = json.loads(response.text)
            
            return {
                "success": True,
                "learning_path": learning_path,
                "metadata": {
                    "student_profile": student_profile,
                    "topic": topic,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Adaptive learning path generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "learning_path": None
            }

# Global AI content generator instance
ai_content_generator = AIContentGenerator()

# Content generation utilities
class ContentGenerationUtils:
    """Utility functions for content generation"""
    
    @staticmethod
    def validate_generated_content(content: Dict[str, Any], content_type: str) -> bool:
        """Validate generated content structure"""
        required_fields = {
            "explanation": ["title", "introduction", "explanation"],
            "problems": ["problems"],
            "simulation": ["simulation_title", "learning_objectives", "script"],
            "questions": ["questions"],
            "guidance": ["career_paths", "skill_gaps"],
            "translations": ["translations"]
        }
        
        if content_type not in required_fields:
            return False
        
        required = required_fields[content_type]
        return all(field in content for field in required)
    
    @staticmethod
    def format_for_frontend(content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Format content for frontend consumption"""
        if not content.get("success"):
            return content
        
        formatted = {
            "success": True,
            "data": content.get("content", content.get("problems", content.get("questions", content.get("guidance", {})))),
            "metadata": content.get("metadata", {}),
            "generated_at": content.get("metadata", {}).get("generated_at")
        }
        
        return formatted
    
    @staticmethod
    def estimate_content_complexity(content: str) -> str:
        """Estimate content complexity level"""
        word_count = len(content.split())
        if word_count < 100:
            return "Beginner"
        elif word_count < 500:
            return "Intermediate"
        else:
            return "Advanced"
    
    @staticmethod
    def generate_content_summary(content: Dict[str, Any]) -> str:
        """Generate summary of generated content"""
        if not content.get("success"):
            return "Content generation failed"
        
        metadata = content.get("metadata", {})
        content_type = metadata.get("type", "Unknown")
        topic = metadata.get("topic", "Unknown topic")
        
        return f"Generated {content_type} content for {topic} at {datetime.fromisoformat(metadata.get('generated_at', '')).strftime('%Y-%m-%d %H:%M:%S')}"

# Content caching for performance
class ContentCache:
    """Simple in-memory content cache"""
    
    def __init__(self):
        self.cache = {}
        self.max_size = 1000
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get content from cache"""
        return self.cache.get(key)
    
    def set(self, key: str, content: Dict[str, Any]):
        """Set content in cache"""
        if len(self.cache) >= self.max_size:
            # Remove oldest item
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = content
    
    def clear(self):
        """Clear all cached content"""
        self.cache.clear()

# Global content cache instance
content_cache = ContentCache()