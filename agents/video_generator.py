"""
Video Generator Agent (Agent 4)

Generates images using Together AI (Flux-Schnell) or Stability AI as fallback.
"""

import os
import base64
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from PIL import Image
import io
from agents import BaseAgent
from config.settings import (
    TOGETHER_API_KEY, TOGETHER_API_URL, TOGETHER_MODEL,
    STABILITY_API_KEY, STABILITY_API_URL,
    PROJECTS_DIR, VIDEO_RESOLUTIONS
)


class VideoGeneratorAgent(BaseAgent):
    """Agent that generates images from visual prompts."""
    
    def __init__(self):
        """Initialize Video Generator agent."""
        super().__init__("video_generator", max_retries=2)
        
        self.use_together = bool(TOGETHER_API_KEY)
        self.use_stability = bool(STABILITY_API_KEY)
        
        if not self.use_together and not self.use_stability:
            raise ValueError("At least one of TOGETHER_API_KEY or STABILITY_API_KEY must be configured")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate images from visual prompts.
        
        Args:
            input_data: Dictionary with keys:
                - visual_prompts: List of prompt dictionaries
                - project_id: Project ID
                - format: Video format
        
        Returns:
            Dictionary with paths to generated images
        """
        self.validate_input(input_data, ["visual_prompts", "project_id"])
        
        visual_prompts = input_data["visual_prompts"]
        project_id = input_data["project_id"]
        format_type = input_data.get("format", "Vertical 9:16")
        
        # Create project directory
        project_dir = PROJECTS_DIR / f"project_{project_id}"
        project_dir.mkdir(exist_ok=True)
        
        images_dir = project_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Get resolution
        resolution = VIDEO_RESOLUTIONS.get(format_type, (1080, 1920))
        width, height = resolution
        
        generated_images = []
        
        # Generate each image
        for i, prompt_data in enumerate(visual_prompts):
            scene_number = prompt_data.get("scene_number", i + 1)
            prompt = prompt_data["prompt"]
            negative_prompt = prompt_data.get("negative_prompt", "")
            
            self.logger.info(f"Generating image {scene_number}/{len(visual_prompts)}: {prompt[:50]}...")
            
            try:
                # Try Together AI first, then Stability AI
                image_path = None
                
                if self.use_together:
                    try:
                        image_path = self._generate_with_together(
                            prompt, negative_prompt, width, height, images_dir, scene_number
                        )
                    except Exception as e:
                        self.logger.warning(f"Together AI failed: {str(e)}")
                        if self.use_stability:
                            self.logger.info("Falling back to Stability AI...")
                            image_path = self._generate_with_stability(
                                prompt, negative_prompt, width, height, images_dir, scene_number
                            )
                        else:
                            raise
                elif self.use_stability:
                    image_path = self._generate_with_stability(
                        prompt, negative_prompt, width, height, images_dir, scene_number
                    )
                
                if image_path and image_path.exists():
                    generated_images.append({
                        "scene_number": scene_number,
                        "image_path": str(image_path),
                        "prompt": prompt,
                        "status": "success"
                    })
                else:
                    raise Exception(f"Failed to generate image for scene {scene_number}")
            
            except Exception as e:
                self.logger.error(f"Error generating image {scene_number}: {str(e)}")
                generated_images.append({
                    "scene_number": scene_number,
                    "image_path": None,
                    "prompt": prompt,
                    "status": "error",
                    "error": str(e)
                })
        
        # Check if all images were generated successfully
        successful_images = [img for img in generated_images if img["status"] == "success"]
        
        if not successful_images:
            raise Exception("Failed to generate any images")
        
        self.logger.info(f"Generated {len(successful_images)}/{len(visual_prompts)} images successfully")
        
        return {
            "generated_images": generated_images,
            "project_dir": str(project_dir),
            "images_dir": str(images_dir),
            "format": format_type
        }
    
    def _generate_with_together(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        output_dir: Path,
        scene_number: int
    ) -> Path:
        """Generate image using Together AI."""
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": TOGETHER_MODEL,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": 4,
            "n": 1
        }
        
        response = requests.post(TOGETHER_API_URL, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if "output" not in result or not result["output"].get("choices"):
            raise Exception("Invalid response from Together AI")
        
        # Get image data
        image_data = result["output"]["choices"][0]["image_base64"]
        image_bytes = base64.b64decode(image_data)
        
        # Save image
        image_path = output_dir / f"scene_{scene_number:03d}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        return image_path
    
    def _generate_with_stability(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        output_dir: Path,
        scene_number: int
    ) -> Path:
        """Generate image using Stability AI."""
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }
        
        payload = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30
        }
        
        response = requests.post(STABILITY_API_URL, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if "artifacts" not in result or not result["artifacts"]:
            raise Exception("Invalid response from Stability AI")
        
        # Get image data
        image_data = result["artifacts"][0]["base64"]
        image_bytes = base64.b64decode(image_data)
        
        # Save image
        image_path = output_dir / f"scene_{scene_number:03d}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        return image_path
