import os
import streamlit as st
import time
from google import genai
from google.genai import types
from typing import Optional

# Configuración de Vertex AI
PROJECT_ID = "gen-lang-client-0706301797"
LOCATION = "us-central1"

class VeoGeneratorAgent:
    def __init__(self):
        """
        Inicializa el agente de Google Veo usando Vertex AI.
        Requiere que el entorno tenga configuradas las Application Default Credentials
        o que se ejecute en un entorno con permisos de GCP.
        """
        self.output_dir = os.path.join("assets", "generated_videos")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Cliente GenAI configurado para Vertex AI
        try:
            self.client = genai.Client(
                vertexai=True,
                project=PROJECT_ID,
                location=LOCATION
            )
            self.model_id = "veo-001"
        except Exception as e:
            st.error(f"❌ Error al inicializar Vertex AI Client: {e}")
            self.client = None

    def generate_video_clip(self, prompt: str, aspect_ratio: str = "9:16", duration: str = "5s") -> Optional[str]:
        """
        Genera un clip de video usando Google Veo.
        
        Args:
            prompt: Descripción visual en inglés.
            aspect_ratio: Relación de aspecto (9:16 para TikTok).
            duration: Duración del clip (5s o 10s).
            
        Returns:
            Ruta al video generado (.mp4) o None si falla.
        """
        if not self.client:
            st.error("❌ Cliente de Veo no inicializado.")
            return None

        # Asegurar que el prompt esté limpio
        prompt = prompt.strip()
        
        try:
            st.info(f"🎬 Iniciando generación de video Veo (tardará ~60-90s)...")
            
            # Llamada al modelo Veo-001
            # Nota: generate_videos es una operación de larga duración (LRO)
            operation = self.client.models.generate_videos(
                model=self.model_id,
                prompt=prompt,
                config=types.GenerateVideoConfig(
                    aspect_ratio=aspect_ratio,
                    # duration_seconds=int(duration.replace('s', '')), # Opcional según SDK
                )
            )

            # Esperar a que se complete la operación
            # El SDK suele manejar el polling automáticamente si se accede al resultado
            video_result = operation.result()
            
            if not video_result.generated_videos:
                st.error("❌ Veo no generó ningún video.")
                return None

            # Obtener el primer video generado
            video = video_result.generated_videos[0]
            
            # Generar nombre de archivo único
            timestamp = int(time.time())
            filename = f"veo_{timestamp}.mp4"
            output_path = os.path.join(self.output_dir, filename)
            
            # Descargar/Guardar el video
            # El objeto video suele tener bytes o una URI de GCS
            # Si el SDK lo descarga directamente:
            with open(output_path, "wb") as f:
                f.write(video.video.data) # Acceso a los bytes según docs genai
                
            return output_path

        except Exception as e:
            st.error(f"❌ Error en la generación con Veo: {str(e)}")
            return None

    def is_ready(self) -> bool:
        """Verifica si el agente tiene acceso al cliente."""
        return self.client is not None
