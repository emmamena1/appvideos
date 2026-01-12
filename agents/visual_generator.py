import os
import streamlit as st
from together import Together
import base64

class VisualGeneratorAgent:
    def __init__(self):
        """
        Inicializa el agente visual con Together AI (Flux-Schnell).
        Genera imágenes ultra-realistas adaptadas al contexto del guion.
        """
        self.api_key = st.secrets.get("TOGETHER_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                self.client = Together(api_key=self.api_key)
            except Exception as e:
                st.error(f"❌ Error inicializando Together AI: {e}")

    def is_ready(self):
        """Verifica si el agente está listo."""
        return self.client is not None
    
    def enhance_visual_prompt(self, original_prompt: str, narration: str) -> str:
        """
        Usa Gemini para mejorar el prompt visual asegurando coherencia con la narración.
        
        Args:
            original_prompt: Prompt visual original
            narration: Texto de la narración correspondiente
            
        Returns:
            str: Prompt mejorado con coherencia garantizada
        """
        try:
            import google.genai as genai
            
            if "GOOGLE_API_KEY" not in st.secrets:
                return original_prompt
            
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            
            enhancement_prompt = f"""Eres un experto en prompts para generación de imágenes AI.

NARRACIÓN DEL VIDEO: "{narration}"

PROMPT VISUAL ORIGINAL: "{original_prompt}"

Tu tarea es mejorar el prompt visual para que:
1. Sea 100% coherente con la narración
2. Describa una escena REAL y FÍSICA (no dispositivos electrónicos)
3. NO incluya texto, letras, palabras, UI, pantallas, teléfonos
4. Sea específico y detallado para evitar ambigüedades

REGLAS ESTRICTAS:
- Si la narración habla de PLANTAS/HUERTO: la imagen DEBE mostrar plantas reales, macetas con tierra, hojas verdes, frutas
- Si habla de PROBLEMAS: mostrar expresión preocupada de persona junto a plantas marchitas
- Si habla de SOLUCIÓN: mostrar plantas saludables, persona sonriendo con su huerto
- NUNCA uses la palabra "pots" sola (confunde con ollas), usa "plant pots" o "flower pots" o "terracotta planters"
- Agregar siempre: "ultra-realistic photography, 8K, cinematic lighting, NO TEXT, no words, no letters"

Responde SOLO con el prompt mejorado en inglés, nada más:"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=enhancement_prompt
            )
            
            enhanced = response.text.strip()
            # Limpiar comillas si las tiene
            enhanced = enhanced.strip('"').strip("'")
            
            print(f"DEBUG: Prompt original: {original_prompt[:50]}...")
            print(f"DEBUG: Prompt mejorado: {enhanced[:50]}...")
            
            return enhanced
            
        except Exception as e:
            print(f"DEBUG: Error mejorando prompt: {e}")
            return original_prompt


    def generate_image(self, prompt: str, filename: str) -> str:
        """
        Genera imagen usando Flux-Schnell.
        Aplica mejoras de calidad cinematográfica sin forzar un estilo específico.
        
        Args:
            prompt: Prompt visual en inglés (viene desde ScriptWriter)
            filename: Nombre del archivo (ej: "scene_1.png")
        
        Returns:
            str: Ruta absoluta del archivo PNG generado, o None si falla
        """
        if not self.is_ready():
            st.error("❌ Together Client no inicializado.")
            return None

        try:
            output_dir = os.path.join("assets", "images")
            os.makedirs(output_dir, exist_ok=True)

            # Forzar extensión .png
            if not filename.lower().endswith(".png"):
                filename = filename.rsplit(".", 1)[0] + ".png"
            
            output_path = os.path.join(output_dir, filename)

            # Cache DESHABILITADO - Siempre generar nueva imagen
            # if os.path.exists(output_path):
            #     return output_path

            # ✨ MEJORA DE CALIDAD GENÉRICA (No fuerza estilo industrial)
            # El prompt del scriptwriter ya define el contexto visual
            # IMPORTANTE: Prohibir texto para que las imágenes sean limpias
            final_prompt = f"{prompt}, ultra-realistic, 8k, highly detailed, cinematic lighting, professional photography, NO TEXT, no words, no letters, no typography, no watermarks, clean image without any text overlays"

            # Generación con Flux Schnell (9:16 Vertical para Shorts)
            response = self.client.images.generate(
                prompt=final_prompt,
                model="black-forest-labs/FLUX.1-schnell",
                width=1024,   # Ancho
                height=1792,  # Alto (9:16 Vertical exacto)
                steps=4,      # Flux-Schnell optimizado para 1-4 steps
                n=1,
                response_format="b64_json"
            )

            # Decodificación y guardado
            if response.data and len(response.data) > 0:
                image_data = base64.b64decode(response.data[0].b64_json)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                # Verificar que se creó correctamente
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return output_path
                else:
                    st.error("❌ La imagen no se generó correctamente")
                    return None
            else:
                st.error("❌ Together AI no retornó datos")
                return None

        except Exception as e:
            st.error(f"❌ Error generando imagen con Together AI: {e}")
            import traceback
            st.code(traceback.format_exc())
            return None