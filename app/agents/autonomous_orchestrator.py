"""
Autonomous Agent Orchestrator
Intelligently coordinates all 10 engines based on student context and needs
"""

from app.agents import (
    student_intelligence_agent,
    foundation_agent,
    simulation_agent,
    prediction_agent,
    competitive_exam_agent,
    college_mastery_agent,
    career_agent,
    multilingual_agent,
    industry_integration_agent,
    explainability_agent
)

class EduVerseAutonomousAgent:
    """
    Autonomous AI agent that makes intelligent decisions about student learning path
    """
    
    def __init__(self, student_id: int, student_profile: dict):
        self.student_id = student_id
        self.profile = student_profile
        self.language = student_profile.get("language", "English")
        self.education_level = student_profile.get("education_level", "School")
        self.learning_history = []
        self.current_state = "INITIAL_ASSESSMENT"
        
    def analyze_and_decide(self, assessment_data: dict):
        """
        Autonomous decision-making based on assessment results
        Returns: Complete learning action plan
        """
        
        # Step 1: Analyze performance using Engine 1
        analysis = student_intelligence_agent.analyze_assessment(
            assessment_data["score"],
            assessment_data["max_score"],
            assessment_data["time_taken"],
            assessment_data["difficulty"]
        )
        
        decision_tree = {
            "assessment_result": analysis,
            "actions": [],
            "reasoning": []
        }
        
        # Step 2: Autonomous decision based on weakness detection
        if analysis["weakness_detected"]:
            decision_tree["current_state"] = "WEAKNESS_DETECTED"
            
            # Check if simulation needed (Engine 2 + 3)
            failure_count = self._get_failure_count(assessment_data["topic"])
            sim_trigger = foundation_agent.check_simulation_trigger(
                failure_count, 
                assessment_data["topic"]
            )
            
            if sim_trigger["trigger_simulation"]:
                # Activate Simulation Engine
                decision_tree["actions"].append({
                    "engine": "Simulation (Engine 3)",
                    "action": "start_simulation",
                    "simulation_type": sim_trigger["simulation_type"],
                    "reason": sim_trigger["reason"]
                })
                decision_tree["reasoning"].append(
                    explainability_agent.explain_simulation_activation(
                        assessment_data["topic"],
                        failure_count,
                        analysis["percentage"]
                    )
                )
            else:
                # Activate Foundation Rebuilding
                decision_tree["actions"].append({
                    "engine": "Foundation Rebuilding (Engine 2)",
                    "action": "rebuild_foundation",
                    "topic": assessment_data["topic"]
                })
        
        else:
            decision_tree["current_state"] = "PROGRESSING_WELL"
            
            # Check if ready for exam preparation
            if self._is_exam_preparation_ready():
                decision_tree["actions"].append({
                    "engine": "Question Prediction (Engine 4)",
                    "action": "generate_priority_questions",
                    "exam_type": self.profile.get("target_exam", "School")
                })
        
        # Step 3: Career guidance check (for college students)
        if self.education_level in ["College", "University"]:
            decision_tree["actions"].append({
                "engine": "College Mastery (Engine 6)",
                "action": "check_placement_readiness",
                "department": self.profile.get("department", "Computer Science")
            })
            
            # Industry integration
            decision_tree["actions"].append({
                "engine": "Industry Integration (Engine 9)",
                "action": "suggest_industry_challenges",
                "domain": self.profile.get("domain", "Software")
            })
        
        # Step 4: Multilingual support (Engine 8)
        if self.language != "English":
            decision_tree["multilingual"] = {
                "engine": "Multilingual (Engine 8)",
                "translate_all_content": True,
                "language": self.language,
                "tts_enabled": True
            }
        
        # Step 5: Explainability for all decisions (Engine 10)
        decision_tree["explanations"] = self._generate_explanations(decision_tree)
        
        return decision_tree
    
    def continuous_learning_loop(self, student_data: dict):
        """
        Autonomous continuous learning loop
        Monitors progress and adapts learning path
        """
        
        loop_state = {
            "cycle": "continuous_monitoring",
            "student_id": self.student_id,
            "actions": []
        }
        
        # Get all assessments
        assessments = student_data.get("assessments", [])
        
        if not assessments:
            loop_state["actions"].append({
                "action": "initial_assessment",
                "reason": "No assessment data available"
            })
            return loop_state
        
        # Build skill profile
        profile = student_intelligence_agent.build_skill_profile(
            self.student_id,
            assessments
        )
        
        # Autonomous decisions based on profile
        weak_topics = profile["weak_topics"]
        strong_topics = profile["strong_topics"]
        
        # Decision 1: Focus on weak topics
        if weak_topics:
            for topic in weak_topics[:3]:  # Top 3 priorities
                loop_state["actions"].append({
                    "engine": "Foundation + Simulation",
                    "action": "intensive_learning",
                    "topic": topic,
                    "method": "adaptive_simulation"
                })
        
        # Decision 2: Exam prediction for strong areas
        if strong_topics and len(strong_topics) >= 5:
            loop_state["actions"].append({
                "engine": "Question Prediction (Engine 4)",
                "action": "generate_advanced_questions",
                "topics": strong_topics,
                "difficulty": "Hard"
            })
        
        # Decision 3: Career path analysis
        if profile["overall_performance"] >= 70:
            loop_state["actions"].append({
                "engine": "Career Intelligence (Engine 7)",
                "action": "analyze_career_fit",
                "strengths": strong_topics
            })
        
        # Decision 4: Mock test recommendation
        if self._should_take_mock_test(profile):
            loop_state["actions"].append({
                "engine": "Competitive Exam (Engine 5)",
                "action": "generate_mock_test",
                "adaptive": True,
                "focus_areas": weak_topics
            })
        
        return loop_state
    
    def predict_and_prepare(self, exam_type: str, exam_date: str):
        """
        Autonomous exam preparation strategy
        """
        
        # Calculate days remaining
        import datetime
        days_remaining = self._calculate_days_remaining(exam_date)
        
        strategy = {
            "exam_type": exam_type,
            "days_remaining": days_remaining,
            "preparation_plan": []
        }
        
        # Get student weaknesses
        weaknesses = self._get_current_weaknesses()
        
        # Generate priority questions (Engine 4)
        priority_pack = prediction_agent.generate_priority_questions(
            exam_type,
            self.profile.get("subject", "Math"),
            weaknesses
        )
        
        # Phase-based preparation
        if days_remaining > 60:
            strategy["phase"] = "Foundation Building"
            strategy["preparation_plan"].append({
                "weeks": "1-4",
                "focus": "Weak topics intensive learning",
                "engine": "Foundation + Simulation",
                "daily_hours": 3
            })
            strategy["preparation_plan"].append({
                "weeks": "5-8",
                "focus": "High probability topics",
                "engine": "Question Prediction",
                "daily_hours": 4
            })
        
        elif days_remaining > 30:
            strategy["phase"] = "Intensive Practice"
            strategy["preparation_plan"].append({
                "weeks": "1-2",
                "focus": "Priority question pack",
                "engine": "Question Prediction",
                "daily_hours": 5
            })
            strategy["preparation_plan"].append({
                "weeks": "3-4",
                "focus": "Mock tests",
                "engine": "Competitive Exam",
                "daily_hours": 6
            })
        
        else:
            strategy["phase"] = "Final Sprint"
            strategy["preparation_plan"].append({
                "days": "All remaining",
                "focus": "Mock tests + revision",
                "engine": "Competitive Exam + Prediction",
                "daily_hours": 8
            })
        
        # Add explainability
        strategy["explanation"] = explainability_agent.explain_recommendation_logic({
            "action": "Exam preparation strategy",
            "benefit": "Maximizes score based on time available"
        })
        
        return strategy
    
    def career_pathway_orchestration(self, interests: list, current_skills: list):
        """
        Autonomous career pathway planning
        """
        
        pathway = {
            "student_id": self.student_id,
            "orchestration": "autonomous",
            "steps": []
        }
        
        # Step 1: Career analysis (Engine 7)
        career_matches = career_agent.analyze_career_fit(
            interests,
            current_skills,
            {}
        )
        
        if not career_matches:
            return {"error": "No career matches found"}
        
        top_career = career_matches[0]
        pathway["recommended_career"] = top_career["career"]
        
        # Step 2: Skill gap analysis
        skill_gaps = career_agent.identify_skill_gaps(
            top_career["career"],
            current_skills
        )
        
        pathway["skill_gaps"] = skill_gaps["skill_gaps"]
        
        # Step 3: Learning roadmap
        roadmap = career_agent.generate_learning_roadmap(
            top_career["career"],
            skill_gaps["skill_gaps"]
        )
        
        pathway["steps"].append({
            "phase": "Skill Development",
            "duration": roadmap["estimated_time"],
            "engine": "Career Intelligence",
            "actions": roadmap["phases"]
        })
        
        # Step 4: College mastery (if applicable)
        if self.education_level in ["College", "University"]:
            placement_readiness = college_mastery_agent.assess_placement_readiness(
                current_skills,
                top_career["career"],
                self.profile.get("department", "Computer Science")
            )
            
            pathway["steps"].append({
                "phase": "Placement Preparation",
                "readiness": placement_readiness["status"],
                "engine": "College Mastery",
                "actions": placement_readiness["next_steps"]
            })
        
        # Step 5: Industry integration
        industry_challenges = industry_integration_agent.get_real_world_challenges(
            self.profile.get("domain", "Software"),
            "Intermediate"
        )
        
        pathway["steps"].append({
            "phase": "Industry Experience",
            "engine": "Industry Integration",
            "challenges": industry_challenges["available_challenges"]
        })
        
        # Step 6: Explainability
        pathway["explanation"] = explainability_agent.explain_career_suggestion(
            top_career["career"],
            top_career["match_score"],
            {"interests": interests, "strengths": current_skills, "matching_skills": current_skills}
        )
        
        return pathway
    
    def adaptive_difficulty_controller(self, performance_history: list):
        """
        Autonomous difficulty adjustment based on performance
        """
        
        if not performance_history:
            return {"difficulty": "Medium", "reason": "No history available"}
        
        recent_scores = [p["score"] for p in performance_history[-5:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        if avg_score >= 85:
            new_difficulty = "Hard"
            reason = "Consistently high performance - increasing challenge"
        elif avg_score >= 70:
            new_difficulty = "Medium"
            reason = "Good performance - maintaining current level"
        else:
            new_difficulty = "Easy"
            reason = "Struggling - reducing difficulty to build confidence"
        
        return {
            "current_avg": avg_score,
            "new_difficulty": new_difficulty,
            "reason": reason,
            "explanation": explainability_agent.explain_difficulty_adjustment(
                "Medium",
                new_difficulty,
                reason
            )
        }
    
    # Helper methods
    def _get_failure_count(self, topic: str):
        """Get failure count for a topic"""
        count = 0
        for record in self.learning_history:
            if record.get("topic") == topic and record.get("status") in ["Weak", "Critical"]:
                count += 1
        return count
    
    def _is_exam_preparation_ready(self):
        """Check if student is ready for exam preparation"""
        return len(self.learning_history) >= 10
    
    def _should_take_mock_test(self, profile: dict):
        """Decide if student should take mock test"""
        return profile["overall_performance"] >= 60
    
    def _calculate_days_remaining(self, exam_date: str):
        """Calculate days remaining until exam"""
        # Placeholder - implement actual date calculation
        return 45
    
    def _get_current_weaknesses(self):
        """Get current weak topics"""
        return ["Algebra", "Calculus"]  # Placeholder
    
    def _generate_explanations(self, decision_tree: dict):
        """Generate explanations for all decisions"""
        explanations = []
        for action in decision_tree.get("actions", []):
            explanations.append({
                "action": action["action"],
                "engine": action["engine"],
                "transparency": "Decision made based on performance data and learning science"
            })
        return explanations


def create_autonomous_agent(student_id: int, student_profile: dict):
    """Factory function to create autonomous agent"""
    return EduVerseAutonomousAgent(student_id, student_profile)
