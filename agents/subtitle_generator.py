# agents/subtitle_generator.py
import os
import PIL.Image

# --- PARCHE PILLOW ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    try:
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

try:
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
except ImportError:
    print("⚠️ Error importando MoviePy")

FONT_NAME = 'Arial'

class SubtitleGeneratorAgent:
    def __init__(self):
        pass

    def generate_subtitles(self, script_data, total_duration, video_width=1080):
        """
        Genera subtítulos SIN usar SubtitlesClip (que está roto).
        En su lugar, crea TextClips individuales y los compone.
        """
        print(f"💬 Generando subtítulos (SIN SubtitlesClip)...")
        print(f"   ⏱️ Duración Total Video: {total_duration}s")
        
        scenes = script_data.get("scenes", [])
        if not scenes: 
            print("⚠️ No hay escenas para subtitular")
            return None

        # Margen de seguridad MUY agresivo
        safe_duration = total_duration - 1.0
        if safe_duration <= 0:
            safe_duration = total_duration * 0.9
            
        scene_duration = safe_duration / len(scenes)
        
        # Configuración Visual
        max_text_width = int(video_width * 0.85)
        video_height = 1920  # Altura estándar para shorts
        
        subtitle_clips = []
        
        for i, scene in enumerate(scenes):
            start_time = i * scene_duration
            end_time = (i + 1) * scene_duration
            
            # Limpieza de texto
            text = scene.get("narration", "").replace("*", "").strip()
            
            if not text:
                continue
            
            # Asegurar tiempos válidos
            if start_time >= end_time:
                continue
            if end_time > safe_duration:
                end_time = safe_duration
            
            duration = end_time - start_time
            if duration <= 0:
                continue
            
            try:
                # Crear TextClip individual para cada escena
                txt_clip = TextClip(
                    text,
                    font=FONT_NAME,
                    fontsize=50,
                    color='yellow',
                    stroke_color='black',
                    stroke_width=2,
                    method='caption',
                    size=(max_text_width, None),
                    align='center'
                )
                
                # Posicionar en la parte inferior
                txt_clip = (txt_clip
                    .set_start(start_time)
                    .set_duration(duration)
                    .set_position(('center', video_height * 0.78))
                )
                
                subtitle_clips.append(txt_clip)
                print(f"   ✅ Escena {i+1}: {start_time:.2f}s - {end_time:.2f}s")
                
            except Exception as e:
                print(f"   ⚠️ Error en escena {i+1}: {e}")
                continue
        
        if not subtitle_clips:
            print("⚠️ No se pudieron crear subtítulos")
            return None
        
        # Crear un clip transparente base y componer los subtítulos encima
        try:
            # Clip transparente del tamaño del video
            transparent_base = ColorClip(
                size=(video_width, video_height), 
                color=(0, 0, 0)
            ).set_opacity(0).set_duration(safe_duration)
            
            # Componer todos los subtítulos sobre el clip transparente
            subs_composite = CompositeVideoClip(
                [transparent_base] + subtitle_clips,
                size=(video_width, video_height)
            ).set_duration(safe_duration)
            
            print(f"✅ Subtítulos generados: {len(subtitle_clips)} bloques")
            return subs_composite
            
        except Exception as e:
            print(f"❌ Error al componer subtítulos: {e}")
            return None