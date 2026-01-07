import streamlit as st
import json
import os
import PIL.Image
# FIX: Parche de compatibilidad para MoviePy 1.0.3 con Pillow reciente
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

# Importamos los agentes (Arquitectura Quantum Clic)
from agents.scriptwriter import ScriptWriterAgent
from agents.audio_generator import AudioGeneratorAgent
from agents.visual_generator import VisualGeneratorAgent
from agents.video_editor import VideoEditorAgent  # NUEVO AGENTE - Fase 4

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Video Factory AI | Quantum Clic",
    page_icon="🎬",
    layout="wide"
)

# --- ESTILOS CSS INDUSTRIAL DARK ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .stButton > button { width: 100%; border-radius: 4px; font-weight: bold; }
    .success-box { padding: 10px; background-color: #0f2e1a; border: 1px solid #238636; border-radius: 5px; }
    h1, h2, h3 { color: #f0f6fc; font-family: 'Segoe UI', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN ---
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'script_data' not in st.session_state:
    st.session_state['script_data'] = {}
if 'assets_ready' not in st.session_state:
    st.session_state['assets_ready'] = False
if 'final_video_path' not in st.session_state:
    st.session_state['final_video_path'] = None

# --- BARRA LATERAL (OPS CENTER) ---
with st.sidebar:
    st.title("🎬 OPS CENTER v2.0")
    st.caption("🎯 Arquitectura: Quantum Clic + Antigravity")
    st.markdown("---")
    
    # Verificador de Estado de APIs
    st.markdown("**🔌 Estado del Sistema:**")
    
    if "GOOGLE_API_KEY" in st.secrets:
        st.success("🧠 Brain (Gemini 2.0): ONLINE")
    else:
        st.error("🧠 Brain (Gemini): OFFLINE")
    
    st.success("🔊 Voice (Edge TTS): ONLINE (Gratis)")
    
    if "TOGETHER_API_KEY" in st.secrets:
        st.success("👁️ Visuals (Flux-Schnell): ONLINE")
    else:
        st.error("👁️ Visuals (Flux): OFFLINE")

    st.markdown("---")
    
    # Subida de Música de Fondo para Fase 4
    st.markdown("**🎵 Música de Fondo (Opcional):**")
    uploaded_music = st.file_uploader("Subir MP3/WAV", type=["mp3", "wav"], key="music_upload")
    if uploaded_music:
        os.makedirs("assets", exist_ok=True)
        music_path = os.path.join("assets", "background_music.mp3")
        with open(music_path, "wb") as f:
            f.write(uploaded_music.getbuffer())
        st.success(" Música lista para Fase 4")
    
    st.markdown("---")
    if st.button("🔄 Nuevo Proyecto"):
        st.session_state['step'] = 1
        st.session_state['script_data'] = {}
        st.session_state['assets_ready'] = False
        st.session_state['final_video_path'] = None
        st.rerun()

# ========================================================================
# PASO 1: ESTRATEGIA (Gemini 2.0 Flash + Ads Expansive)
# ========================================================================
if st.session_state['step'] == 1:
    st.title("🚀 Planificador de Producción")
    st.markdown("Define el objetivo para activar la metodología **Quantum Clic** (Ads Expansive).")
    
    col1, col2 = st.columns(2)
    topic = col1.text_input(
        "💡 Tema / Dolor del Cliente",
        placeholder="Ej: Mis anuncios de Facebook no convierten..."
    )
    product = col2.text_input(
        "🎯 Producto/Servicio a Vender",
        placeholder="Ej: Consultoría de Meta Ads"
    )

    if st.button("⚡ GENERAR GUION MAESTRO (Gemini 2.0 Flash)"):
        if topic and product:
            with st.spinner("🧠 Gemini aplicando lógica de 'Ads Expansive' (Dolor → Intriga → Solución)..."):
                try:
                    writer = ScriptWriterAgent() 
                    script = writer.generate_script(topic, product)
                    
                    if script:
                        st.session_state['script_data'] = script
                        st.session_state['step'] = 2
                        st.rerun()
                    else:
                        st.error("❌ El guion no se generó correctamente. Verifica tu API key de Gemini.")
                        
                except Exception as e:
                    st.error(f"❌ Error crítico en ScriptWriter: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        else:
            st.warning("⚠️ Faltan datos para iniciar la planificación.")

# ========================================================================
# PASO 2: APROBACIÓN HUMANA (Human-in-the-Loop + TSL)
# ========================================================================
elif st.session_state['step'] == 2:
    st.title("🛡️ Dashboard de Aprobación")
    st.markdown("Revisa y edita el guion generado. Aplica el **Creador de TSL** (CTA orgánica).")
    
    data = st.session_state['script_data']
    
    # Mostrar análisis del Hook para validación estratégica
    st.info(f"🎯 **Análisis del Hook (Ads Expansive):** {data.get('hook_analysis', 'N/A')}")
    
    with st.form("approval_form"):
        scenes = data.get('scenes', [])
        updated_scenes = []
        
        st.markdown("### 🎬 Edición de Escenas (Human-in-the-Loop)")
        st.caption("Edita la narración y los prompts visuales. Lo que apruebes será producido.")
        
        for i, scene in enumerate(scenes):
            with st.expander(
                f"Escena {i+1}: {scene.get('role', 'Clip').upper()} ({scene.get('estimated_duration', 0)}s)",
                expanded=True
            ):
                c1, c2 = st.columns(2)
                
                # Edición de Narración (CTA orgánica al final)
                nar = c1.text_area(
                    f"🗣️ Narración {i+1}",
                    scene.get('narration', ''),
                    height=120,
                    help="Si es la última escena, asegura un CTA orgánico (Ej: 'Sígueme para más' en lugar de 'SUSCRÍBETE')"
                )
                
                # Edición de Prompt Visual (Mockups - Industrial Realism)
                vis = c2.text_area(
                    f"👁️ Prompt Visual {i+1} (Inglés)",
                    scene.get('visual_prompt', ''),
                    height=120,
                    help="El sistema inyectará automáticamente el estilo 'Industrial Realism' de Quantum Clic"
                )
                
                scene['narration'] = nar
                scene['visual_prompt'] = vis
                updated_scenes.append(scene)
        
        st.markdown("---")
        
        # Botón de Aprobación Final
        submit_col1, submit_col2 = st.columns([1, 3])
        with submit_col1:
            submitted = st.form_submit_button("✅ APROBAR Y PRODUCIR ASSETS", use_container_width=True)
        
        if submitted:
            # Verificación de pre-vuelo (agentes listos)
            audio_agent = AudioGeneratorAgent()
            visual_agent = VisualGeneratorAgent()
            
            if not audio_agent.is_ready():
                st.error("❌ Edge TTS no disponible. Ejecuta: pip install edge-tts")
            elif not visual_agent.is_ready():
                st.error("❌ VisualGeneratorAgent NO está listo. Verifica TOGETHER_API_KEY en .streamlit/secrets.toml")
            else:
                # Todo OK, guardar cambios y avanzar
                st.session_state['script_data']['scenes'] = updated_scenes
                st.session_state['step'] = 3
                st.success("✅ Plan aprobado. Iniciando motores de producción...")
                st.rerun()

# ========================================================================
# PASO 3: FÁBRICA DE ASSETS (Audio + Visual + Mockups)
# ========================================================================
elif st.session_state['step'] == 3:
    st.title("⚙️ Fábrica de Multimedia en Acción")
    st.markdown("Los agentes están creando el material audiovisual con calidad **cinematográfica profesional**.")
    
    scenes = st.session_state['script_data'].get('scenes', [])
    
    if not scenes:
        st.error("❌ No hay escenas para producir")
        if st.button("← Volver"):
            st.session_state['step'] = 2
            st.rerun()
    else:
        # Inicializar agentes
        audio_agent = AudioGeneratorAgent()
        visual_agent = VisualGeneratorAgent()
        
        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        generated_assets = []
        errors = []
        total_scenes = len(scenes)
        
        # 🎬 PROCESAR CADA ESCENA
        for i, scene in enumerate(scenes):
            scene_num = i + 1
            status_text.markdown(f"### 🎬 Procesando Escena {scene_num}/{total_scenes}...")
            
            # Contenedor expandible para cada escena
            with st.expander(f"Escena {scene_num} - En Producción", expanded=True):
                col_audio, col_visual = st.columns(2)
                
                # 1️⃣ GENERAR AUDIO (Deepgram Aura)
                with col_audio:
                    st.markdown("**🎤 Generando Voz Neural (Edge TTS - Mexicana)...**")
                    audio_file = f"scene_{scene_num}.mp3"
                    audio_path = audio_agent.generate_narration(scene['narration'], audio_file)
                    
                    if audio_path:
                        st.audio(audio_path)
                        scene['audio_path'] = audio_path
                        st.success(f"✅ Audio: {audio_file}")
                    else:
                        st.error(f"❌ Fallo en audio escena {scene_num}")
                        errors.append(f"Audio escena {scene_num}")
                        scene['audio_path'] = None

                # 2️⃣ GENERAR IMAGEN (Together AI / Flux-Schnell)
                with col_visual:
                    st.markdown("**🎨 Renderizando Imagen (Flux-Schnell Ultra HD)...**")
                    img_file = f"scene_{scene_num}.png"
                    img_path = visual_agent.generate_image(scene['visual_prompt'], img_file)
                    
                    if img_path:
                        st.image(img_path, caption=f"Escena {scene_num}", use_container_width=True)
                        scene['image_path'] = img_path
                        st.success(f"✅ Imagen: {img_file}")
                    else:
                        st.error(f"❌ Fallo en imagen escena {scene_num}")
                        errors.append(f"Imagen escena {scene_num}")
                        scene['image_path'] = None
                
                # Mostrar narración
                st.caption(f"**📝 Narración:** {scene['narration'][:100]}...")
            
            generated_assets.append(scene)
            
            # Actualizar progreso
            progress = (scene_num) / total_scenes
            progress_bar.progress(progress)
        
        # 🎉 RESULTADO FINAL
        progress_bar.progress(1.0)
        status_text.markdown("### ✅ Producción Completada")
        
        if not errors:
            st.session_state['script_data']['scenes'] = generated_assets
            st.balloons()
            st.success("🎉 ¡TODOS LOS ASSETS GENERADOS CORRECTAMENTE!")
            
            # Resumen visual
            st.markdown("---")
            st.subheader("📁 Material Listo para Ensamblaje Final")
            
            for idx, s in enumerate(generated_assets):
                c1, c2, c3 = st.columns([1, 2, 4])
                
                if 'image_path' in s and s['image_path']:
                    c1.image(s['image_path'], use_container_width=True)
                
                if 'audio_path' in s and s['audio_path']:
                    c2.audio(s['audio_path'])
                
                c3.markdown(f"**Escena {idx + 1}:** *{s['narration'][:80]}...*")
            
            st.markdown("---")
            st.info("🔜 **Próximo Paso:** Fase 4 - Ensamblaje con MoviePy (VideoEditorAgent)")
            
            if st.button("🎬 Continuar al Editor de Video (Próximamente)"):
                st.session_state['step'] = 4
                st.rerun()
        
        else:
            st.error(f"⚠️ Ocurrieron {len(errors)} errores durante la generación:")
            for err in errors:
                st.warning(f"• {err}")
            
            if st.button("⬅️ Volver a Editar Escenas"):
                st.session_state['step'] = 2
                st.rerun()

# ========================================================================
# PASO 4: ENSAMBLAJE FINAL (MoviePy 1.0.3)
# ========================================================================
elif st.session_state['step'] == 4:
    st.title("🎬 Fase 4: Renderizado Final")
    st.markdown("Ensamblando video con: **Zoom Ken Burns + Subtítulos Hormozi + Audio Ducking**")
    
    # Si no se ha renderizado aún
    if not st.session_state['final_video_path']:
        with st.spinner("🔥 Ensamblando clips, aplicando zoom y mezclando audio... (Esto puede tardar 1-3 min)"):
            try:
                editor = VideoEditorAgent()
                scenes = st.session_state['script_data']['scenes']
                
                # Verificar si hay música de fondo cargada
                music_file = os.path.join("assets", "background_music.mp3")
                if not os.path.exists(music_file):
                    music_file = None
                    st.info("ℹ️ Sin música de fondo. Generando video solo con narración.")
                else:
                    st.info("🎵 Música de fondo detectada. Aplicando audio ducking al 15%.")
                
                # Ensamblar video
                video_path = editor.assemble_video(scenes, music_path=music_file)
                
                if video_path:
                    st.session_state['final_video_path'] = video_path
                    st.balloons()
                else:
                    st.error("❌ Error en el renderizado. Revisa los logs arriba para más detalles.")
                    
            except Exception as e:
                st.error(f"❌ Error crítico durante renderizado: {e}")
                import traceback
                st.code(traceback.format_exc())

    # Mostrar resultado si existe
    if st.session_state['final_video_path']:
        st.success("✅ ¡VIDEO COMPLETADO CON ÉXITO!")
        
        st.markdown("---")
        st.subheader("📺 Preview del Video Final")
        st.video(st.session_state['final_video_path'])
        
        st.markdown("---")
        
        # Información del video
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Formato", "9:16 Vertical (Shorts/Reels/TikTok)")
            st.metric("FPS", "24 (Cinematográfico)")
        with col2:
            st.metric("Codec", "H.264 + AAC")
            st.metric("Resolución", "1080x1920")
        
        st.markdown("---")
        
        # Botón de descarga
        with open(st.session_state['final_video_path'], "rb") as file:
            st.download_button(
                label="⬇️ DESCARGAR VIDEO MP4",
                data=file,
                file_name="video_quantum_clic.mp4",
                mime="video/mp4",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Opciones adicionales
        col_restart, col_back = st.columns(2)
        with col_restart:
            if st.button("🔄 Crear Nuevo Video", use_container_width=True):
                st.session_state['step'] = 1
                st.session_state['script_data'] = {}
                st.session_state['final_video_path'] = None
                st.session_state['assets_ready'] = False
                st.rerun()
        
        with col_back:
            if st.button("← Volver a Producción", use_container_width=True):
                st.session_state['step'] = 3
                st.rerun()
    
    else:
        # Si falló el renderizado, permitir volver
        if st.button("← Volver a Producción de Assets"):
            st.session_state['step'] = 3
            st.rerun()