"""
Social Optimizer Agent (Agent 8)

Generates social media metadata (title, description, hashtags) using Google Gemini 1.5 Pro.
"""

import json
from typing import Dict, Any
from google import genai
from google.genai import types
from agents import BaseAgent
from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from config.prompts import SOCIAL_OPTIMIZER_SYSTEM_PROMPT, SOCIAL_OPTIMIZER_USER_PROMPT


class SocialOptimizerAgent(BaseAgent):
    """Agent that generates social media optimization metadata."""
    
    def __init__(self):
        """Initialize Social Optimizer agent."""
        super().__init__("social_optimizer")
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = GEMINI_MODEL or "gemini-2.0-flash"
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate social media metadata.
        
        Args:
            input_data: Dictionary with keys:
                - script: Script dictionary
                - video_path: Path to final video (optional)
                - duration: Video duration in seconds
                - format: Video format
        
        Returns:
            Dictionary with social media metadata
        """
        self.validate_input(input_data, ["script"])
        
        script = input_data["script"]
        video_path = input_data.get("video_path")
        duration = input_data.get("duration", script.get("total_duration", 60))
        format_type = input_data.get("format", "Vertical 9:16")
        
        # Extract script summary
        video_title = script.get("title", "Video")
        script_summary = script.get("full_script", "")
        if not script_summary and "scenes" in script:
            # Build summary from scenes
            narration_parts = [scene.get("narration", "") for scene in script["scenes"] if scene.get("narration")]
            script_summary = " ".join(narration_parts)
        
        # Build prompt
        prompt = SOCIAL_OPTIMIZER_USER_PROMPT.format(
            video_title=video_title,
            script_summary=script_summary[:1000],  # Limit length
            duration=duration,
            format=format_type
        )
        
        # Generate metadata
        self.logger.info("Generating social media metadata...")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=SOCIAL_OPTIMIZER_SYSTEM_PROMPT + "\n\n" + prompt
            )
            
            metadata_text = response.text
            
            # Parse JSON response
            metadata = self.safe_json_parse(metadata_text)
            
            # Validate structure
            required_keys = ["title", "description", "hashtags"]
            missing_keys = [key for key in required_keys if key not in metadata]
            
            if missing_keys:
                # Fill missing keys with defaults
                if "title" not in metadata:
                    metadata["title"] = video_title
                if "description" not in metadata:
                    metadata["description"] = script_summary[:500]
                if "hashtags" not in metadata:
                    metadata["hashtags"] = []
            
            # Ensure hashtags is a list
            if not isinstance(metadata.get("hashtags"), list):
                metadata["hashtags"] = []
            
            # Limit hashtags to 15
            metadata["hashtags"] = metadata["hashtags"][:15]
            
            self.logger.info(f"Generated metadata: {metadata['title']}")
            
            return {
                "social_metadata": metadata,
                "video_path": video_path,
                "duration": duration,
                "format": format_type
            }
        
        except Exception as e:
            self.logger.error(f"Error generating social media metadata: {str(e)}")
            # Return basic metadata as fallback
            return {
                "social_metadata": {
                    "title": video_title,
                    "description": script_summary[:500] if script_summary else "",
                    "hashtags": [],
                    "keywords": [],
                    "thumbnail_suggestion": "Use first frame of video",
                    "posting_time": "Post during peak hours (9am-12pm, 5pm-9pm)",
                    "call_to_action": "Like and subscribe for more!",
                    "engagement_tips": []
                },
                "video_path": video_path,
                "duration": duration,
                "format": format_type
            }
