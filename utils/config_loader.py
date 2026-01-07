"""
Configuration Loader Utility

Loads configuration from Streamlit secrets or environment variables.
"""

import os
from typing import Dict, Any, Optional
import streamlit as st
from config.settings import load_api_keys_from_secrets


def load_config() -> Dict[str, Any]:
    """
    Load configuration from Streamlit secrets or environment.
    
    Returns:
        Dictionary with configuration
    """
    secrets = {}
    
    try:
        # Try to get Streamlit secrets
        if hasattr(st, "secrets"):
            secrets = dict(st.secrets) if st.secrets else {}
    except:
        pass
    
    # Load API keys
    load_api_keys_from_secrets(secrets)
    
    return {
        "secrets": secrets,
        "api_keys_loaded": True
    }


def get_api_key(key_name: str, secrets: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Get API key from secrets or environment.
    
    Args:
        key_name: Name of API key
        secrets: Streamlit secrets dictionary (optional)
    
    Returns:
        API key value or None
    """
    # Try secrets first
    if secrets:
        value = secrets.get(key_name)
        if value:
            return value
    
    # Try environment
    return os.getenv(key_name)
