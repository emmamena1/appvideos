import os
import streamlit as st
from deepgram import DeepgramClient

class AudioGeneratorAgent:
    def __init__(self):
        """
        Inicializa el agente de audio con Deepgram Aura.
        Alineado con metodología Quantum Clic.
        """
        # Intentamos cargar la key de secrets
        self.api_key = st.secrets.get("DEEPGRAM_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                self.client = DeepgramClient(api_key=self.api_key)
            except Exception as e:
                st.error(f"❌ Error inicializando cliente Deepgram: {e}")

    def is_ready(self):
        """Verifica si el agente tiene todo lo necesario para funcionar."""
        return self.client is not None

    def generate_narration(self, text: str, filename: str) -> str:
        """
        Genera audio TTS usando Deepgram Aura (Latino).
        
        Args:
            text: Texto de narración a convertir en audio
            filename: Nombre del archivo (ej: "scene_1.wav")
        
        Returns:
            str: Ruta absoluta del archivo generado, o None si falla
        """
        if not self.is_ready():
            st.error("❌ Deepgram Client no inicializado.")
            return None

        try:
            # Asegurar directorios
            output_dir = os.path.join("assets", "audio")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)

            # 1. Cache Inteligente: Si el archivo ya existe y es válido (>0 bytes)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path

            # 2. Configuración para Deepgram SDK v5.x
            # Método: speak.v1.audio.generate()
            
            # Intentar generar en español, fallback a inglés si falla el modelo
            target_model = "aura-celeste-es"
            try:
                response = self.client.speak.v1.audio.generate(
                    text=text,
                    model=target_model
                )
            except Exception as e_es:
                st.warning(f"⚠️ Voz español '{target_model}' falló: {e_es}. Usando fallback (inglés).")
                target_model = "aura-asteria-en"
                response = self.client.speak.v1.audio.generate(
                    text=text,
                    model=target_model
                )
            
            # 4. Guardar el audio desde el generator
            with open(output_path, "wb") as audio_file:
                for chunk in response:
                    audio_file.write(chunk)
            
            # Verificar que el archivo se creó
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
            else:
                st.error("❌ El archivo de audio no se generó correctamente")
                return None

        except Exception as e:
            st.error(f"❌ Error generando audio con Deepgram: {e}")
            import traceback
            st.code(traceback.format_exc())
            return None
