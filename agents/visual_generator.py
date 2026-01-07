import os
import streamlit as st
from together import Together
import base64

class VisualGeneratorAgent:
    def __init__(self):
        """
        Inicializa el agente visual con Together AI (Flux-Schnell).
        Aplica la "Fórmula Maestra" de Quantum Clic (Mockups).
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

    def generate_image(self, prompt: str, filename: str) -> str:
        """
        Genera imagen usando Flux-Schnell.
        Inyecta automáticamente el estilo 'Industrial Realism' de Quantum Clic.
        
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

            # Forzar extensión .png para calidad y compatibilidad
            if not filename.lower().endswith(".png"):
                filename = filename.rsplit(".", 1)[0] + ".png"
            
            output_path = os.path.join(output_dir, filename)

            # Cache Inteligente
            if os.path.exists(output_path):
                return output_path

            # ✨ INYECCIÓN DE ESTILO INDUSTRIAL (Basado en Agente 'Mockups' de Quantum Clic)
            # El prompt ya viene profesional desde ScriptWriter, 
            # solo aseguramos la calidad ultra-realista
            final_prompt = f"{prompt}, ultra-realistic, 8k, highly detailed, industrial photography, 50mm lens, f/2.8"

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