"""
Anti-Distraction Service for EduVerse AI
Prevents students from switching tabs or using AI tools during learning sessions
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import asyncio
import hashlib
import secrets
from enum import Enum

from app.core.config import settings
from app.db.enhanced_models import Student, LearningSession, DistractionEvent
from app.db.database import get_db
from sqlalchemy.orm import Session

# Configure logging
logger = logging.getLogger(__name__)

class DistractionType(Enum):
    """Types of distractions detected"""
    TAB_SWITCH = "tab_switch"
    WINDOW_FOCUS_LOSS = "window_focus_loss"
    AI_TOOL_USAGE = "ai_tool_usage"
    MULTITASKING = "multitasking"
    INACTIVITY = "inactivity"

class SessionState(Enum):
    """States of learning session"""
    ACTIVE = "active"
    PAUSED = "paused"
    LOCKED = "locked"
    COMPLETED = "completed"
    DISTRACTED = "distracted"

@dataclass
class DistractionAlert:
    """Alert for distraction detection"""
    student_id: int
    session_id: str
    distraction_type: DistractionType
    timestamp: datetime
    severity: str  # low, medium, high
    message: str
    action_taken: str

@dataclass
class LearningSessionState:
    """State of a learning session"""
    session_id: str
    student_id: int
    start_time: datetime
    end_time: Optional[datetime]
    state: SessionState
    focus_score: float
    distractions_count: int
    last_activity: datetime
    locked_until: Optional[datetime]
    session_key: str

class AntiDistractionManager:
    """Main anti-distraction service manager"""
    
    def __init__(self):
        """Initialize the anti-distraction manager"""
        self.active_sessions: Dict[str, LearningSessionState] = {}
        self.distraction_thresholds = {
            "max_distractions_per_hour": 3,
            "max_inactivity_minutes": 5,
            "lock_duration_minutes": 10,
            "focus_score_threshold": 0.7
        }
        
        # Track student activities
        self.student_activities: Dict[int, Dict[str, Any]] = {}
        
        logger.info("Anti-Distraction Manager initialized successfully")
    
    def create_learning_session(self, student_id: int, session_type: str = "video") -> Dict[str, Any]:
        """Create a new learning session with anti-distraction features"""
        try:
            session_id = self._generate_session_id()
            session_key = self._generate_session_key()
            
            session_state = LearningSessionState(
                session_id=session_id,
                student_id=student_id,
                start_time=datetime.utcnow(),
                end_time=None,
                state=SessionState.ACTIVE,
                focus_score=1.0,
                distractions_count=0,
                last_activity=datetime.utcnow(),
                locked_until=None,
                session_key=session_key
            )
            
            # Store session
            self.active_sessions[session_id] = session_state
            
            # Initialize student activity tracking
            if student_id not in self.student_activities:
                self.student_activities[student_id] = {
                    "session_start": datetime.utcnow(),
                    "distractions": [],
                    "focus_history": [],
                    "last_checkin": datetime.utcnow()
                }
            
            # Create database session record
            session_data = {
                "session_id": session_id,
                "student_id": student_id,
                "session_type": session_type,
                "start_time": session_state.start_time,
                "session_key": session_key,
                "is_active": True
            }
            
            return {
                "success": True,
                "session_data": session_data,
                "client_config": {
                    "session_id": session_id,
                    "session_key": session_key,
                    "anti_distraction_enabled": True,
                    "distraction_thresholds": self.distraction_thresholds,
                    "session_duration_limit": 3600,  # 1 hour
                    "checkin_interval": 30  # Check in every 30 seconds
                }
            }
            
        except Exception as e:
            logger.error(f"Session creation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def validate_session_activity(self, session_id: str, session_key: str, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and process student activity during learning session"""
        try:
            # Validate session exists and is active
            if session_id not in self.active_sessions:
                return {"success": False, "error": "Session not found"}
            
            session_state = self.active_sessions[session_id]
            
            # Validate session key
            if session_state.session_key != session_key:
                return {"success": False, "error": "Invalid session key"}
            
            # Check if session is locked
            if session_state.state == SessionState.LOCKED:
                if datetime.utcnow() < session_state.locked_until:
                    return {
                        "success": False, 
                        "error": "Session locked due to distractions",
                        "locked_until": session_state.locked_until.isoformat()
                    }
                else:
                    # Unlock session
                    session_state.state = SessionState.ACTIVE
                    session_state.locked_until = None
            
            # Process activity data
            distractions = self._analyze_activity(session_state, activity_data)
            
            # Update session state
            session_state.last_activity = datetime.utcnow()
            session_state.distractions_count += len(distractions)
            
            # Update focus score
            session_state.focus_score = self._calculate_focus_score(session_state)
            
            # Handle distractions
            alerts = []
            for distraction in distractions:
                alert = self._handle_distraction(session_state, distraction)
                alerts.append(alert)
                
                # Log distraction event
                self._log_distraction_event(session_state, distraction)
            
            # Check if session should be locked
            if session_state.distractions_count >= self.distraction_thresholds["max_distractions_per_hour"]:
                self._lock_session(session_state)
                alerts.append(DistractionAlert(
                    student_id=session_state.student_id,
                    session_id=session_id,
                    distraction_type=DistractionType.MULTITASKING,
                    timestamp=datetime.utcnow(),
                    severity="high",
                    message="Session locked due to excessive distractions",
                    action_taken="Session locked for 10 minutes"
                ))
            
            return {
                "success": True,
                "session_state": {
                    "session_id": session_id,
                    "state": session_state.state.value,
                    "focus_score": session_state.focus_score,
                    "distractions_count": session_state.distractions_count,
                    "last_activity": session_state.last_activity.isoformat()
                },
                "alerts": [asdict(alert) for alert in alerts],
                "recommendations": self._get_focus_recommendations(session_state)
            }
            
        except Exception as e:
            logger.error(f"Session validation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _analyze_activity(self, session_state: LearningSessionState, activity_data: Dict[str, Any]) -> List[DistractionAlert]:
        """Analyze student activity for distractions"""
        distractions = []
        
        # Check for tab switching
        if activity_data.get("tab_switch_detected", False):
            distractions.append(DistractionAlert(
                student_id=session_state.student_id,
                session_id=session_state.session_id,
                distraction_type=DistractionType.TAB_SWITCH,
                timestamp=datetime.utcnow(),
                severity="medium",
                message="Tab switch detected",
                action_taken="Warning issued"
            ))
        
        # Check for window focus loss
        if activity_data.get("window_focus_lost", False):
            distractions.append(DistractionAlert(
                student_id=session_state.student_id,
                session_id=session_state.session_id,
                distraction_type=DistractionType.WINDOW_FOCUS_LOSS,
                timestamp=datetime.utcnow(),
                severity="medium",
                message="Window focus lost",
                action_taken="Warning issued"
            ))
        
        # Check for AI tool usage
        if activity_data.get("ai_tool_detected", False):
            distractions.append(DistractionAlert(
                student_id=session_state.student_id,
                session_id=session_state.session_id,
                distraction_type=DistractionType.AI_TOOL_USAGE,
                timestamp=datetime.utcnow(),
                severity="high",
                message="AI tool usage detected",
                action_taken="Session will be locked after 3 violations"
            ))
        
        # Check for inactivity
        last_activity = session_state.last_activity
        if datetime.utcnow() - last_activity > timedelta(minutes=self.distraction_thresholds["max_inactivity_minutes"]):
            distractions.append(DistractionAlert(
                student_id=session_state.student_id,
                session_id=session_state.session_id,
                distraction_type=DistractionType.INACTIVITY,
                timestamp=datetime.utcnow(),
                severity="low",
                message="Extended inactivity detected",
                action_taken="Reminder sent"
            ))
        
        # Check for multitasking indicators
        if activity_data.get("multitasking_indicators", 0) > 2:
            distractions.append(DistractionAlert(
                student_id=session_state.student_id,
                session_id=session_state.session_id,
                distraction_type=DistractionType.MULTITASKING,
                timestamp=datetime.utcnow(),
                severity="high",
                message="Multitasking detected",
                action_taken="Focus reminder sent"
            ))
        
        return distractions
    
    def _handle_distraction(self, session_state: LearningSessionState, distraction: DistractionAlert) -> DistractionAlert:
        """Handle a detected distraction"""
        # Update focus score based on distraction severity
        if distraction.severity == "high":
            session_state.focus_score -= 0.2
        elif distraction.severity == "medium":
            session_state.focus_score -= 0.1
        else:
            session_state.focus_score -= 0.05
        
        # Ensure focus score doesn't go below 0
        session_state.focus_score = max(0.0, session_state.focus_score)
        
        # Add to student's distraction history
        if session_state.student_id in self.student_activities:
            self.student_activities[session_state.student_id]["distractions"].append(distraction)
        
        return distraction
    
    def _lock_session(self, session_state: LearningSessionState):
        """Lock a session due to excessive distractions"""
        session_state.state = SessionState.LOCKED
        session_state.locked_until = datetime.utcnow() + timedelta(
            minutes=self.distraction_thresholds["lock_duration_minutes"]
        )
        
        logger.warning(f"Session {session_state.session_id} locked for student {session_state.student_id}")
    
    def _calculate_focus_score(self, session_state: LearningSessionState) -> float:
        """Calculate current focus score for the session"""
        base_score = 1.0
        distraction_penalty = session_state.distractions_count * 0.1
        
        # Time-based decay
        session_duration = datetime.utcnow() - session_state.start_time
        time_penalty = min(session_duration.total_seconds() / 3600 * 0.05, 0.3)
        
        focus_score = base_score - distraction_penalty - time_penalty
        
        return max(0.0, min(1.0, focus_score))
    
    def _get_focus_recommendations(self, session_state: LearningSessionState) -> List[str]:
        """Get focus improvement recommendations"""
        recommendations = []
        
        if session_state.focus_score < 0.5:
            recommendations.append("Take a 5-minute break and return with fresh focus")
            recommendations.append("Close all unrelated applications and tabs")
            recommendations.append("Consider switching to a quieter environment")
        
        if session_state.distractions_count > 2:
            recommendations.append("Enable 'Do Not Disturb' mode on your devices")
            recommendations.append("Use website blockers for distracting sites")
        
        if session_state.focus_score > 0.8:
            recommendations.append("Great focus! Keep up the excellent work")
        
        return recommendations
    
    def _log_distraction_event(self, session_state: LearningSessionState, distraction: DistractionAlert):
        """Log distraction event to database"""
        try:
            # In a real implementation, this would save to the database
            # For now, we'll log it
            logger.info(f"Distraction logged: {distraction.message} for student {session_state.student_id}")
        except Exception as e:
            logger.error(f"Error logging distraction: {str(e)}")
    
    def end_learning_session(self, session_id: str, session_key: str) -> Dict[str, Any]:
        """End a learning session and generate report"""
        try:
            if session_id not in self.active_sessions:
                return {"success": False, "error": "Session not found"}
            
            session_state = self.active_sessions[session_id]
            
            # Validate session key
            if session_state.session_key != session_key:
                return {"success": False, "error": "Invalid session key"}
            
            # Update session end time
            session_state.end_time = datetime.utcnow()
            session_state.state = SessionState.COMPLETED
            
            # Generate session report
            session_duration = session_state.end_time - session_state.start_time
            session_report = {
                "session_id": session_id,
                "student_id": session_state.student_id,
                "duration_minutes": session_duration.total_seconds() / 60,
                "focus_score": session_state.focus_score,
                "distractions_count": session_state.distractions_count,
                "session_efficiency": self._calculate_session_efficiency(session_state),
                "recommendations": self._get_session_recommendations(session_state)
            }
            
            # Clean up session
            del self.active_sessions[session_id]
            
            return {
                "success": True,
                "session_report": session_report
            }
            
        except Exception as e:
            logger.error(f"Session ending error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _calculate_session_efficiency(self, session_state: LearningSessionState) -> float:
        """Calculate overall session efficiency"""
        base_efficiency = session_state.focus_score
        distraction_penalty = min(session_state.distractions_count * 0.1, 0.5)
        
        efficiency = base_efficiency - distraction_penalty
        return max(0.0, efficiency)
    
    def _get_session_recommendations(self, session_state: LearningSessionState) -> List[str]:
        """Get recommendations based on session performance"""
        recommendations = []
        
        if session_state.focus_score < 0.5:
            recommendations.append("Consider shorter learning sessions with more breaks")
            recommendations.append("Work on improving focus techniques")
            recommendations.append("Review and adjust your learning environment")
        
        if session_state.distractions_count > 3:
            recommendations.append("Use distraction-blocking tools during study sessions")
            recommendations.append("Practice mindfulness techniques to improve focus")
            recommendations.append("Set specific goals for each learning session")
        
        if session_state.focus_score > 0.8 and distractions_count == 0:
            recommendations.append("Excellent session! Maintain this level of focus")
            recommendations.append("Consider gradually increasing session duration")
        
        return recommendations
    
    def get_student_focus_report(self, student_id: int) -> Dict[str, Any]:
        """Get focus and distraction report for a student"""
        try:
            if student_id not in self.student_activities:
                return {"success": False, "error": "No activity data found for student"}
            
            student_data = self.student_activities[student_id]
            
            # Calculate statistics
            total_distractions = len(student_data["distractions"])
            distraction_types = {}
            for distraction in student_data["distractions"]:
                distraction_type = distraction.distraction_type.value
                distraction_types[distraction_type] = distraction_types.get(distraction_type, 0) + 1
            
            # Calculate average focus score (simplified)
            avg_focus_score = 0.7  # This would be calculated from actual data
            
            report = {
                "student_id": student_id,
                "total_sessions": len([s for s in self.active_sessions.values() if s.student_id == student_id]),
                "total_distractions": total_distractions,
                "distraction_breakdown": distraction_types,
                "average_focus_score": avg_focus_score,
                "improvement_suggestions": self._get_improvement_suggestions(distraction_types, avg_focus_score)
            }
            
            return {"success": True, "report": report}
            
        except Exception as e:
            logger.error(f"Focus report generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _get_improvement_suggestions(self, distraction_types: Dict[str, int], focus_score: float) -> List[str]:
        """Get personalized improvement suggestions"""
        suggestions = []
        
        if distraction_types.get("tab_switch", 0) > 3:
            suggestions.append("Use website blockers to prevent tab switching")
        
        if distraction_types.get("ai_tool_usage", 0) > 0:
            suggestions.append("Complete learning sessions before using AI tools for help")
        
        if distraction_types.get("inactivity", 0) > 2:
            suggestions.append("Set timers to maintain consistent engagement")
        
        if focus_score < 0.6:
            suggestions.append("Practice the Pomodoro technique (25 minutes focus, 5 minutes break)")
        
        return suggestions
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{secrets.token_hex(8)}"
    
    def _generate_session_key(self) -> str:
        """Generate secure session key"""
        return secrets.token_urlsafe(32)

# Global anti-distraction manager instance
anti_distraction_manager = AntiDistractionManager()

class DistractionMonitoringService:
    """Service for monitoring and preventing distractions"""
    
    @staticmethod
    def create_session(student_id: int, session_type: str = "video") -> Dict[str, Any]:
        """Create a new learning session with anti-distraction features"""
        return anti_distraction_manager.create_learning_session(student_id, session_type)
    
    @staticmethod
    def validate_activity(session_id: str, session_key: str, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate student activity and detect distractions"""
        return anti_distraction_manager.validate_session_activity(session_id, session_key, activity_data)
    
    @staticmethod
    def end_session(session_id: str, session_key: str) -> Dict[str, Any]:
        """End learning session and generate report"""
        return anti_distraction_manager.end_learning_session(session_id, session_key)
    
    @staticmethod
    def get_focus_report(student_id: int) -> Dict[str, Any]:
        """Get student's focus and distraction report"""
        return anti_distraction_manager.get_student_focus_report(student_id)
    
    @staticmethod
    def get_client_scripts() -> Dict[str, str]:
        """Get JavaScript client scripts for anti-distraction monitoring"""
        return {
            "monitoring_script": """
            // Anti-Distraction Monitoring Script
            class DistractionMonitor {
                constructor(sessionId, sessionKey) {
                    this.sessionId = sessionId;
                    this.sessionKey = sessionKey;
                    this.activityInterval = null;
                    this.lastActivity = new Date();
                    this.distractions = [];
                    
                    this.init();
                }
                
                init() {
                    // Monitor tab visibility
                    document.addEventListener('visibilitychange', () => {
                        if (document.hidden) {
                            this.recordDistraction('tab_switch');
                        }
                    });
                    
                    // Monitor window focus
                    window.addEventListener('blur', () => {
                        this.recordDistraction('window_focus_loss');
                    });
                    
                    // Monitor mouse and keyboard activity
                    document.addEventListener('mousemove', () => {
                        this.lastActivity = new Date();
                    });
                    
                    document.addEventListener('keydown', () => {
                        this.lastActivity = new Date();
                    });
                    
                    // Start activity monitoring
                    this.startMonitoring();
                }
                
                startMonitoring() {
                    this.activityInterval = setInterval(() => {
                        this.sendActivityUpdate();
                    }, 30000); // Check every 30 seconds
                }
                
                stopMonitoring() {
                    if (this.activityInterval) {
                        clearInterval(this.activityInterval);
                    }
                }
                
                recordDistraction(type) {
                    this.distractions.push({
                        type: type,
                        timestamp: new Date().toISOString(),
                        severity: this.getSeverity(type)
                    });
                }
                
                getSeverity(type) {
                    const severityMap = {
                        'tab_switch': 'medium',
                        'window_focus_loss': 'medium',
                        'ai_tool_usage': 'high',
                        'inactivity': 'low'
                    };
                    return severityMap[type] || 'low';
                }
                
                async sendActivityUpdate() {
                    const activityData = {
                        tab_switch_detected: this.distractions.some(d => d.type === 'tab_switch'),
                        window_focus_lost: this.distractions.some(d => d.type === 'window_focus_loss'),
                        ai_tool_detected: this.distractions.some(d => d.type === 'ai_tool_usage'),
                        multitasking_indicators: this.distractions.length,
                        last_activity: this.lastActivity.toISOString(),
                        distractions: this.distractions
                    };
                    
                    try {
                        const response = await fetch('/api/v1/anti-distraction/validate', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${this.sessionKey}`
                            },
                            body: JSON.stringify({
                                session_id: this.sessionId,
                                session_key: this.sessionKey,
                                activity_data: activityData
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            this.handleSuccessResponse(result);
                        } else {
                            this.handleErrorResponse(result);
                        }
                        
                    } catch (error) {
                        console.error('Activity update failed:', error);
                    }
                }
                
                handleSuccessResponse(result) {
                    // Update UI based on session state
                    if (result.session_state) {
                        const state = result.session_state;
                        this.updateUIState(state);
                    }
                    
                    // Show alerts
                    if (result.alerts && result.alerts.length > 0) {
                        this.showDistractionAlerts(result.alerts);
                    }
                }
                
                handleErrorResponse(result) {
                    if (result.error === 'Session locked') {
                        this.showLockScreen(result.locked_until);
                    }
                }
                
                updateUIState(state) {
                    // Update focus score display
                    const focusElement = document.getElementById('focus-score');
                    if (focusElement) {
                        focusElement.textContent = `Focus: ${(state.focus_score * 100).toFixed(0)}%`;
                    }
                    
                    // Update distraction count
                    const distractionElement = document.getElementById('distraction-count');
                    if (distractionElement) {
                        distractionElement.textContent = `Distractions: ${state.distractions_count}`;
                    }
                }
                
                showDistractionAlerts(alerts) {
                    alerts.forEach(alert => {
                        // Show toast notification
                        this.showToast(alert.message, alert.severity);
                    });
                }
                
                showToast(message, type) {
                    // Create toast notification
                    const toast = document.createElement('div');
                    toast.className = `toast toast-${type}`;
                    toast.textContent = message;
                    
                    document.body.appendChild(toast);
                    
                    setTimeout(() => {
                        toast.remove();
                    }, 3000);
                }
                
                showLockScreen(until) {
                    // Show lock screen
                    const lockScreen = document.createElement('div');
                    lockScreen.className = 'lock-screen';
                    lockScreen.innerHTML = `
                        <div class="lock-content">
                            <h2>Session Locked</h2>
                            <p>Due to excessive distractions, your session has been locked.</p>
                            <p>Session will be available again at: ${new Date(until).toLocaleString()}</p>
                            <button onclick="location.reload()">Try Again</button>
                        </div>
                    `;
                    
                    document.body.appendChild(lockScreen);
                }
            }
            
            // Initialize monitoring when page loads
            document.addEventListener('DOMContentLoaded', () => {
                const sessionId = document.getElementById('session-id')?.value;
                const sessionKey = document.getElementById('session-key')?.value;
                
                if (sessionId && sessionKey) {
                    window.distractionMonitor = new DistractionMonitor(sessionId, sessionKey);
                }
            });
            """,
            "css_styles": """
            /* Anti-Distraction CSS Styles */
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                z-index: 1000;
                animation: slideIn 0.3s ease-in-out;
            }
            
            .toast-low { background-color: #28a745; }
            .toast-medium { background-color: #ffc107; color: #000; }
            .toast-high { background-color: #dc3545; }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            .lock-screen {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            }
            
            .lock-content {
                text-align: center;
                background: #333;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }
            
            .lock-content h2 { color: #ff4444; margin-bottom: 20px; }
            .lock-content button {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }
            
            .focus-indicator {
                position: fixed;
                top: 10px;
                left: 10px;
                background: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #007bff;
                font-weight: bold;
                z-index: 100;
            }
            """
        }