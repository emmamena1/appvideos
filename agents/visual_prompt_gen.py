"""
Visual Prompt Generator Agent (Agent 3)

Converts scripts into optimized prompts for AI image generation using Google Gemini 1.5 Pro.
"""

import json
from typing import Dict, Any, List
from google import genai
from google.genai import types
from agents import BaseAgent
from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from config.prompts import VISUAL_PROMPT_GENERATOR_SYSTEM_PROMPT, VISUAL_PROMPT_GENERATOR_USER_PROMPT


class VisualPromptGeneratorAgent(BaseAgent):
    """Agent that generates optimized prompts for image generation."""
    
    def __init__(self):
        """Initialize Visual Prompt Generator agent."""
        super().__init__("visual_prompt_generator")
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = GEMINI_MODEL or "gemini-2.0-flash"
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate visual prompts from script.
        
        Args:
            input_data: Dictionary with keys:
                - script: Script dictionary
                - format: Video format (e.g., "Vertical 9:16")
        
        Returns:
            Dictionary with visual prompts
        """
        self.validate_input(input_data, ["script"])
        
        script = input_data["script"]
        format_type = input_data.get("format", "Vertical 9:16")
        
        # Convert script to JSON string for prompt
        script_json = json.dumps(script, indent=2)
        
        # Build prompt
        prompt = VISUAL_PROMPT_GENERATOR_USER_PROMPT.format(
            script=script_json,
            format=format_type
        )
        
        # Generate prompts
        self.logger.info("Generating visual prompts from script...")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=VISUAL_PROMPT_GENERATOR_SYSTEM_PROMPT + "\n\n" + prompt
            )
            
            prompts_text = response.text
            
            # Parse JSON response
            prompts_data = self.safe_json_parse(prompts_text)
            
            # Validate structure
            if "prompts" not in prompts_data:
                raise ValueError("Response must contain 'prompts' array")
            
            if not isinstance(prompts_data["prompts"], list):
                raise ValueError("'prompts' must be an array")
            
            # Ensure each prompt has required fields
            for i, prompt_item in enumerate(prompts_data["prompts"]):
                if "prompt" not in prompt_item:
                    raise ValueError(f"Prompt {i+1} missing 'prompt' field")
                
                if "scene_number" not in prompt_item:
                    prompt_item["scene_number"] = i + 1
                
                if "negative_prompt" not in prompt_item:
                    prompt_item["negative_prompt"] = "low quality, blurry, distorted, watermark"
                
                if "aspect_ratio" not in prompt_item:
                    # Map format to aspect ratio
                    aspect_ratios = {
                        "Vertical 9:16": "9:16",
                        "Horizontal 16:9": "16:9",
                        "Cuadrado 1:1": "1:1"
                    }
                    prompt_item["aspect_ratio"] = aspect_ratios.get(format_type, "9:16")
            
            self.logger.info(f"Generated {len(prompts_data['prompts'])} visual prompts")
            
            return {
                "visual_prompts": prompts_data["prompts"],
                "script": script,
                "format": format_type
            }
        
        except Exception as e:
            self.logger.error(f"Error generating visual prompts: {str(e)}")
            raise
