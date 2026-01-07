import streamlit as st
from google import genai
from google.genai import types
from config import settings

st.set_page_config(page_title="Gemini Debugger")
st.title("🕵️ Gemini Model Debugger")

# Get API Key
api_key = settings.get_api_key("GEMINI")

if not api_key:
    st.error("❌ No Gemini API Key found in settings.")
else:
    st.success("✅ API Key found.")
    
    # Configure GenAI
    client = genai.Client(api_key=api_key)
    
    st.subheader("Available Models")
    
    try:
        models = list(client.models.list())
        found_models = []
        
        for m in models:
            st.text(f"• {m.name}")
            found_models.append(m.name)
        
        if not found_models:
            st.warning("No models found.")
        else:
            st.success(f"Found {len(found_models)} compatible models.")
            
    except Exception as e:
        st.error(f"Error listing models: {str(e)}")
        st.code(str(e))
