# agents/audio_generator.py - VERSIÓN EDGE TTS (HARDENED)

import os
from pathlib import Path
import edge_tts
import asyncio
import streamlit as st
import time

class AudioGeneratorAgent:
    """
    Genera audio GRATIS con Microsoft Edge TTS.
    Versión reforzada con reintentos anti-403 y timeout.
    """
    
    def __init__(self):
        """
        Inicializa el agente con voz en español recomendada.
        "es-MX-DaliaNeural" - Mexicana, profesional y cálida (RECOMENDADA)
        """
        self.voice = "es-MX-DaliaNeural" 
        self.max_retries = 3  # Reintentos por fallo 403
        self.retry_delay = 2  # Segundos entre reintentos
        self.default_voice = self.voice # Alias para compatibilidad con app.py
        
    def is_ready(self):
        """Siempre listo, no requiere API Key."""
        return True
    
    def generate_narration(self, text: str, filename: str) -> str:
        """
        Genera archivo de audio .mp3 usando Edge TTS con reintentos.
        
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
            
            # Cache check (>0 bytes)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"[CACHE] Audio encontrado: {output_path}")
                return output_path

            print(f"[*] Generando audio: {text[:30]}...")
            
            # Generar con reintentos
            for attempt in range(self.max_retries):
                try:
                    asyncio.run(self._generate_audio_async(text, output_path, self.voice))
                    
                    # Validar
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        print(f"[SUCCESS] Audio generado en intento {attempt+1}")
                        return output_path
                    else:
                         print(f"[FAIL] Archivo vacío en intento {attempt+1}")
                        
                except Exception as e:
                    print(f"[ERROR] Intento {attempt+1} falló: {e}")
                    
                    if "403" in str(e) and attempt < self.max_retries - 1:
                        if "streamlit" in str(type(st)): # Check si estamos en contexto streamlit
                             st.warning(f"⚠️ Error 403 (Intento {attempt+1}/{self.max_retries}). Reintentando en {self.retry_delay}s...")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        if attempt == self.max_retries - 1:
                            if "streamlit" in str(type(st)):
                                st.error("❌ No se pudo generar audio tras múltiples intentos (Posible bloqueo 403)")
                        # Si no es recuperable o último intento, no re-anzamos inmediatamente para permitir el return None final
                        pass
                        
            st.error("❌ No se pudo generar audio tras múltiples intentos")
            return None
                
        except Exception as e:
            st.error(f"❌ Error Crítico Edge TTS: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _generate_audio_async(self, text, output_path, voice_id):
        """Helper async con timeout para evitar cuelgues."""
        communicate = edge_tts.Communicate(text, voice_id)
        await asyncio.wait_for(communicate.save(output_path), timeout=30)

# === PRUEBA RÁPIDA ===
if __name__ == "__main__":
    agent = AudioGeneratorAgent()
    try:
        agent.generate_narration("Prueba de audio robusta con reintentos.", "test_hardened.mp3")
        print("Prueba completada.")
    except Exception as e:
        print(f"Prueba fallida: {e}")
