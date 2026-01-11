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
        Busca credenciales en este orden:
        1. GCP_SERVICE_ACCOUNT_FILE (ruta a archivo JSON) - PREFERIDO
        2. GCP_SERVICE_ACCOUNT (contenido inline en TOML)
        3. GOOGLE_APPLICATION_CREDENTIALS (variable de entorno)
        """
        self.output_dir = os.path.join("assets", "generated_videos")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Cliente GenAI configurado para Vertex AI
        try:
            from google.oauth2 import service_account
            credentials = None
            
            # OPCIÓN 1: Ruta al archivo JSON (preferido, evita problemas de formato)
            if "GCP_SERVICE_ACCOUNT_FILE" in st.secrets:
                json_path = st.secrets["GCP_SERVICE_ACCOUNT_FILE"]
                if os.path.exists(json_path):
                    credentials = service_account.Credentials.from_service_account_file(
                        json_path,
                        scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
                    print(f"DEBUG: Usando credenciales desde archivo: {json_path}")
            
            # OPCIÓN 2: Contenido inline en TOML (puede tener problemas con private_key)
            elif "GCP_SERVICE_ACCOUNT" in st.secrets:
                import json
                import tempfile
                
                creds_data = st.secrets["GCP_SERVICE_ACCOUNT"]
                creds_dict = dict(creds_data)
                
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                
                # También guardar como archivo temporal
                self.temp_creds = os.path.join(tempfile.gettempdir(), "gcp_creds_veo.json")
                with open(self.temp_creds, "w") as f:
                    json.dump(creds_dict, f)
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.temp_creds
                print("DEBUG: Usando credenciales desde secrets inline")
            
            # OPCIÓN 3: Variable de entorno ya configurada
            elif "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                json_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                credentials = service_account.Credentials.from_service_account_file(
                    json_path,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                print(f"DEBUG: Usando GOOGLE_APPLICATION_CREDENTIALS: {json_path}")
            
            # Crear cliente
            self.client = genai.Client(
                vertexai=True,
                project=PROJECT_ID,
                location=LOCATION,
                credentials=credentials
            )
            self.model_id = "veo-2"  # Modelo correcto de Vertex AI (veo-001 no existe)
            print("DEBUG: Cliente Veo inicializado correctamente")
            
        except Exception as e:
            print(f"DEBUG: Error al inicializar Vertex AI Client: {e}")
            import traceback
            traceback.print_exc()
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
                config=types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                    # duration_seconds=5, # Opcional
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
