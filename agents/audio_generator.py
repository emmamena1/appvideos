# agents/audio_generator.py - VERSIÓN EDGE TTS (GRATIS)

import os
from pathlib import Path
import edge_tts
import asyncio
import streamlit as st

class AudioGeneratorAgent:
    """
    Genera audio GRATIS con Microsoft Edge TTS.
    Reemplaza Deepgram para eliminar costos y errores de API.
    """
    
    def __init__(self):
        """
        Inicializa el agente con voz en español recomendada.
        """
        # Voces recomendadas:
        # "es-MX-DaliaNeural" - Mexicana, profesional y cálida (RECOMENDADA)
        # "es-CO-SalomeNeural" - Colombiana, energética
        self.voice = "es-MX-DaliaNeural" 
        
    def is_ready(self):
        """Siempre listo, no requiere API Key."""
        return True
    
    def generate_narration(self, text: str, filename: str) -> str:
        """
        Genera archivo de audio .mp3 usando Edge TTS.
        
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
                return output_path

            # Generar async
            asyncio.run(self._generate_audio_async(text, output_path))
            
            # Validar
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
            else:
                st.error("❌ Archivo de audio vacío o no creado")
                return None
                
        except Exception as e:
            st.error(f"❌ Error Edge TTS: {e}")
            return None
    
    async def _generate_audio_async(self, text, output_path):
        """Helper async para comunicar con edge-tts"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)

