"""
AI Agents module for video production pipeline.

This module contains 8 specialized agents that work together to create
professional videos from user ideas.
"""

import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

__version__ = "1.0.0"


class BaseAgent(ABC):
    """Base class for all AI agents in the video production pipeline."""
    
    def __init__(self, name: str, max_retries: int = 3, retry_delay: float = 2.0):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.name = name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(f"agents.{name}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return output.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Output data dictionary
        """
        pass
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent with retry logic and error handling.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Output data dictionary
            
        Raises:
            Exception: If all retries fail
        """
        last_error = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Agent {self.name} - Attempt {attempt}/{self.max_retries}")
                start_time = time.time()
                
                result = self.process(input_data)
                
                execution_time = time.time() - start_time
                self.logger.info(f"Agent {self.name} - Completed in {execution_time:.2f}s")
                
                return {
                    "success": True,
                    "output": result,
                    "execution_time": execution_time,
                    "attempts": attempt
                }
            
            except Exception as e:
                last_error = e
                self.logger.error(f"Agent {self.name} - Attempt {attempt} failed: {str(e)}")
                
                if attempt < self.max_retries:
                    wait_time = self.retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                    self.logger.info(f"Agent {self.name} - Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Agent {self.name} - All {self.max_retries} attempts failed")
        
        # All retries failed
        raise Exception(
            f"Agent {self.name} failed after {self.max_retries} attempts. "
            f"Last error: {str(last_error)}"
        ) from last_error
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> bool:
        """
        Validate input data has required fields.
        
        Args:
            input_data: Input data dictionary
            required_fields: List of required field names
            
        Returns:
            True if valid, raises ValueError if not
        """
        missing_fields = [field for field in required_fields if field not in input_data]
        
        if missing_fields:
            raise ValueError(
                f"Agent {self.name} - Missing required fields: {', '.join(missing_fields)}"
            )
        
        return True
    
    def safe_json_parse(self, text: str) -> Dict[str, Any]:
        """
        Safely parse JSON from text, handling code blocks if present.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Parsed JSON dictionary
        """
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error: {str(e)}")
            self.logger.error(f"Text: {text[:500]}")
            raise ValueError(f"Failed to parse JSON response: {str(e)}") from e
