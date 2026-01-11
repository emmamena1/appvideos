import os
import streamlit as st
import PIL.Image
# FIX: Parche ANTIALIAS para MoviePy 1.0.3 en Python 3.10+
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import *
from moviepy.video.fx.all import resize
# Importación específica para audio loop en v1.0.3
try:
    from moviepy.audio.fx.all import audio_loop
except ImportError:
    # Fallback para algunas subversiones
    from moviepy.audio.fx.audio_loop import audio_loop

class VideoEditorAgent:
    def __init__(self):
        """
        Agente de ensamblaje de video con MoviePy 1.0.3.
        Aplica: Zoom Ken Burns + Subtítulos Hormozi + Audio Ducking
        Alineado con metodología Quantum Clic.
        """
        self.output_dir = os.path.join("assets", "final_output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configuración de fuente (Arial es compatible en Windows/Linux)
        self.font = 'Arial' 
        self.fontsize = 50
        self.color = 'yellow'
        self.stroke_color = 'black'
        self.stroke_width = 2

    def create_zoom_clip(self, img_path, duration):
        """
        Aplica efecto Ken Burns (zoom suave) compatible con MoviePy 1.0.3.
        
        Args:
            img_path: Ruta a la imagen
            duration: Duración del clip en segundos
        
        Returns:
            VideoClip con efecto zoom aplicado
        """
        # Cargar imagen
        clip = ImageClip(img_path).set_duration(duration)
        
        # Redimensionar para cubrir formato 9:16 (1080x1920)
        clip = clip.resize(height=1920)
        
        # Recortar al centro para obtener 1080 de ancho exacto
        w, h = clip.size
        clip = clip.crop(x1=w/2 - 540, y1=0, width=1080, height=1920)
        
        # Efecto zoom suave (1.0 -> 1.02 sobre la duración)
        # Usamos resize con función lambda
        def zoom_function(t):
            return 1 + 0.02 * (t / duration)
        
        return clip.resize(zoom_function)

    def assemble_video(self, scenes, music_path=None, output_filename="final_video.mp4"):
        """
        Ensambla el video final: Imagen + Zoom + Audio + Texto + Música.
        
        Args:
            scenes: Lista de escenas con audio_path, image_path, narration
            music_path: Ruta opcional a música de fondo
            output_filename: Nombre del archivo de salida
        
        Returns:
            str: Ruta del video generado, o None si falla
        """
        try:
            clips = []
            
            for i, scene in enumerate(scenes):
                # 1. Validar que existan los assets
                audio_path = scene.get('audio_path')
                img_path = scene.get('image_path')
                
                if not audio_path or not os.path.exists(audio_path):
                    st.warning(f"⚠️ Saltando escena {i+1}: Falta audio")
                    continue
                if not img_path or not os.path.exists(img_path):
                    st.warning(f"⚠️ Saltando escena {i+1}: Falta imagen")
                    continue

                # 2. Cargar audio y definir duración
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration + 0.2  # Buffer para transiciones suaves
                
                # 3. Crear el clip visual (Imagen o Video)
                is_video = img_path.lower().endswith('.mp4')
                
                if is_video:
                    # Cargar Video Clip
                    v_clip = VideoFileClip(img_path)
                    
                    # Redimensionar al alto de 1920
                    v_clip = v_clip.resize(height=1920)
                    
                    # Recortar al centro para 1080 de ancho
                    vw, vh = v_clip.size
                    video_clip = v_clip.crop(x1=vw/2 - 540, y1=0, width=1080, height=1920)
                    
                    # Ajustar duración si es necesario (el audio manda)
                    if video_clip.duration < duration:
                        # Si es corto, podemos loopear o simplemente extender el último cuadro
                        video_clip = video_clip.set_duration(duration)
                    else:
                        video_clip = video_clip.set_duration(duration)
                else:
                    # Crear video clip con efecto zoom (para imágenes estáticas)
                    video_clip = self.create_zoom_clip(img_path, duration)
                
                # 4. Crear subtítulos estilo Hormozi
                txt_content = scene.get('narration', '')
                
                # Intentar crear TextClip (requiere ImageMagick)
                try:
                    txt_clip = (TextClip(txt_content, 
                                         fontsize=self.fontsize, 
                                         font=self.font, 
                                         color=self.color, 
                                         stroke_color=self.stroke_color, 
                                         stroke_width=self.stroke_width,
                                         size=(900, None), 
                                         method='caption')
                                .set_position(('center', 1400))  # Posición inferior
                                .set_duration(duration))
                    
                    # Componer imagen/video + texto
                    video_clip = CompositeVideoClip([video_clip, txt_clip])
                    
                except Exception as e:
                    st.warning(f"⚠️ No se pudo generar texto para escena {i+1}. Verifica ImageMagick: {e}")
                    # Si falla, continuar sin texto
                    pass

                # 5. Asignar audio al video
                # Si el original era video, quitamos su audio previo para poner la voz en off
                video_clip = video_clip.set_audio(audio_clip)
                clips.append(video_clip)

            if not clips:
                st.error("❌ No hay clips válidos para ensamblar")
                return None

            # 6. Concatenar todos los clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # 7. Añadir música de fondo con audio ducking
            if music_path and os.path.exists(music_path):
                bg_music = AudioFileClip(music_path)
                
                # Loop de música si es más corta que el video
                if bg_music.duration < final_video.duration:
                    bg_music = audio_loop(bg_music, duration=final_video.duration)
                else:
                    bg_music = bg_music.subclip(0, final_video.duration)
                
                # Audio Ducking: Bajar volumen de música al 15%
                bg_music = bg_music.volumex(0.15)
                
                # Mezclar narración + música
                final_audio = CompositeAudioClip([final_video.audio, bg_music])
                final_video = final_video.set_audio(final_audio)

            # 8. Exportar video final
            output_path = os.path.join(self.output_dir, output_filename)
            
            final_video.write_videofile(
                output_path, 
                fps=24,  # FPS cinematográfico estándar
                codec="libx264", 
                audio_codec="aac",
                threads=4,
                preset="medium"  # Balance velocidad/calidad
            )
            
            return output_path

        except Exception as e:
            st.error(f"❌ Error crítico en VideoEditor (MoviePy 1.0.3): {e}")
            import traceback
            st.code(traceback.format_exc())
            return None
    
    def is_ready(self):
        """Verifica si el agente está listo (siempre True, MoviePy es local)"""
        return True
