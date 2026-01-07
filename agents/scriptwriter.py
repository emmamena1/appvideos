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

    def generate_script(self, topic: str, product_name: str = "Producto", num_scenes: int = 4) -> Optional[Dict]:
        """
        Genera un guion técnico completo en formato JSON usando Gemini.
        
        Args:
            topic: Tema del video
            product_name: Producto/servicio a promover
            num_scenes: Número de escenas deseadas (3-5 recomendado)
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
                    "narration": "Texto exacto que dirá la voz en off (MAX 15 palabras)...",
                    "visual_prompt": "Prompt detallado en INGLÉS para Flux-Schnell. Describe la escena de forma específica y coherente con el tema '{topic}'...",
                    "estimated_duration": 3.5
                }},
                // ... MÁS ESCENAS ...
            ]
        }}
        
        REGLAS CRÍTICAS:
        1. DEBES generar EXACTAMENTE {num_scenes} escenas (ni más, ni menos).
        2. Estructura obligatoria:
           - Escena 1: "hook" (3-4 segundos)
           - Escenas 2-{num_scenes-1}: "body" (4-6 segundos cada una)
           - Escena {num_scenes}: "cta" (3-5 segundos con llamado a la acción orgánico)
        3. La narración debe ser coloquial, directa y con ritmo rápido (máximo 15 palabras por escena).
        4. Los 'visual_prompt' deben estar OBLIGATORIAMENTE en INGLÉS.
        5. Los prompts visuales deben ser ESPECÍFICOS al tema '{topic}' (evita términos genéricos).
        6. El JSON no debe tener errores de sintaxis (comas extra, etc.).
        7. Duración total del video: 30-45 segundos.
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
            
            script_data = json.loads(text_response)
            
            # VALIDACIÓN: Asegurar que tenga el número correcto de escenas
            if len(script_data.get('scenes', [])) != num_scenes:
                st.warning(f"⚠️ Gemini generó {len(script_data['scenes'])} escenas en lugar de {num_scenes}. Reintentando...")
                # Reintentar UNA vez
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=system_prompt
                )
                text_response = response.text.replace("```json", "").replace("```", "").strip()
                script_data = json.loads(text_response)
            
            return script_data
            
        except Exception as e:
            st.error(f"❌ Error en ScriptWriter: {str(e)}")
            return None

if __name__ == "__main__":
    print("✅ El archivo scriptwriter.py se ha cargado correctamente.")