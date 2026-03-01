# EduVerse AI - Complete API Documentation

## 🌍 Overview

EduVerse AI is a comprehensive 10-engine autonomous agentic AI educational platform that provides intelligent learning, simulation-based education, exam prediction, and career guidance. This documentation covers all API endpoints, data models, and integration guidelines.

## 🏗️ System Architecture

### 10 Integrated Engines

1. **Student Intelligence & Assessment Engine** - Diagnoses strengths and weaknesses
2. **Foundation Rebuilding Engine** - Rebuilds weak conceptual foundations
3. **Hybrid Simulation Intelligence Engine** - Provides experiential learning
4. **Question Intelligence & Prediction Engine** - Predicts exam questions
5. **Competitive & Government Exam Engine** - Mock tests and rank estimation
6. **College Mastery & Department Excellence Engine** - Deep subject mastery
7. **Career Intelligence & Global Demand Engine** - Career guidance and skill mapping
8. **Multilingual & Accessibility Engine** - 6-language support with accessibility
9. **Industry Integration & Credibility Layer** - Mentorship and industry connections
10. **Explainability & Transparency Engine** - AI decision explanations

## 🔐 Authentication

### JWT-Based Authentication

All API endpoints require authentication using JWT tokens.

#### Login Endpoint
```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "role": "student",
            "is_active": true,
            "created_at": "2024-01-01T10:00:00Z"
        }
    }
}
```

#### Authentication Header
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Role-Based Access Control

- **Student**: Access to learning content, assessments, simulations
- **Teacher**: Access to student management, analytics
- **Admin**: Full system access, user management
- **Mentor**: Industry expert access, session management

## 📊 Core API Endpoints

### Authentication & User Management

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "username": "student123",
    "email": "student@example.com",
    "password": "securepassword123",
    "role": "student"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Student Intelligence & Assessment Engine

#### Submit Assessment
```http
POST /api/v1/students/{student_id}/assessments
Authorization: Bearer <token>
Content-Type: application/json

{
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
```

**Response:**
```json
{
    "success": true,
    "message": "Assessment submitted successfully",
    "data": {
        "assessment": {
            "id": 123,
            "student_id": 1,
            "subject": "Mathematics",
            "topic": "Algebra",
            "score": 75.0,
            "max_score": 100.0,
            "percentage": 75.0,
            "time_taken": 450,
            "difficulty": "intermediate",
            "created_at": "2024-01-01T10:00:00Z"
        },
        "analysis": {
            "percentage": 75.0,
            "status": "Good",
            "weakness_detected": false,
            "time_efficiency": "Efficient"
        },
        "skill_profile": {
            "weak_topics": ["Calculus", "Trigonometry"],
            "strong_topics": ["Algebra", "Geometry"],
            "priority_index": [
                {"topic": "Calculus", "priority": "High", "score": 45.0},
                {"topic": "Trigonometry", "priority": "Medium", "score": 60.0}
            ]
        },
        "recommendation": "Great performance! Continue to next topic."
    }
}
```

#### Get Weakness Analysis
```http
GET /api/v1/students/{student_id}/weakness-analysis
Authorization: Bearer <token>
```

### Foundation Rebuilding Engine

#### Rebuild Foundation
```http
POST /api/v1/students/{student_id}/foundation/rebuild
Authorization: Bearer <token>
Content-Type: application/json

{
    "weak_topic": "Calculus",
    "current_level": "Weak"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Foundation rebuilding plan generated",
    "data": {
        "student_id": 1,
        "topic": "Calculus",
        "learning_path": {
            "topic": "Calculus",
            "prerequisites": ["Algebra", "Trigonometry"],
            "learning_path": [
                {
                    "step": 1,
                    "concept": "Limits - Basics",
                    "mode": "Beginner",
                    "resources": [
                        {"type": "video", "title": "Introduction to Limits"},
                        {"type": "text", "title": "Limits - Detailed Explanation"},
                        {"type": "practice", "title": "Limits - Practice Problems"}
                    ]
                }
            ],
            "estimated_time": 90
        },
        "visual_aids": {
            "diagrams": ["calculus_diagram_1.png", "calculus_diagram_2.png"],
            "animations": ["calculus_animation.mp4"],
            "interactive": "calculus_interactive_demo"
        }
    }
}
```

### Simulation Intelligence Engine

#### Start Simulation
```http
POST /api/v1/simulations/start
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": 1,
    "simulation_type": "virtual_lab",
    "topic": "Chemistry",
    "difficulty": "beginner"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Simulation started successfully",
    "data": {
        "simulation_id": 456,
        "parameters": {
            "difficulty": {
                "level": "beginner",
                "guidance": "high",
                "hints": "enabled"
            },
            "language": "English",
            "duration": 30
        },
        "guidance_level": "high",
        "language": "English"
    }
}
```

#### Complete Simulation
```http
POST /api/v1/simulations/{simulation_id}/complete
Authorization: Bearer <token>
Content-Type: application/json

{
    "performance": 85.0,
    "actions_taken": 15,
    "decisions_made": 10
}
```

### Question Intelligence & Prediction Engine

#### Predict Exam Questions
```http
POST /api/v1/exam/predict
Authorization: Bearer <token>
Content-Type: application/json

{
    "exam_type": "school_board",
    "subject": "Mathematics",
    "student_weaknesses": ["Calculus", "Trigonometry"]
}
```

**Response:**
```json
{
    "success": true,
    "message": "Exam predictions generated successfully",
    "data": {
        "high_probability_topics": [
            {
                "topic": "Calculus",
                "probability": 85.0,
                "weightage": 25.0,
                "question_types": ["MCQ", "Long Answer"]
            }
        ],
        "priority_questions": ["Calculus", "Trigonometry", "Algebra"],
        "weightage_distribution": {"analyzed": true},
        "study_strategy": "Focus on Calculus fundamentals and practice derivations"
    }
}
```

### Competitive Exam Engine

#### Generate Mock Test
```http
POST /api/v1/mock-tests/generate
Authorization: Bearer <token>
Content-Type: application/json

{
    "exam_type": "competitive",
    "difficulty": "advanced",
    "student_id": 1
}
```

#### Evaluate Mock Test
```http
POST /api/v1/mock-tests/evaluate
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": 1,
    "exam_type": "competitive",
    "answers": [
        {"question_id": 1, "answer": "A"},
        {"question_id": 2, "answer": "B"}
    ]
}
```

### Career Intelligence Engine

#### Analyze Career
```http
POST /api/v1/career/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": 1,
    "interests": ["Programming", "Mathematics", "Problem Solving"],
    "strengths": ["Logical Thinking", "Analytical Skills", "Coding"]
}
```

**Response:**
```json
{
    "success": true,
    "message": "Career analysis completed successfully",
    "data": {
        "recommended_careers": [
            {
                "career": "Software Engineer",
                "match_score": 92.0,
                "description": "Develop and maintain software applications",
                "salary_range": "$70k - $150k"
            }
        ],
        "skill_gaps": {
            "Data Structures": {"current": "Beginner", "target": "Advanced"},
            "Algorithms": {"current": "Intermediate", "target": "Advanced"}
        },
        "certifications": ["AWS Certified Developer", "Google Cloud Professional"],
        "learning_path": ["Data Structures", "Algorithms", "System Design"]
    }
}
```

### Multilingual Engine

#### Translate Content
```http
POST /api/v1/translate
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "Welcome to EduVerse AI learning platform",
    "target_language": "Tamil"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Content translated successfully",
    "data": {
        "translated_text": "எட்யூவேர்ஸ் ஏஐ கற்றல் தளத்திற்கு வரவேற்கிறோம்",
        "audio_url": "https://api.eduverse.ai/audio/tamil_welcome.mp3"
    }
}
```

#### Get Supported Languages
```http
GET /api/v1/languages
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "message": "Languages retrieved successfully",
    "data": {
        "languages": ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"],
        "total": 6
    }
}
```

### Industry Integration Engine

#### Onboard Mentor
```http
POST /api/v1/mentors/onboard
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Dr. John Smith",
    "email": "john.smith@techcorp.com",
    "industry": "Technology",
    "expertise": ["Software Architecture", "Cloud Computing", "AI/ML"],
    "experience_years": 15,
    "company": "TechCorp Inc.",
    "linkedin_profile": "https://linkedin.com/in/johnsmith"
}
```

#### Find Mentor
```http
GET /api/v1/mentors/find/Technology?expertise=Software%20Architecture
Authorization: Bearer <token>
```

### Explainability Engine

#### Explain Topic Importance
```http
GET /api/v1/explain/topic-importance/Calculus?exam_type=school_board&probability=85.0
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "message": "Topic importance explained successfully",
    "data": {
        "topic": "Calculus",
        "exam_type": "school_board",
        "importance_score": 85.0,
        "reasons": [
            "Fundamental for advanced mathematics",
            "High weightage in board exams",
            "Essential for engineering entrance exams"
        ],
        "suggested_focus": "Practice derivations and applications"
    }
}
```

#### Get Transparency Report
```http
GET /api/v1/transparency-report/{student_id}
Authorization: Bearer <token>
```

### College Mastery Engine

#### Get Learning Path
```http
GET /api/v1/college/learning-path/Computer%20Science/Data%20Structures?current_level=Beginner
Authorization: Bearer <token>
```

#### Get Project Suggestions
```http
GET /api/v1/college/projects/Computer%20Science?skill_level=Intermediate&interests=Web%20Development,AI
Authorization: Bearer <token>
```

### Autonomous Agent Orchestrator

#### Autonomous Decision
```http
POST /api/v1/autonomous/analyze-and-decide
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": 1,
    "assessment_data": {
        "topic": "Calculus",
        "score": 65.0,
        "max_score": 100.0,
        "time_taken": 600
    }
}
```

**Response:**
```json
{
    "success": true,
    "message": "Autonomous analysis completed",
    "data": {
        "autonomous_decision": {
            "recommended_action": "Start foundation rebuilding for Calculus",
            "priority": "High",
            "suggested_resources": ["Video tutorials", "Interactive simulations"],
            "estimated_time": "2-3 weeks"
        },
        "agent_type": "EduVerse Autonomous Intelligence",
        "decision_confidence": "High"
    }
}
```

#### Get Student Dashboard
```http
GET /api/v1/dashboard/{student_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "message": "Student dashboard generated successfully",
    "data": {
        "student_info": {
            "id": 1,
            "name": "John Doe",
            "education_level": "college",
            "language_preference": "English",
            "overall_performance": 78.5
        },
        "current_assessment": {
            "subject": "Mathematics",
            "topic": "Calculus",
            "percentage": 75.0,
            "status": "Good"
        },
        "weakness_analysis": {
            "weak_topics": ["Calculus", "Trigonometry"],
            "strength_topics": ["Algebra", "Geometry"],
            "priority_index": [...]
        },
        "learning_path": {
            "subject": "Mathematics",
            "current_level": "intermediate",
            "progress_percentage": 65.0,
            "completed_topics": ["Algebra", "Geometry"]
        },
        "simulation_progress": [...],
        "career_profile": {...},
        "recent_content_interactions": [...],
        "progress_analytics": {...}
    }
}
```

## 📋 Data Models

### User Model
```json
{
    "id": 1,
    "username": "student123",
    "email": "student@example.com",
    "role": "student",
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z",
    "last_login": "2024-01-02T15:30:00Z"
}
```

### Student Model
```json
{
    "id": 1,
    "user_id": 1,
    "name": "John Doe",
    "age": 18,
    "education_level": "college",
    "language_preference": "English",
    "learning_style": "visual",
    "accessibility_needs": {},
    "overall_performance": 78.5,
    "last_assessment_date": "2024-01-02T10:00:00Z",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-02T15:30:00Z"
}
```

### Assessment Model
```json
{
    "id": 123,
    "student_id": 1,
    "subject": "Mathematics",
    "topic": "Algebra",
    "score": 75.0,
    "max_score": 100.0,
    "percentage": 75.0,
    "time_taken": 450,
    "difficulty": "intermediate",
    "complexity_level": 7,
    "question_count": 25,
    "assessment_type": "diagnostic",
    "created_at": "2024-01-01T10:00:00Z"
}
```

### Simulation Progress Model
```json
{
    "id": 456,
    "student_id": 1,
    "simulation_id": 1,
    "mastery_score": 85.0,
    "attempts": 2,
    "best_score": 90.0,
    "time_spent": 1800,
    "completed": true,
    "completed_at": "2024-01-01T11:00:00Z",
    "created_at": "2024-01-01T10:00:00Z"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eduverse

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Services
GOOGLE_API_KEY=your-google-api-key

# Application
ENVIRONMENT=production
DEBUG=false
```

### CORS Configuration
```python
# FastAPI CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Deployment

### Docker Setup
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/eduverse
      - SECRET_KEY=your-secret-key
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: eduverse
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eduverse-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eduverse-api
  template:
    metadata:
      labels:
        app: eduverse-api
    spec:
      containers:
      - name: eduverse-api
        image: eduverse/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: eduverse-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: eduverse-secrets
              key: secret-key
---
apiVersion: v1
kind: Service
metadata:
  name: eduverse-api-service
spec:
  selector:
    app: eduverse-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 📈 Monitoring & Analytics

### System Health
```http
GET /api/v1/system/health
Authorization: Bearer <token>
```

### System Metrics
```http
GET /api/v1/system/metrics
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "message": "System metrics retrieved successfully",
    "data": {
        "users": {
            "total": 1000,
            "students": 950,
            "mentors": 50
        },
        "assessments": {
            "total": 5000,
            "average_score": 78.5
        },
        "simulations": {
            "total": 2000,
            "completed": 1800,
            "completion_rate": 90.0
        },
        "timestamp": "2024-01-01T10:00:00Z"
    }
}
```

## 🔒 Security

### Rate Limiting
- Registration: 5 attempts per hour per email
- Login: 10 attempts per 5 minutes per user
- API calls: Configurable per endpoint

### Input Validation
- Password strength requirements
- SQL injection prevention
- XSS protection
- Input sanitization

### Data Encryption
- Passwords: bcrypt hashing
- JWT tokens: HS256 algorithm
- Database: SSL/TLS encryption

## 🧪 Testing

### Unit Tests
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
```

### Integration Tests
```python
def test_assessment_submission():
    # Login first
    login_response = client.post("/api/v1/auth/login", json={
        "email": "student@example.com",
        "password": "password123"
    })
    token = login_response.json()["data"]["access_token"]
    
    # Submit assessment
    response = client.post("/api/v1/students/1/assessments", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subject": "Mathematics",
            "topic": "Algebra",
            "score": 85.0,
            "max_score": 100.0,
            "time_taken": 450,
            "difficulty": "intermediate"
        })
    
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## 📞 Support

### Error Codes
- `400`: Bad Request - Invalid input data
- `401`: Unauthorized - Invalid or missing authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Server error

### Contact
- **Email**: support@eduverse.ai
- **Documentation**: https://docs.eduverse.ai
- **GitHub**: https://github.com/eduverse/eduverse-backend

## 📄 License

This API is part of the EduVerse AI educational platform. For licensing information, please refer to the project repository.

---

**Last Updated**: January 2024  
**Version**: 2.0.0  
**API Base URL**: `https://api.eduverse.ai/api/v1`