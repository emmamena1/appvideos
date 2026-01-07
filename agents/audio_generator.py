# agents/audio_generator.py - VERSIÓN CORREGIDA

import os
from pathlib import Path
import asyncio

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts no instalado. Ejecuta: pip install edge-tts")


class AudioGeneratorAgent:
    """
    Agente de generación de audio con Microsoft Edge TTS (GRATIS)
    Compatible con metodología Quantum Clic
    """
    
    def __init__(self):
        """
        Inicializa el generador de audio Edge TTS
        NO requiere API keys - 100% GRATIS
        """
        if not EDGE_TTS_AVAILABLE:
            raise ImportError(
                "edge-tts no instalado. Ejecuta: pip install edge-tts"
            )
        
        # Voces recomendadas para Quantum Clic (Ads Expansive)
        self.voices = {
            "mx_female": "es-MX-DaliaNeural",      # Mexicana, profesional ⭐
            "mx_male": "es-MX-JorgeNeural",        # Mexicano, confiable
            "co_female": "es-CO-SalomeNeural",     # Colombiana, energética
            "es_male": "es-ES-AlvaroNeural",       # España, formal
            "ar_male": "es-AR-TomasNeural"         # Argentina, técnico
        }
        
        # Voz por defecto para ads industriales
        self.default_voice = self.voices["mx_female"]
        
    def is_ready(self):
        """
        Validación requerida por arquitectura del proyecto
        Returns: bool
        """
        return EDGE_TTS_AVAILABLE
    
    def generate_narration(self, text, output_path, voice=None):
        """
        Genera narración profesional GRATIS con Edge TTS
        
        Args:
            text (str): Texto del guion en español
            output_path (str): Ruta absoluta donde guardar .mp3
            voice (str, optional): Voz específica o usa default
            
        Returns:
            str: Ruta absoluta del archivo generado
            
        Raises:
            ValueError: Si el texto está vacío
            FileNotFoundError: Si no se genera el audio
        """
        # Validaciones
        if not text or not text.strip():
            raise ValueError("El texto no puede estar vacío")
        
        if not self.is_ready():
            raise RuntimeError("Edge TTS no está disponible")
        
        # Usar voz por defecto si no se especifica
        voice_id = voice or self.default_voice
        
        try:
            # Convertir a ruta absoluta (regla CONTEXT.md)
            output_path = os.path.abspath(output_path)
            
            # Crear directorio assets/audio si no existe
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"[*] Generando audio GRATIS con Edge TTS...")
            print(f"   Voz: {voice_id}")
            # print(f"   Texto: {text[:50]}..." if len(text) > 50 else f"   Texto: {text}") # EVITAR UNICODE ERRORS
            
            # Generar audio usando asyncio
            asyncio.run(self._generate_audio_async(text, output_path, voice_id))
            
            # Validar que el archivo se creó
            if not Path(output_path).exists():
                raise FileNotFoundError(
                    f"Audio no generado en {output_path}"
                )
            
            file_size = Path(output_path).stat().st_size
            duration = self._estimate_duration(text)
            
            print(f"[+] Audio generado exitosamente:")
            print(f"   Archivo: {output_path}")
            print(f"   Tamaño: {file_size / 1024:.2f} KB")
            print(f"   Duración estimada: {duration:.1f}s")
            
            return output_path
            
        except Exception as e:
            print(f"[!] Error generando audio con Edge TTS:")
            print(f"   {type(e).__name__}: {e}")
            
            # Traceback completo (regla CONTEXT.md)
            import traceback
            traceback.print_exc()
            
            raise
    
    async def _generate_audio_async(self, text, output_path, voice):
        """
        Función interna async para Edge TTS
        
        Args:
            text (str): Texto a narrar
            output_path (str): Ruta del archivo
            voice (str): ID de voz de Edge TTS
        """
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    
    def _estimate_duration(self, text):
        """
        Estima duración del audio basándose en palabras
        Español: ~150 palabras por minuto
        
        Args:
            text (str): Texto narrado
            
        Returns:
            float: Duración estimada en segundos
        """
        word_count = len(text.split())
        words_per_second = 150 / 60  # ~2.5 palabras/segundo
        return word_count / words_per_second
    
    def list_voices(self):
        """
        Lista todas las voces disponibles
        Útil para testear diferentes opciones
        
        Returns:
            dict: Diccionario de voces disponibles
        """
        return self.voices


# === PRUEBA RÁPIDA DEL AGENTE ===
if __name__ == "__main__":
    """
    Test del agente de audio
    Ejecuta: python agents/audio_generator.py
    """
    
    # Inicializar agente
    try:
        agent = AudioGeneratorAgent()
        
        if not agent.is_ready():
            print("Agente no está listo")
            exit(1)
        
        # Texto de prueba (Hook Ads Expansive)
        texto_prueba = """
        ¿Estás perdiendo tiempo valioso en procesos manuales?
        Cada minuto perdido cuesta dinero a tu empresa.
        Descubre cómo automatizar tu negocio en solo 3 pasos.
        """
        
        # Generar audio
        output_dir = "assets/audio"
        os.makedirs(output_dir, exist_ok=True)
        audio_path = agent.generate_narration(
            text=texto_prueba.strip(),
            output_path="assets/audio/test_edge_tts.mp3"
        )
        
        print(f"\n[+] PRUEBA EXITOSA")
        print(f"Reproduce el audio: {audio_path}")
        
    except Exception as e:
        print(f"\n[!] PRUEBA FALLIDA: {e}")
        exit(1)
