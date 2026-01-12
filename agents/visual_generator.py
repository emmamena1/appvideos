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
            
            enhancement_prompt = f"""Eres un experto en prompts para generación de imágenes AI (Flux).

NARRACIÓN DEL VIDEO: "{narration}"

PROMPT VISUAL ORIGINAL: "{original_prompt}"

Tu tarea es crear un prompt visual en INGLÉS que sea 100% coherente con la narración y que NO GENERE TEXTO.

REGLAS DE ORO PARA EVITAR TEXTO:
1. Si mencionas un libro, manual, guía o papel: descríbelo como "BLANK white cover", "unlabeled book", "plain white folder", "generic white booklet with no text".
2. PROHIBIDO mencionar: "title", "cover design", "text", "words", "letters", "typography", "logo", "branding".
3. Describe el objeto por su FORMA y COLOR físico, nunca por su contenido escrito.
4. NUNCA uses la palabra "pots" sola (confunde con ollas), usa "plant pots" o "terracotta planters".

REGLAS DE ESCENA:
- Describa una escena REAL y FÍSICA (balcones, jardines, manos reales).
- NO dispositivos electrónicos (teléfonos, pantallas).
- Estilo: Cinematic 8K photography, highly detailed, realistic textures.

Responde SOLO con el prompt final en inglés, agregando al final: ", ultra-realistic, 8k, cinematic lighting, NO TEXT, no words, no letters, no labels, blank surfaces"
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=enhancement_prompt
            )
            
            enhanced = response.text.strip()
            enhanced = enhanced.strip('"').strip("'")
            
            return enhanced
            
        except Exception as e:
            return original_prompt


    def generate_image(self, prompt: str, filename: str) -> str:
        """
        Genera imagen usando Flux-Schnell.
        
        Args:
            prompt: Prompt visual en inglés (mejorado)
            filename: Nombre del archivo
        """
        if not self.is_ready():
            st.error("❌ Together Client no inicializado.")
            return None

        try:
            output_dir = os.path.join("assets", "images")
            os.makedirs(output_dir, exist_ok=True)

            if not filename.lower().endswith(".png"):
                filename = filename.rsplit(".", 1)[0] + ".png"
            
            output_path = os.path.join(output_dir, filename)

            # ✨ REFUERZO DE SEGURIDAD CONTRA TEXTO (Pesado al inicio)
            # Ponemos las restricciones al inicio porque los modelos dan más peso a las primeras palabras
            final_prompt = f"CLEAN IMAGE WITHOUT ANY TEXT OR WORDS, NO LETTERS, NO TYPOGRAPHY, NO LABELS, {prompt}"

            response = self.client.images.generate(
                prompt=final_prompt,
                model="black-forest-labs/FLUX.1-schnell",
                width=1024,
                height=1792,
                steps=4,
                n=1,
                response_format="b64_json"
            )

            if response.data and len(response.data) > 0:
                image_data = base64.b64decode(response.data[0].b64_json)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return output_path
                
            return None

        except Exception as e:
            st.error(f"❌ Error generando imagen: {e}")
            return None
