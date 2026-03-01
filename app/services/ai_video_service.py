"""
AI Video Generation Service for EduVerse AI
Generates educational videos for each topic with easy-to-understand explanations
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import subprocess
import asyncio
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip
from moviepy.video.fx.all import fadein, fadeout
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64

from app.core.config import settings
from app.services.ai_content_service import ai_content_generator
from app.db.enhanced_models import ContentRepository, Student, Assessment
from app.db.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

class AIVideoGenerator:
    """AI-powered video generation service for educational content"""
    
    def __init__(self):
        """Initialize the AI video generator"""
        self.video_storage_path = Path("static/videos")
        self.video_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Video configuration
        self.video_config = {
            "width": 1280,
            "height": 720,
            "fps": 30,
            "font_size": 48,
            "background_color": "#1a1a1a",
            "text_color": "#ffffff",
            "accent_color": "#007bff"
        }
        
        logger.info("AI Video Generator initialized successfully")
    
    async def generate_topic_video(self, topic: str, difficulty: str, language: str = "English", duration: int = 300) -> Dict[str, Any]:
        """Generate an educational video for a specific topic"""
        try:
            # Generate script using AI content generator
            script_result = await self._generate_video_script(topic, difficulty, language)
            if not script_result["success"]:
                return {"success": False, "error": script_result["error"]}
            
            script = script_result["content"]
            
            # Generate visual assets
            visual_assets = await self._generate_visual_assets(script, topic, language)
            
            # Generate audio narration
            audio_result = await self._generate_audio_narration(script["narration"], language)
            
            # Create video
            video_result = await self._create_educational_video(
                script, visual_assets, audio_result, topic, language, duration
            )
            
            if not video_result["success"]:
                return video_result
            
            # Save to database
            video_metadata = {
                "title": script["title"],
                "topic": topic,
                "difficulty": difficulty,
                "language": language,
                "duration": duration,
                "video_path": video_result["video_path"],
                "thumbnail_path": video_result["thumbnail_path"],
                "script": script,
                "visual_assets": visual_assets
            }
            
            return {
                "success": True,
                "video_metadata": video_metadata,
                "message": f"Video generated successfully for {topic}"
            }
            
        except Exception as e:
            logger.error(f"Video generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _generate_video_script(self, topic: str, difficulty: str, language: str) -> Dict[str, Any]:
        """Generate video script using AI content generator"""
        try:
            # Use existing AI content generator to create educational content
            content_result = ai_content_generator.generate_explanation(
                topic=topic,
                difficulty=difficulty,
                language=language
            )
            
            if not content_result["success"]:
                return content_result
            
            content = content_result["content"]
            
            # Structure the content for video format
            script = {
                "title": content.get("title", f"Understanding {topic}"),
                "introduction": content.get("introduction", ""),
                "main_content": content.get("explanation", ""),
                "examples": content.get("examples", []),
                "visual_descriptions": content.get("visual_descriptions", []),
                "summary": content.get("summary", ""),
                "narration": self._create_narration_script(content),
                "scene_breakdown": self._create_scene_breakdown(content)
            }
            
            return {"success": True, "content": script}
            
        except Exception as e:
            logger.error(f"Script generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _create_narration_script(self, content: Dict[str, Any]) -> str:
        """Create a narration script from content"""
        introduction = content.get("introduction", "")
        explanation = content.get("explanation", "")
        examples = content.get("examples", [])
        summary = content.get("summary", "")
        
        # Create engaging narration
        narration_parts = []
        
        if introduction:
            narration_parts.append(f"Welcome to today's lesson on {content.get('title', 'this topic')}. {introduction}")
        
        if explanation:
            narration_parts.append(f"Let's dive into the main concept. {explanation}")
        
        for i, example in enumerate(examples[:3]):  # Limit to 3 examples
            if isinstance(example, dict):
                narration_parts.append(f"Let me show you an example. {example.get('description', '')}")
            else:
                narration_parts.append(f"Here's an example: {example}")
        
        if summary:
            narration_parts.append(f"To summarize, remember that {summary}")
        
        narration_parts.append("Thank you for watching! Practice this concept to master it.")
        
        return " ".join(narration_parts)
    
    def _create_scene_breakdown(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create scene breakdown for video production"""
        scenes = []
        
        # Introduction scene
        scenes.append({
            "scene_id": 1,
            "type": "title",
            "duration": 5,
            "content": content.get("title", "Educational Video"),
            "visual": "animated_title"
        })
        
        # Main content scenes
        main_content = content.get("explanation", "")
        if main_content:
            # Split content into segments
            segments = self._split_content_into_segments(main_content)
            for i, segment in enumerate(segments[:4]):  # Limit to 4 main segments
                scenes.append({
                    "scene_id": i + 2,
                    "type": "explanation",
                    "duration": 45,
                    "content": segment,
                    "visual": "animated_explanation"
                })
        
        # Example scenes
        examples = content.get("examples", [])
        for i, example in enumerate(examples[:2]):  # Limit to 2 examples
            scenes.append({
                "scene_id": len(scenes) + 1,
                "type": "example",
                "duration": 60,
                "content": example.get("description", "") if isinstance(example, dict) else example,
                "visual": "animated_example"
            })
        
        # Summary scene
        summary = content.get("summary", "")
        if summary:
            scenes.append({
                "scene_id": len(scenes) + 1,
                "type": "summary",
                "duration": 30,
                "content": f"In summary: {summary}",
                "visual": "summary_points"
            })
        
        return scenes
    
    def _split_content_into_segments(self, content: str) -> List[str]:
        """Split long content into manageable segments"""
        sentences = content.split('. ')
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) < 200:  # Limit segment length
                current_segment += sentence + ". "
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence + ". "
        
        if current_segment:
            segments.append(current_segment.strip())
        
        return segments[:4]  # Limit to 4 segments
    
    async def _generate_visual_assets(self, script: Dict[str, Any], topic: str, language: str) -> Dict[str, Any]:
        """Generate visual assets for the video"""
        try:
            visual_assets = {
                "background_images": [],
                "animated_elements": [],
                "diagrams": [],
                "icons": []
            }
            
            # Generate background images
            for i in range(3):
                bg_image = await self._create_background_image(topic, i)
                visual_assets["background_images"].append(bg_image)
            
            # Generate diagrams based on topic
            diagrams = await self._create_topic_diagrams(topic)
            visual_assets["diagrams"] = diagrams
            
            # Generate animated elements
            animations = await self._create_animated_elements(script["scene_breakdown"])
            visual_assets["animated_elements"] = animations
            
            return visual_assets
            
        except Exception as e:
            logger.error(f"Visual asset generation error: {str(e)}")
            return {}
    
    async def _create_background_image(self, topic: str, index: int) -> str:
        """Create a background image for the video"""
        try:
            # Create a simple gradient background
            width, height = 1280, 720
            image = Image.new('RGB', (width, height), color='#1a1a1a')
            draw = ImageDraw.Draw(image)
            
            # Add topic-related elements
            font = ImageFont.load_default()
            text = f"{topic} - Learning"
            text_width = draw.textlength(text, font=font)
            text_position = ((width - text_width) // 2, height // 2)
            
            draw.text(text_position, text, fill='#ffffff', font=font)
            
            # Save image
            filename = f"bg_{topic.replace(' ', '_')}_{index}.png"
            filepath = self.video_storage_path / filename
            image.save(filepath)
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Background image creation error: {str(e)}")
            return ""
    
    async def _create_topic_diagrams(self, topic: str) -> List[str]:
        """Create topic-specific diagrams"""
        diagrams = []
        
        try:
            # Create simple diagrams based on topic
            topics_with_diagrams = {
                "Mathematics": ["equation", "graph", "geometry"],
                "Science": ["atom", "molecule", "experiment"],
                "Programming": ["code", "flowchart", "algorithm"],
                "History": ["timeline", "map", "artifact"]
            }
            
            diagram_types = topics_with_diagrams.get(topic, ["concept"])
            
            for i, diagram_type in enumerate(diagram_types):
                diagram = await self._create_simple_diagram(diagram_type, topic, i)
                if diagram:
                    diagrams.append(diagram)
            
            return diagrams
            
        except Exception as e:
            logger.error(f"Diagram creation error: {str(e)}")
            return []
    
    async def _create_simple_diagram(self, diagram_type: str, topic: str, index: int) -> Optional[str]:
        """Create a simple diagram"""
        try:
            width, height = 400, 300
            image = Image.new('RGB', (width, height), color='#ffffff')
            draw = ImageDraw.Draw(image)
            
            if diagram_type == "equation":
                # Draw a simple equation
                draw.text((50, 50), "E = mc²", fill='#000000', font=ImageFont.load_default())
                draw.ellipse([100, 100, 300, 200], outline='#000000', width=2)
            
            elif diagram_type == "graph":
                # Draw a simple graph
                draw.line([(50, 250), (350, 250)], fill='#000000', width=2)  # X-axis
                draw.line([(50, 250), (50, 50)], fill='#000000', width=2)    # Y-axis
                draw.line([(50, 200), (300, 100)], fill='#ff0000', width=3)   # Line
            
            elif diagram_type == "flowchart":
                # Draw a simple flowchart
                draw.rectangle([100, 100, 300, 150], outline='#000000', width=2)
                draw.text((150, 120), "Start", fill='#000000', font=ImageFont.load_default())
                draw.rectangle([100, 200, 300, 250], outline='#000000', width=2)
                draw.text((150, 220), "End", fill='#000000', font=ImageFont.load_default())
                draw.line([(200, 150), (200, 200)], fill='#000000', width=2)
            
            # Save diagram
            filename = f"diagram_{topic.replace(' ', '_')}_{diagram_type}_{index}.png"
            filepath = self.video_storage_path / filename
            image.save(filepath)
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Simple diagram creation error: {str(e)}")
            return None
    
    async def _create_animated_elements(self, scenes: List[Dict[str, Any]]) -> List[str]:
        """Create animated elements for scenes"""
        animations = []
        
        try:
            for scene in scenes:
                animation = await self._create_scene_animation(scene)
                if animation:
                    animations.append(animation)
            
            return animations
            
        except Exception as e:
            logger.error(f"Animation creation error: {str(e)}")
            return []
    
    async def _create_scene_animation(self, scene: Dict[str, Any]) -> Optional[str]:
        """Create animation for a specific scene"""
        try:
            # Create a simple animation file path
            scene_type = scene.get("type", "generic")
            filename = f"animation_{scene_type}_{scene.get('scene_id', 1)}.mp4"
            filepath = self.video_storage_path / filename
            
            # For now, return the path (actual animation creation would require more complex implementation)
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Scene animation creation error: {str(e)}")
            return None
    
    async def _generate_audio_narration(self, script: str, language: str) -> Dict[str, Any]:
        """Generate audio narration for the script"""
        try:
            # For now, return a placeholder audio file
            # In a real implementation, this would use TTS services
            audio_filename = f"narration_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            audio_path = self.video_storage_path / audio_filename
            
            # Create a placeholder audio file (in real implementation, use TTS)
            # For now, return the path where audio would be stored
            return {
                "success": True,
                "audio_path": str(audio_path),
                "duration": len(script.split()) * 0.6  # Rough estimate
            }
            
        except Exception as e:
            logger.error(f"Audio narration generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _create_educational_video(
        self, 
        script: Dict[str, Any], 
        visual_assets: Dict[str, Any], 
        audio_result: Dict[str, Any],
        topic: str,
        language: str,
        duration: int
    ) -> Dict[str, Any]:
        """Create the final educational video"""
        try:
            # This is a simplified video creation
            # In a real implementation, this would use moviepy or similar libraries
            
            video_filename = f"video_{topic.replace(' ', '_')}_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            video_path = self.video_storage_path / video_filename
            
            thumbnail_filename = f"thumbnail_{topic.replace(' ', '_')}_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            thumbnail_path = self.video_storage_path / thumbnail_filename
            
            # Create placeholder files (in real implementation, create actual video)
            video_path.touch()
            thumbnail_path.touch()
            
            return {
                "success": True,
                "video_path": str(video_path),
                "thumbnail_path": str(thumbnail_path),
                "duration": duration
            }
            
        except Exception as e:
            logger.error(f"Video creation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_video_url(self, video_path: str) -> str:
        """Get the URL for a video file"""
        # In a real implementation, this would return a CDN or server URL
        return f"/static/videos/{Path(video_path).name}"
    
    def get_thumbnail_url(self, thumbnail_path: str) -> str:
        """Get the URL for a thumbnail file"""
        return f"/static/videos/{Path(thumbnail_path).name}"

# Global AI video generator instance
ai_video_generator = AIVideoGenerator()

class VideoContentManager:
    """Manager for AI-generated video content"""
    
    @staticmethod
    async def generate_topic_video(
        topic: str, 
        difficulty: str, 
        language: str = "English",
        duration: int = 300
    ) -> Dict[str, Any]:
        """Generate a video for a specific topic"""
        return await ai_video_generator.generate_topic_video(topic, difficulty, language, duration)
    
    @staticmethod
    def get_topic_videos(topic: str, language: str = "English") -> List[Dict[str, Any]]:
        """Get all videos for a specific topic"""
        # In a real implementation, this would query the database
        # For now, return a placeholder structure
        return [
            {
                "title": f"Understanding {topic}",
                "topic": topic,
                "language": language,
                "duration": 300,
                "video_url": f"/static/videos/video_{topic.replace(' ', '_')}_{language}.mp4",
                "thumbnail_url": f"/static/videos/thumbnail_{topic.replace(' ', '_')}_{language}.png",
                "difficulty": "Beginner",
                "created_at": datetime.utcnow().isoformat()
            }
        ]
    
    @staticmethod
    def get_student_video_recommendations(student_id: int, topic: str) -> List[Dict[str, Any]]:
        """Get video recommendations for a student based on their level"""
        # In a real implementation, this would analyze student data
        # For now, return basic recommendations
        return [
            {
                "title": f"{topic} - Beginner Level",
                "topic": topic,
                "difficulty": "Beginner",
                "duration": 300,
                "video_url": f"/static/videos/beginner_{topic.replace(' ', '_')}.mp4",
                "recommended": True
            },
            {
                "title": f"{topic} - Intermediate Level", 
                "topic": topic,
                "difficulty": "Intermediate",
                "duration": 450,
                "video_url": f"/static/videos/intermediate_{topic.replace(' ', '_')}.mp4",
                "recommended": False
            }
        ]

# Video caching for performance
class VideoCache:
    """Cache for video metadata and thumbnails"""
    
    def __init__(self):
        self.cache = {}
        self.max_size = 500
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get video from cache"""
        return self.cache.get(key)
    
    def set(self, key: str, video_data: Dict[str, Any]):
        """Set video in cache"""
        if len(self.cache) >= self.max_size:
            # Remove oldest item
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = video_data
    
    def clear(self):
        """Clear all cached videos"""
        self.cache.clear()

# Global video cache instance
video_cache = VideoCache()