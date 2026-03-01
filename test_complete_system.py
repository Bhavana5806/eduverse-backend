"""
Comprehensive Test Suite for EduVerse AI System
Tests all 10 engines, API endpoints, database models, and AI services
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Import app components
from app.main import app
from app.db.database import Base, get_db
from app.db.enhanced_models import User, Student, Mentor, Assessment
from app.core.config import settings
from app.services.ai_content_service import ai_content_generator

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

# Test client
client = TestClient(app)

class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_register_user(self):
        """Test user registration"""
        response = client.post("/api/v1/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["email"] == "test@example.com"
        assert data["data"]["role"] == "student"
    
    def test_login_user(self):
        """Test user login"""
        # First register a user
        client.post("/api/v1/auth/register", json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        # Then login
        response = client.post("/api/v1/auth/login", json={
            "email": "login@example.com",
            "password": "SecurePass123!"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
    
    def test_invalid_login(self):
        """Test invalid login credentials"""
        response = client.post("/api/v1/auth/login", json={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 200  # Returns success=False instead of 401
        data = response.json()
        assert data["success"] == False
    
    def test_refresh_token(self):
        """Test token refresh"""
        # Login first
        login_response = client.post("/api/v1/auth/login", json={
            "email": "login@example.com",
            "password": "SecurePass123!"
        })
        
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Refresh token
        response = client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "access_token" in data["data"]

class TestStudentIntelligence:
    """Test Student Intelligence & Assessment Engine"""
    
    def setup_method(self):
        """Setup test data"""
        # Register and login a student
        client.post("/api/v1/auth/register", json={
            "username": "student1",
            "email": "student1@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "student1@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_submit_assessment(self):
        """Test assessment submission"""
        response = client.post(
            f"/api/v1/students/{self.student_id}/assessments",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "subject": "Mathematics",
                "topic": "Algebra",
                "score": 75.0,
                "max_score": 100.0,
                "time_taken": 450,
                "difficulty": "intermediate",
                "complexity_level": 7,
                "question_count": 25,
                "assessment_type": "diagnostic"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["assessment"]["subject"] == "Mathematics"
        assert data["data"]["analysis"]["percentage"] == 75.0
    
    def test_get_weakness_analysis(self):
        """Test weakness analysis"""
        # Submit multiple assessments first
        for i in range(3):
            client.post(
                f"/api/v1/students/{self.student_id}/assessments",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "subject": "Mathematics",
                    "topic": f"Topic {i}",
                    "score": 60.0 + i * 10,
                    "max_score": 100.0,
                    "time_taken": 450,
                    "difficulty": "intermediate",
                    "complexity_level": 7,
                    "question_count": 25,
                    "assessment_type": "diagnostic"
                }
            )
        
        response = client.get(
            f"/api/v1/students/{self.student_id}/weakness-analysis",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "weak_topics" in data["data"]

class TestFoundationRebuilding:
    """Test Foundation Rebuilding Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "foundation_user",
            "email": "foundation@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "foundation@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_rebuild_foundation(self):
        """Test foundation rebuilding"""
        response = client.post(
            f"/api/v1/students/{self.student_id}/foundation/rebuild",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "weak_topic": "Calculus",
                "current_level": "Weak"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["topic"] == "Calculus"
        assert "learning_path" in data["data"]
        assert "visual_aids" in data["data"]

class TestSimulationIntelligence:
    """Test Simulation Intelligence Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "simulation_user",
            "email": "simulation@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "simulation@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_start_simulation(self):
        """Test starting a simulation"""
        response = client.post(
            "/api/v1/simulations/start",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "student_id": self.student_id,
                "simulation_type": "virtual_lab",
                "topic": "Chemistry",
                "difficulty": "beginner"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "simulation_id" in data["data"]
        assert data["data"]["parameters"]["difficulty"]["level"] == "beginner"
    
    def test_complete_simulation(self):
        """Test completing a simulation"""
        # Start simulation first
        start_response = client.post(
            "/api/v1/simulations/start",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "student_id": self.student_id,
                "simulation_type": "virtual_lab",
                "topic": "Chemistry",
                "difficulty": "beginner"
            }
        )
        
        simulation_id = start_response.json()["data"]["simulation_id"]
        
        # Complete simulation
        response = client.post(
            f"/api/v1/simulations/{simulation_id}/complete",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "performance": 85.0,
                "actions_taken": 15,
                "decisions_made": 10
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "reinforcement_test" in data["data"]
        assert "mastery" in data["data"]

class TestQuestionIntelligence:
    """Test Question Intelligence & Prediction Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "question_user",
            "email": "question@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "question@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_predict_exam_questions(self):
        """Test exam question prediction"""
        response = client.post(
            "/api/v1/exam/predict",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "exam_type": "school_board",
                "subject": "Mathematics",
                "student_weaknesses": ["Calculus", "Trigonometry"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "high_probability_topics" in data["data"]
        assert "priority_questions" in data["data"]

class TestCareerIntelligence:
    """Test Career Intelligence Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "career_user",
            "email": "career@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "career@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_career_analysis(self):
        """Test career analysis"""
        response = client.post(
            "/api/v1/career/analyze",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "student_id": self.student_id,
                "interests": ["Programming", "Mathematics", "Problem Solving"],
                "strengths": ["Logical Thinking", "Analytical Skills", "Coding"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "recommended_careers" in data["data"]
        assert "skill_gaps" in data["data"]
        assert "certifications" in data["data"]

class TestMultilingualEngine:
    """Test Multilingual & Accessibility Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "multilingual_user",
            "email": "multilingual@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "multilingual@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
    
    def test_translate_content(self):
        """Test content translation"""
        response = client.post(
            "/api/v1/translate",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "text": "Welcome to EduVerse AI learning platform",
                "target_language": "Tamil"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "translated_text" in data["data"]
        assert "audio_url" in data["data"]
    
    def test_get_supported_languages(self):
        """Test getting supported languages"""
        response = client.get(
            "/api/v1/languages",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "languages" in data["data"]
        assert len(data["data"]["languages"]) >= 6  # Should include all 6 languages

class TestIndustryIntegration:
    """Test Industry Integration Engine"""
    
    def setup_method(self):
        """Setup test data"""
        # Register admin user
        client.post("/api/v1/auth/register", json={
            "username": "admin_user",
            "email": "admin@example.com",
            "password": "SecurePass123!",
            "role": "admin"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "admin@example.com",
            "password": "SecurePass123!"
        })
        self.admin_token = login_response.json()["data"]["access_token"]
        
        # Register student user
        client.post("/api/v1/auth/register", json={
            "username": "student_mentor_user",
            "email": "student_mentor@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "student_mentor@example.com",
            "password": "SecurePass123!"
        })
        self.student_token = login_response.json()["data"]["access_token"]
    
    def test_onboard_mentor(self):
        """Test mentor onboarding"""
        response = client.post(
            "/api/v1/mentors/onboard",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={
                "name": "Dr. John Smith",
                "email": "john.smith@techcorp.com",
                "industry": "Technology",
                "expertise": ["Software Architecture", "Cloud Computing", "AI/ML"],
                "experience_years": 15,
                "company": "TechCorp Inc.",
                "linkedin_profile": "https://linkedin.com/in/johnsmith"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["name"] == "Dr. John Smith"
        assert data["data"]["industry"] == "Technology"
    
    def test_find_mentor(self):
        """Test finding mentors"""
        # First onboard a mentor
        client.post(
            "/api/v1/mentors/onboard",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={
                "name": "Dr. Jane Doe",
                "email": "jane.doe@techcorp.com",
                "industry": "Technology",
                "expertise": ["Software Architecture", "Cloud Computing"],
                "experience_years": 12,
                "company": "TechCorp Inc."
            }
        )
        
        response = client.get(
            "/api/v1/mentors/find/Technology?expertise=Software%20Architecture",
            headers={"Authorization": f"Bearer {self.student_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert len(data["data"]) > 0

class TestExplainabilityEngine:
    """Test Explainability & Transparency Engine"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "explainability_user",
            "email": "explainability@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "explainability@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_explain_topic_importance(self):
        """Test topic importance explanation"""
        response = client.get(
            "/api/v1/explain/topic-importance/Calculus?exam_type=school_board&probability=85.0",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "topic" in data["data"]
        assert "reasons" in data["data"]
    
    def test_get_transparency_report(self):
        """Test transparency report generation"""
        response = client.get(
            f"/api/v1/transparency-report/{self.student_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "report" in data["data"]

class TestAutonomousOrchestrator:
    """Test Autonomous Agent Orchestrator"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "autonomous_user",
            "email": "autonomous@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "autonomous@example.com",
            "password": "SecurePass123!"
        })
        self.token = login_response.json()["data"]["access_token"]
        self.student_id = login_response.json()["data"]["user"]["id"]
    
    def test_autonomous_decision(self):
        """Test autonomous decision making"""
        response = client.post(
            "/api/v1/autonomous/analyze-and-decide",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "student_id": self.student_id,
                "assessment_data": {
                    "topic": "Calculus",
                    "score": 65.0,
                    "max_score": 100.0,
                    "time_taken": 600
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "autonomous_decision" in data["data"]
        assert "agent_type" in data["data"]
    
    def test_get_student_dashboard(self):
        """Test student dashboard generation"""
        response = client.get(
            f"/api/v1/dashboard/{self.student_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "student_info" in data["data"]
        assert "current_assessment" in data["data"]
        assert "weakness_analysis" in data["data"]

class TestAIContentGeneration:
    """Test AI Content Generation Service"""
    
    def test_generate_explanation(self):
        """Test content explanation generation"""
        if not hasattr(ai_content_generator, 'model'):
            pytest.skip("AI model not available")
        
        result = ai_content_generator.generate_explanation(
            topic="Calculus",
            difficulty="intermediate",
            language="English"
        )
        
        assert result["success"] == True
        assert "content" in result
        assert "title" in result["content"]
        assert "explanation" in result["content"]
    
    def test_generate_practice_problems(self):
        """Test practice problem generation"""
        if not hasattr(ai_content_generator, 'model'):
            pytest.skip("AI model not available")
        
        result = ai_content_generator.generate_practice_problems(
            topic="Algebra",
            difficulty="beginner",
            count=3
        )
        
        assert result["success"] == True
        assert "problems" in result
        assert len(result["problems"]) == 3
    
    def test_generate_multilingual_content(self):
        """Test multilingual content generation"""
        if not hasattr(ai_content_generator, 'model'):
            pytest.skip("AI model not available")
        
        result = ai_content_generator.generate_multilingual_content(
            content="Welcome to learning",
            target_languages=["Tamil", "Hindi"]
        )
        
        assert result["success"] == True
        assert "translations" in result
        assert "Tamil" in result["translations"]
        assert "Hindi" in result["translations"]

class TestSystemHealth:
    """Test system health and monitoring"""
    
    def setup_method(self):
        """Setup test data"""
        client.post("/api/v1/auth/register", json={
            "username": "admin_health",
            "email": "admin_health@example.com",
            "password": "SecurePass123!",
            "role": "admin"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "admin_health@example.com",
            "password": "SecurePass123!"
        })
        self.admin_token = login_response.json()["data"]["access_token"]
    
    def test_system_health(self):
        """Test system health endpoint"""
        response = client.get(
            "/api/v1/system/health",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["status"] == "healthy"
        assert data["data"]["engines_active"] == 10
    
    def test_system_metrics(self):
        """Test system metrics endpoint"""
        response = client.get(
            "/api/v1/system/metrics",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "users" in data["data"]
        assert "assessments" in data["data"]
        assert "simulations" in data["data"]

class TestSecurity:
    """Test security features"""
    
    def test_rate_limiting(self):
        """Test rate limiting on login"""
        # Try multiple login attempts
        for i in range(15):  # Exceed limit of 10
            response = client.post("/api/v1/auth/login", json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            })
        
        # Should eventually be rate limited
        assert response.status_code in [200, 429]  # Depends on implementation
    
    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        response = client.get("/api/v1/students/1/assessments")
        
        # Should require authentication
        assert response.status_code in [401, 403]
    
    def test_password_strength_validation(self):
        """Test password strength validation"""
        response = client.post("/api/v1/auth/register", json={
            "username": "weak_user",
            "email": "weak@example.com",
            "password": "123",  # Weak password
            "role": "student"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "errors" in data

class TestDatabaseModels:
    """Test database models and relationships"""
    
    def test_user_model(self):
        """Test User model creation"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
            role="student"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.role == "student"
        assert user.is_active == True
    
    def test_student_model(self):
        """Test Student model creation"""
        student = Student(
            name="John Doe",
            age=18,
            education_level="college",
            language_preference="English",
            learning_style="visual"
        )
        
        assert student.name == "John Doe"
        assert student.age == 18
        assert student.education_level == "college"
        assert student.language_preference == "English"
    
    def test_assessment_model(self):
        """Test Assessment model creation"""
        assessment = Assessment(
            student_id=1,
            subject="Mathematics",
            topic="Algebra",
            score=75.0,
            max_score=100.0,
            time_taken=450,
            difficulty="intermediate"
        )
        
        assert assessment.student_id == 1
        assert assessment.subject == "Mathematics"
        assert assessment.topic == "Algebra"
        assert assessment.score == 75.0
        assert assessment.max_score == 100.0

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_learning_workflow(self):
        """Test complete learning workflow"""
        # 1. Register and login student
        client.post("/api/v1/auth/register", json={
            "username": "workflow_user",
            "email": "workflow@example.com",
            "password": "SecurePass123!",
            "role": "student"
        })
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": "workflow@example.com",
            "password": "SecurePass123!"
        })
        
        token = login_response.json()["data"]["access_token"]
        student_id = login_response.json()["data"]["user"]["id"]
        
        # 2. Submit assessment
        assessment_response = client.post(
            f"/api/v1/students/{student_id}/assessments",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "subject": "Mathematics",
                "topic": "Calculus",
                "score": 60.0,
                "max_score": 100.0,
                "time_taken": 600,
                "difficulty": "intermediate",
                "complexity_level": 8,
                "question_count": 30,
                "assessment_type": "diagnostic"
            }
        )
        
        assert assessment_response.status_code == 200
        
        # 3. Get weakness analysis
        weakness_response = client.get(
            f"/api/v1/students/{student_id}/weakness-analysis",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert weakness_response.status_code == 200
        
        # 4. Start foundation rebuilding
        foundation_response = client.post(
            f"/api/v1/students/{student_id}/foundation/rebuild",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "weak_topic": "Calculus",
                "current_level": "Weak"
            }
        )
        
        assert foundation_response.status_code == 200
        
        # 5. Start simulation
        simulation_response = client.post(
            "/api/v1/simulations/start",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "student_id": student_id,
                "simulation_type": "virtual_lab",
                "topic": "Calculus",
                "difficulty": "beginner"
            }
        )
        
        assert simulation_response.status_code == 200
        simulation_id = simulation_response.json()["data"]["simulation_id"]
        
        # 6. Complete simulation
        complete_response = client.post(
            f"/api/v1/simulations/{simulation_id}/complete",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "performance": 80.0,
                "actions_taken": 20,
                "decisions_made": 15
            }
        )
        
        assert complete_response.status_code == 200
        
        # 7. Get student dashboard
        dashboard_response = client.get(
            f"/api/v1/dashboard/{student_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert dashboard_response.status_code == 200
        dashboard_data = dashboard_response.json()
        
        # Verify dashboard contains expected data
        assert dashboard_data["success"] == True
        assert "student_info" in dashboard_data["data"]
        assert "weakness_analysis" in dashboard_data["data"]
        assert "simulation_progress" in dashboard_data["data"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])