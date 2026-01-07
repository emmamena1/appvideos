# config/settings.py (Versión Detective 🕵️‍♂️)
import streamlit as st
from pathlib import Path
import os

# --- 1. Definir Rutas ---
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
DATABASE_PATH = BASE_DIR / "video_studio.db"

# Crear carpetas necesarias
ASSETS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# --- 2. Función Detective para encontrar las Llaves ---
def find_key(possible_names):
    """Busca la clave en secrets.toml (con o sin sección) y en variables de entorno."""
    
    # 1. Buscar dentro de la sección [api_keys] en secrets.toml
    if "api_keys" in st.secrets:
        for name in possible_names:
            if name in st.secrets["api_keys"]:
                print(f"✅ Clave encontrada en [api_keys]: {name}")
                return st.secrets["api_keys"][name]
    
    # 2. Buscar "suelta" en el nivel principal de secrets.toml
    for name in possible_names:
        if name in st.secrets:
            print(f"✅ Clave encontrada en nivel principal: {name}")
            return st.secrets[name]
            
    # 3. Buscar en Variables de Entorno (Sistema Operativo)
    for name in possible_names:
        val = os.getenv(name)
        if val:
            print(f"✅ Clave encontrada en el Sistema (OS): {name}")
            return val
            
    print(f"❌ NO SE ENCONTRÓ NINGUNA DE ESTAS CLAVES: {possible_names}")
    return None

# --- 3. Ejecutar la Búsqueda ---
print("--- 🕵️‍♂️ INICIANDO BÚSQUEDA DE API KEYS ---")

# Busca Google/Gemini con ambos nombres posibles
GOOGLE_API_KEY = find_key(["GOOGLE_API_KEY", "GEMINI_API_KEY"])

# Busca Deepgram
DEEPGRAM_API_KEY = find_key(["DEEPGRAM_API_KEY"])

# Busca Together/Flux
TOGETHER_API_KEY = find_key(["TOGETHER_API_KEY", "TOGETHERAI_API_KEY"])

# Busca ElevenLabs (Opcional)
ELEVENLABS_API_KEY = find_key(["ELEVENLABS_API_KEY"]) or ""

print("-------------------------------------------")
