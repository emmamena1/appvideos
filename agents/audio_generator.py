# agents/audio_generator.py - VERSIÓN gTTS (Google Text-to-Speech)

import os
from pathlib import Path
from gtts import gTTS
import streamlit as st
import time

class AudioGeneratorAgent:
    """
    Genera audio GRATIS con Google Text-to-Speech (gTTS).
    Versión estable sin problemas de bloqueo.
    """
    
    def __init__(self):
        """
        Inicializa el agente con configuración para español.
        """
        self.lang = "es"  # Español
        self.tld = "com.mx"  # Acento mexicano
        self.max_retries = 3
        self.retry_delay = 2
        self.default_voice = "es-MX (gTTS)"  # Para compatibilidad con app.py
        
    def is_ready(self):
        """Siempre listo, no requiere API Key."""
        return True
    
    def generate_narration(self, text: str, filename: str) -> str:
        """
        Genera archivo de audio .mp3 usando gTTS.
        
        Args:
            text: Texto a narrar
            filename: Nombre de archivo (ej: scene_1.mp3)
            
        Returns:
            str: Path absoluto al archivo generado
        """
        try:
            # Asegurar extension .mp3
            if filename.endswith(".wav"):
                filename = filename.replace(".wav", ".mp3")
                
            output_dir = os.path.join("assets", "audio")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            print(f"[*] Generando audio con gTTS: {text[:30]}...")
            
            # Generar con reintentos
            for attempt in range(self.max_retries):
                try:
                    # Crear objeto gTTS
                    tts = gTTS(
                        text=text,
                        lang=self.lang,
                        tld=self.tld,
                        slow=False
                    )
                    
                    # Guardar archivo
                    tts.save(output_path)
                    
                    # Validar
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        print(f"[SUCCESS] Audio generado en intento {attempt+1}")
                        return output_path
                    else:
                        print(f"[FAIL] Archivo vacío en intento {attempt+1}")
                        
                except Exception as e:
                    print(f"[ERROR] Intento {attempt+1} falló: {e}")
                    
                    if attempt < self.max_retries - 1:
                        if "streamlit" in str(type(st)):
                            st.warning(f"⚠️ Reintentando audio (Intento {attempt+1}/{self.max_retries})...")
                        time.sleep(self.retry_delay)
                        continue
                        
            # Si llegamos aquí, todos los intentos fallaron
            st.error(f"❌ No se pudo generar audio para: {text[:30]}...")
            return None
                
        except Exception as e:
            st.error(f"❌ Error Crítico gTTS: {e}")
            import traceback
            traceback.print_exc()
            return None

# === PRUEBA RÁPIDA ===
if __name__ == "__main__":
    agent = AudioGeneratorAgent()
    try:
        result = agent.generate_narration("Prueba de audio con Google Text to Speech en español mexicano.", "test_gtts.mp3")
        if result:
            print(f"✅ Audio generado: {result}")
        else:
            print("❌ Falló la generación")
    except Exception as e:
        print(f"Prueba fallida: {e}")
