# agents/audio_director.py
import os
from gtts import gTTS
# Ya no necesitamos settings ni API Keys para esto
# from config import settings 

class AudioDirectorAgent:
    def __init__(self):
        print("🔊 Inicializando motor de audio gTTS (Google Gratuito)...")

    def generate_audio(self, text, output_path, language="Español"):
        try:
            print(f"🎤 Grabando voz (Google TTS): {text[:30]}...")
            
            # Configuración para Español Latino
            lang_code = 'es'
            tld_code = 'com.mx' # Forzamos acento mexicano/latino

            if language != "Español":
                lang_code = 'en'
                tld_code = 'com'

            # --- GENERACIÓN ---
            # slow=False es velocidad normal
            tts = gTTS(text=text, lang=lang_code, tld=tld_code, slow=False)
            
            # Guardar archivo
            tts.save(str(output_path))
            
            # Verificación
            if os.path.exists(output_path):
                print(f"✅ Audio generado exitosamente: {output_path}")
                return str(output_path)
            else:
                print("❌ El archivo no aparece en el disco.")
                return None

        except Exception as e:
            print(f"❌ Error CRÍTICO en gTTS: {e}")
            return None