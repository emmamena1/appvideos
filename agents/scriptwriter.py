from google import genai
from google.genai import types
import json
import streamlit as st
import os
from typing import Dict, List, Optional

# --- CONFIGURACIÓN DE SEGURIDAD ---
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    client = None

class ScriptWriterAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Inicializa el agente de guion con Gemini 2.0 Flash.
        """
        self.model_name = model_name
        
        # 🧠 CEREBRO DE VENTAS (Hooks de Fricción)
        self.hook_framework = """
        ESTRUCTURA OBLIGATORIA DEL HOOK (0-5 seg):
        1. PROBLEMA: Identifica un dolor agudo y específico del usuario.
        2. CONSECUENCIA: Amplifica el daño (pérdida de dinero/tiempo).
        3. INTRIGA: Plantea una contradicción o solución desconocida.
        """
        
        # 👁️ ESTILO VISUAL GENÉRICO (Adaptable al contexto)
        self.visual_style = """
        ESTILO VISUAL (FLUX PROMPTS - INGLÉS):
        - Style: Ultra-realistic, cinematic photography that matches the topic context.
        - Lighting: Professional studio or natural lighting appropriate to the scene.
        - Quality: High resolution, sharp details, realistic textures.
        - Camera: Professional composition with depth of field.
        - Adaptability: The visual style should match the topic (tech → modern/sleek, food → appetizing/warm, etc.)
        """

    def generate_script(self, topic: str, product_name: str = "Producto") -> Optional[Dict]:
        """
        Genera un guion técnico completo en formato JSON usando Gemini.
        """
        
        system_prompt = f"""
        ACTÚA COMO: Un Director Creativo experto en Ventas Orgánicas y Contenido Viral.
        
        TU MISIÓN: Crear un guion para un Video Corto (Short/Reel) de 30-45 segundos sobre: '{topic}'.
        El objetivo es VENDER u obtener ATENCIÓN masiva para: '{product_name}'.
        
        {self.hook_framework}
        
        {self.visual_style}
        
        FORMATO DE SALIDA (JSON ESTRICTO):
        Debes devolver UNICAMENTE un objeto JSON válido con esta estructura exacta:
        {{
            "title": "Título viral del video",
            "hook_analysis": "Explicación breve de por qué este hook detiene el scroll",
            "scenes": [
                {{
                    "id": 1,
                    "role": "hook", 
                    "narration": "Texto exacto que dirá la voz en off...",
                    "visual_prompt": "Prompt detallado en INGLÉS para Flux-Schnell. Describe la escena de forma específica y coherente con el tema '{topic}'...",
                    "estimated_duration": 3.5
                }},
                {{
                    "id": 2,
                    "role": "body", 
                    "narration": "Desarrollo del problema...",
                    "visual_prompt": "Prompt visual coherente con el tema...",
                    "estimated_duration": 5.0
                }}
            ]
        }}
        
        REGLAS CRÍTICAS:
        1. La narración debe ser coloquial, directa y con ritmo rápido.
        2. Los 'visual_prompt' deben estar OBLIGATORIAMENTE en INGLÉS.
        3. Los prompts visuales deben ser ESPECÍFICOS al tema '{topic}' (evita términos genéricos).
        4. El JSON no debe tener errores de sintaxis (comas extra, etc.).
        """

        try:
            # Validar que el cliente esté configurado
            if client is None:
                st.error("❌ Error: API key de Google no configurada en secrets.toml")
                return None
            
            # Solicitamos respuesta a Gemini
            response = client.models.generate_content(
                model=self.model_name,
                contents=system_prompt
            )
            
            # Limpieza del texto por si Gemini incluye bloques ```json ... ```
            text_response = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(text_response)
            
        except Exception as e:
            st.error(f"❌ Error en ScriptWriter: {str(e)}")
            return None

if __name__ == "__main__":
    print("✅ El archivo scriptwriter.py se ha cargado correctamente.")