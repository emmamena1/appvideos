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
from agents.video_editor import VideoEditorAgent
from agents.veo_generator import VeoGeneratorAgent
from agents.researcher import ResearcherAgent
  # NUEVO AGENTE - Fase 4


# --- SISTEMA MULTI-PRODUCTO ---
# Cada producto tiene su propio template, hooks, precio y bonos

PRODUCTOS_DISPONIBLES = {
    "🍊 Frutíferas en Macetas": {
        "nombre": "El Secreto de las Frutíferas en Macetas",
        "template": """
📚 MANUAL: 'El Secreto de las Frutíferas en Macetas' - 13 CAPÍTULOS

🎯 PROBLEMAS QUE RESUELVE (Por Capítulo):
• Capítulo 3: Drenaje perfecto (90% de los fallos vienen de aquí)
• Capítulo 4: Sustrato aireado (clave para raíces sanas)
• Capítulo 6: Cítricos enanos para departamentos
• Capítulo 9: Fertilizante casero de cocina
• Capítulo 11: Calendario de riego 90 días

💰 OFERTA EXACTA:
Precio original: $47
Precio promocional: $7 USD

🎁 4 BONOS INCLUIDOS:
1. Lista de macetas exactas (valor $12)
2. Checklist de errores fatales (valor $15)
3. Fertilizantes de cocina (valor $10)
4. Calendario de cosecha (valor $10)

🔥 CTA SIEMPRE:
"Manual $7 + 4 bonos GRATIS - Link en bio"

📖 ESTRUCTURA DEL MANUAL:
Los 13 capítulos cubren desde selección de macetas hasta cosecha completa.
Cada capítulo tiene soluciones paso a paso probadas.
""",
        "hooks": {
            "Drenaje": "Capítulo 3 (Drenaje perfecto - 90% de fallos)",
            "Dinero": "Ahorro vs supermercado (ROI en 90 días)",
            "Espacio": "Capítulo 6 (Cítricos enanos para departamentos)",
            "Tiempo": "Capítulo 11 (Calendario de riego automático 90 días)"
        },
        "precio": "$7",
        "bonos": 4
    },
    
    "💼 Marketing Digital Pro": {
        "nombre": "Curso Completo de Marketing Digital",
        "template": """
📚 CURSO: 'Marketing Digital desde Cero' - 8 MÓDULOS

🎯 PROBLEMAS QUE RESUELVE (Por Módulo):
• Módulo 2: Targeting avanzado (encuentra tu audiencia exacta)
• Módulo 3: CTR bajo en anuncios (mejora clicks 300%)
• Módulo 5: ROI negativo (convierte en positivo en 30 días)
• Módulo 6: Copy que no vende (fórmulas probadas)
• Módulo 8: Escalamiento sostenible

💰 OFERTA EXACTA:
Precio original: $297
Precio promocional: $27 USD

🎁 5 BONOS INCLUIDOS:
1. Templates de anuncios (valor $97)
2. Script de ventas VSL (valor $147)
3. Calculadora de ROI (valor $47)
4. Acceso comunidad privada (valor $197/mes)
5. Sesión 1-a-1 estrategia (valor $497)

🔥 CTA SIEMPRE:
"Curso completo $27 + 5 bonos - Link en bio"

📖 ESTRUCTURA DEL CURSO:
8 módulos con +50 lecciones en video sobre ads, funnels, copy y escalamiento.
""",
        "hooks": {
            "CTR": "Módulo 3 (Optimización de CTR - +300% clicks)",
            "ROI": "Módulo 5 (ROI positivo en 30 días)",
            "Audiencia": "Módulo 2 (Targeting avanzado FB/IG)",
            "Escalamiento": "Módulo 8 (Escala de $100 a $10K/día)"
        },
        "precio": "$27",
        "bonos": 5
    },
    
    "💪 Fitness en Casa": {
        "nombre": "Transformación Fitness 90 Días",
        "template": """
📚 PROGRAMA: 'Transformación Fitness 90 Días' - SIN GIMNASIO

🎯 PROBLEMAS QUE RESUELVE:
• Semana 1-2: Rutinas sin equipo (resultados visibles en 14 días)
• Semana 3-4: Plan nutricional simple (sin dietas extremas)
• Semana 5-8: Quema grasa localizada (abdomen, brazos, piernas)
• Semana 9-12: Mantenimiento sostenible (resultados permanentes)

💰 OFERTA EXACTA:
Precio original: $97
Precio promocional: $17 USD

🎁 3 BONOS INCLUIDOS:
1. 50 recetas fitness (valor $27)
2. Tracker de progreso app (valor $47)
3. Grupo WhatsApp soporte (valor $97/mes)

🔥 CTA SIEMPRE:
"Programa completo $17 + 3 bonos - Link en bio"

📖 ESTRUCTURA:
12 semanas de rutinas progresivas + plan nutricional + seguimiento.
""",
        "hooks": {
            "Tiempo": "Resultados en 14 días (Semana 1-2)",
            "Sin Gym": "Desde casa sin equipo (rutinas completas)",
            "Grasa": "Quema grasa localizada (Semana 5-8)",
            "Sostenible": "Mantenimiento permanente (Semana 9-12)"
        },
        "precio": "$17",
        "bonos": 3
    }
}

# LEGACY: Mantener compatibilidad con código existente
PRODUCTO_TEMPLATE = PRODUCTOS_DISPONIBLES["🍊 Frutíferas en Macetas"]["template"]
HOOK_TO_CHAPTER = PRODUCTOS_DISPONIBLES["🍊 Frutíferas en Macetas"]["hooks"]

# --- GENERADOR DE IDEAS DE TEMAS ---
def generate_ideas_tema(producto_tipo: str = "general") -> list:
    """
    Genera 5 ideas de temas/títulos virales usando Gemini.
    
    Args:
        producto_tipo: Tipo de producto para contextualizar las ideas
        
    Returns:
        Lista de 5 ideas de temas
    """
    from agents.scriptwriter import client
    
    if not client:
        return ["❌ Gemini no disponible - verifica API key"]
    
    prompt = f"""Eres un experto en marketing viral y contenido TikTok.

Genera EXACTAMENTE 5 ideas de temas/dolores de cliente para videos virales.
Contexto del producto: {producto_tipo}

REGLAS:
- Cada idea debe ser un DOLOR o PROBLEMA específico del cliente
- Deben ser temas que generen curiosidad y detengan el scroll
- Usa lenguaje coloquial (español latino neutro)
- Máximo 10-15 palabras por idea
- NO uses emojis ni numeración

FORMATO DE RESPUESTA (una idea por línea):
Mis anuncios de Facebook queman dinero sin generar ventas
Por qué mi planta se muere aunque la riego todos los días
No puedo bajar de peso aunque hago ejercicio diario
Mi negocio no genera clientes por redes sociales
Mis videos no tienen visualizaciones aunque son buenos

GENERA 5 IDEAS DIFERENTES Y ÚNICAS:"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Parsear respuesta - una idea por línea
        ideas = [line.strip() for line in response.text.strip().split('\n') if line.strip() and len(line.strip()) > 10]
        return ideas[:5] if ideas else ["No se generaron ideas. Intenta de nuevo."]
        
    except Exception as e:
        return [f"Error: {str(e)}"]

# --- FUNCIONES DE AUTO-GENERACIÓN ---
def parse_gemini_scenes(response_text: str) -> list:
    """
    Parsea la respuesta de Gemini para extraer las escenas.
    Formato esperado:
    ESCENA 1: [TEXTO] | [PROMPT IMAGEN]
    ESCENA 2: [TEXTO] | [PROMPT IMAGEN]
    ...
    """
    escenas = []
    lines = response_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('ESCENA'):
            try:
                # Remover "ESCENA X:" del inicio
                content = line.split(':', 1)[1].strip()
                # Separar por el pipe |
                if '|' in content:
                    texto, prompt = content.split('|', 1)
                    escenas.append({
                        'texto': texto.strip(),
                        'prompt': prompt.strip()
                    })
            except Exception as e:
                st.warning(f"⚠️ Error parseando línea: {line[:50]}... - {e}")
                continue
    
    return escenas

def generate_auto_escenas(tema: str, producto: str, hook: str, producto_config: dict = None) -> list:
    """
    Genera automáticamente 4 escenas usando Gemini para TikTok.
    
    Args:
        tema: El tema del video (ej: "Gente en depa sin jardín")
        producto: El producto a vender (ej: "Manual $7")
        hook: Tipo de hook (Drenaje, Dinero, Espacio)
        producto_config: Configuración del producto (template, hooks, precio, bonos)
    
    Returns:
        Lista de diccionarios con 'texto' y 'prompt' para cada escena
    """
    from google import genai
    
    # Validar cliente Gemini
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ GOOGLE_API_KEY no configurado en secrets.toml")
        return []
    
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Si no se proporciona producto_config, usar valores legacy
    if producto_config is None:
        producto_config = PRODUCTOS_DISPONIBLES["🍊 Frutíferas en Macetas"]
    
    # Usar el template del producto seleccionado
    template_producto = producto_config['template']
    hooks_producto = producto_config['hooks']
    
    # Obtener el capítulo/módulo sugerido según el hook
    capitulo_sugerido = hooks_producto.get(hook, "Manual completo")
    
    
    prompt = f"""
{template_producto}

CONTEXTO DEL VIDEO:
Tema: {tema}
Hook enfocado en: {hook}
Producto: {producto}
Referencia sugerida para usar: {capitulo_sugerido}

SISTEMA DE COPYWRITING PROFESIONAL (NIVEL 99%):

1. FRAMEWORK PAS (ESTRICTO):
   - ESCENA 1 (Problema/Hook): Empieza con un "Scroll-Stopper". Una pregunta dolorosa o una estadística que detenga el scroll instantáneamente.
   - ESCENA 2 (Agitación): Pon sal en la herida. Explica por qué el problema es frustrante, costoso o vergonzoso. Haz que sientan la necesidad de cambiar.
   - ESCENA 3 (Solución): Presenta "{capitulo_sugerido}" como el puente entre su dolor actual y el resultado deseado. Usa posesivos ("mi guía", "mi manual").
   - ESCENA 4 (Acción): CTA directo y humano con reducción de riesgo (bonos incluidos).

2. LENGUAJE NATURAL Y PERSUASIVO:
   - Usa tono de "amigo experto". Nada de lenguaje corporativo.
   - Prohibido: revolucionario, increíble, secreto, descubre, domina, maximiza.
   - Usa: "esto funciona", "resulta que", "encontré la forma de", "después de fallar mil veces encontré esto".

3. STORYTELLING:
   - "3 de cada 4 personas fallan en esto por una sola razón..."
   - "Ahorré $200 al mes simplemente cambiando el capítulo 3..."
   - "Mi mayor error fue no saber lo que explico en mi manual..."

GENERA EXACTAMENTE 4 ESCENAS (45 segundos total):

ESTRUCTURA TÉCNICA:
- Escena 1 (0-3s): PAS - Problema/Hook de alto impacto (MAX 12 palabras)
- Escena 2 (3-20s): PAS - Agitación del dolor con datos o experiencias (MAX 18 palabras)
- Escena 3 (20-38s): PAS - Solución natural mencionando "{capitulo_sugerido}" (MAX 18 palabras)
- Escena 4 (38-45s): PAS - CTA Humano con bonos de regalo (MAX 15 palabras)

FORMATO DE RESPUESTA (ESTRICTO):
ESCENA 1: [texto natural español] | [prompt imagen INGLÉS cinematográfico]
ESCENA 2: [texto natural español] | [prompt imagen INGLÉS cinematográfico]
ESCENA 3: [referencia natural + {capitulo_sugerido}] | [prompt imagen INGLÉS cinematográfico]
ESCENA 4: [oferta humana personal con bonos] | [prompt imagen INGLÉS call-to-action]

REGLAS CRITICAS PARA PROMPTS VISUALES (OBLIGATORIO):

PROHIBIDO EN PROMPTS VISUALES:
- NO teléfonos, smartphones, tablets, laptops, pantallas
- NO interfaces de usuario, apps, botones, UI elements
- NO texto, letras, palabras, tipografía, logos
- NO mockups digitales ni gráficos abstractos
- NO manos sosteniendo dispositivos electrónicos

OBLIGATORIO EN PROMPTS VISUALES:
- SOLO escenas reales, físicas y tangibles relacionadas con el tema: {tema}
- Personas REALES haciendo actividades relacionadas con el producto
- Objetos físicos: plantas, macetas, tierra, frutas, herramientas de jardinería (si es sobre plantas)
- Escenarios reales: balcones, terrazas, patios, interiores de casa, jardines
- Estilo: "Cinematic 8K photography, depth of field, professional lighting, natural colors, ultra-realistic, NO TEXT, no words, no letters"

EJEMPLOS DE PROMPTS VISUALES CORRECTOS:
- "Close-up of hands planting a small lemon tree in a terracotta pot on a sunny balcony, cinematic 8K photography, depth of field, natural lighting, NO TEXT"
- "A woman smiling widely, holding a BLANK white book with NO TEXT on the cover, standing next to lush tomato plants, sunny garden setting, 8k detailed, ultra-realistic"
- "Close-up of a PLAIN white folder with NO LABELS or writing, placed on a wooden gardening table next to seeds and soil, cinematic lighting, ultra-realistic"

EJEMPLOS INCORRECTOS:
- "Hand holding smartphone showing gardening app..."
- "Digital mockup of ebook cover with title 'Tomato Guide'..."
- "Phone screen displaying product offer with text..."
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Parsear respuesta
        escenas = parse_gemini_scenes(response.text)
        
        if len(escenas) != 4:
            st.warning(f"⚠️ Se esperaban 4 escenas, se obtuvieron {len(escenas)}. Reintentando...")
            # Reintentar una vez
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            escenas = parse_gemini_scenes(response.text)
        
        return escenas
        
    except Exception as e:
        st.error(f"❌ Error generando escenas: {e}")
        import traceback
        st.code(traceback.format_exc())
        return []

def parse_gemini_guion(texto: str) -> list:
    """
    Parsea texto crudo de Gemini y extrae escenas automáticamente.
    Detecta timestamps, narraciones y prompts visuales.
    
    Args:
        texto: Texto completo de Gemini (puede incluir timestamps)
    
    Returns:
        Lista de diccionarios con 'texto' y 'prompt' para cada escena
    """
    import re
    
    escenas = []
    
    # Método 1: Buscar timestamps formato (0:00-0:03)
    timestamps_pattern = r'\((\d+:\d+-\d+:\d+)\)\s*(.+?)(?=\(|$)'
    matches_timestamps = re.findall(timestamps_pattern, texto, re.DOTALL)
    
    if matches_timestamps:
        # Extraer narraciones con timestamps
        narraciones = [match[1].strip() for match in matches_timestamps[:4]]
    else:
        # Método 2: Buscar por líneas que parecen narraciones
        # Asumiendo que las narraciones son párrafos cortos
        lines = texto.split('\n')
        narraciones = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20][:4]
    
    # Buscar prompts visuales (usualmente en inglés y descriptivos)
    # Patrón: Líneas que empiezan con mayúscula y tienen palabras en inglés
    prompt_pattern = r'([A-Z][a-z]+.*?(?:shot|photo|view|scene|apartment|balcony|plant|professional).*?)(?=\n[A-Z]|\n\n|$)'
    prompts_raw = re.findall(prompt_pattern, texto, re.IGNORECASE)
    
    # Si no se encuentran prompts, usar prompts genéricos
    if not prompts_raw or len(prompts_raw) < 4:
        prompts_raw = [
            "Ultra-realistic cinematic shot, professional lighting, high detail",
            "Professional photography, natural lighting, sharp focus",
            "Cinematic composition, depth of field, realistic textures",
            "High quality photo, professional setup, attractive scene"
        ]
    
    # Construir escenas (mínimo 4)
    for i in range(4):
        escena = {
            'texto': narraciones[i].strip() if i < len(narraciones) else f"Narración escena {i+1}",
            'prompt': prompts_raw[i].strip() if i < len(prompts_raw) else "Balcony apartment with plants and natural lighting"
        }
        escenas.append(escena)
    
    return escenas

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="Video Factory AI | Quantum Clic",
    page_icon="🎬",
    layout="wide"
)

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #111111; color: #ffffff; }
    .stButton > button { width: 100%; border-radius: 4px; font-weight: bold; }
    .success-box { padding: 10px; background-color: #0f2e1a; border: 1px solid #238636; border-radius: 5px; }
    h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN ---
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'veo_agent' not in st.session_state:
    st.session_state.veo_agent = VeoGeneratorAgent()
if 'use_video' not in st.session_state:
    st.session_state.use_video = False
if 'script_data' not in st.session_state:
    st.session_state['script_data'] = {}
if 'assets_ready' not in st.session_state:
    st.session_state['assets_ready'] = False
if 'final_video_path' not in st.session_state:
    st.session_state['final_video_path'] = None
if 'audio_agent' not in st.session_state:
    st.session_state.audio_agent = AudioGeneratorAgent()
if 'visual_agent' not in st.session_state:
    st.session_state.visual_agent = VisualGeneratorAgent()
if 'researcher_agent' not in st.session_state:
    st.session_state.researcher_agent = ResearcherAgent()
if 'url_data' not in st.session_state:
    st.session_state.url_data = None

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

    if st.session_state.veo_agent.is_ready():
        st.success("🎥 Video (Google Veo): ONLINE")
    else:
        st.error("🎥 Video (Google Veo): OFFLINE")
        with st.expander("🔑 Cómo activar Google Veo:", expanded=True):
            st.markdown("""
            **Opción A (Recomendada):**
            Instala [GCloud SDK](https://cloud.google.com/sdk/docs/install-sdk) y ejecuta:
            `gcloud auth application-default login`
            
            **Opción B (Sin instalar nada):**
            1. Crea una **Service Account** en GCP Console.
            2. Descarga el JSON de la llave.
            3. Entra a `.streamlit/secrets.toml` y pega:
            `GCP_SERVICE_ACCOUNT = { ... tu json ... }`
            """)

    st.markdown("---")
    
    # 🆕 Selector de Modo Visual (Global en Sidebar)
    st.markdown("**🎨 Modo de Generación Visual:**")
    visual_mode = st.radio(
        "Preferir:",
        ["🖼️ Imagen (Flux)", "🎥 Video (Veo)"],
        index=1 if st.session_state.use_video else 0,
        help="Video (Veo) es premium y tarda más. Imágenes (Flux) es ultra rápido."
    )
    st.session_state.use_video = "Video" in visual_mode

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
    
    # 🔗 GLOBAL: INVESTIGACIÓN POR URL (Pippit Logic)
    with st.expander("🔗 Investigación por URL (Opcional - Pippit AI Logic)", expanded=False):
        url_input = st.text_input("Pega la URL del producto (Amazon, Shopify, etc.):", placeholder="https://example.com/product")
        if st.button("🔍 Extraer Datos del Producto", key="global_research_btn"):
            if url_input:
                with st.spinner("🤖 El Researcher Agent está analizando la página..."):
                    data = st.session_state.researcher_agent.analyze_url(url_input)
                    if "error" in data:
                        st.error(f"❌ Error al analizar la URL: {data['error']}")
                    else:
                        st.session_state.url_data = data
                        st.success("✅ Datos extraídos correctamente!")
                        st.json(data)
            else:
                st.warning("⚠️ Ingresa una URL primero.")
        
        st.caption("💡 **Tip:** Si el link falla, pega una descripción del producto abajo:")
        product_desc_manual = st.text_area("Descripción manual (Opcional):", placeholder="Ej: Vendo un curso de hidroponía para departamentos pequeños...", height=100)
        if st.button("🧠 Usar esta descripción", key="use_manual_desc_btn"):
            if product_desc_manual:
                st.session_state.url_data = {
                    "nombre_producto": "Producto Personalizado",
                    "dolor_principal": product_desc_manual,
                    "beneficios": ["Extraído de descripción manual"],
                    "ganchos_sugeridos": ["Hook personalizado"]
                }
                st.success("✅ Descripción guardada!")
            else:
                st.warning("⚠️ Escribe algo primero.")
    
    st.markdown("---")
    modo = st.radio(
        "🎯 Modo de trabajo:",
        ["📝 Manual (actual)", "🚀 Automático nuevo", "📋 Paste Gemini"],
        horizontal=True,
        help="Manual: Control total | Automático: Genera 4 escenas | Paste Gemini: Parsea texto de Gemini existente"
    )
    st.markdown("---")
    
    # ========================================================================
    # MODO PASTE GEMINI: Parser Automático de Guiones
    # ========================================================================
    if modo == "📋 Paste Gemini":
        st.header("🧠 Parser de Guiones Gemini")
        st.info("📋 Pega un guion que ya hayas generado con Gemini y extraeré automáticamente las 4 escenas.")
        
        guion_raw = st.text_area(
            "Pega aquí el texto completo de Gemini:",
            height=300,
            placeholder="""Ejemplo:
Opción 1: El Ángulo Financiero
(0:00-0:03) ¿Sabes cuánto dinero pierdes cada semana comprando frutas en el super?
Wide-angle shot of apartment balcony with small pots...
(0:04-0:15) El 70% de la gente sin jardín gasta $50 semanales...
Close-up of hands planting seeds in containers...""",
            help="Copia y pega el texto tal cual lo generó Gemini, con timestamps o sin ellos."
        )
        
        if st.button("🔮 EXTRAER 4 ESCENAS AUTOMÁTICO", type="primary", use_container_width=True):
            if guion_raw.strip():
                with st.spinner("🔍 Analizando texto y extrayendo escenas..."):
                    escenas_parsed = parse_gemini_guion(guion_raw)
                    
                    if escenas_parsed and len(escenas_parsed) >= 4:
                        # Convertir a formato compatible con Step 2
                        scenes_formatted = []
                        for i, escena in enumerate(escenas_parsed[:4]):
                            scene_role = "hook" if i == 0 else ("cta" if i == 3 else "body")
                            scenes_formatted.append({
                                "id": i + 1,
                                "role": scene_role,
                                "narration": escena['texto'],
                                "visual_prompt": escena['prompt'],
                                "estimated_duration": 8.0
                            })
                        
                        # Guardar en session_state
                        st.session_state['script_data'] = {
                            'title': "Video desde Gemini parseado",
                            'hook_analysis': "Guion importado desde texto de Gemini",
                            'scenes': scenes_formatted
                        }
                        st.session_state['step'] = 2
                        st.success(f"✅ ¡{len(escenas_parsed)} escenas extraídas correctamente!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ No se pudieron extraer 4 escenas válidas del texto. Verifica el formato.")
            else:
                st.warning("⚠️ Pega el texto de Gemini primero.")
    
    # ========================================================================
    # MODO AUTOMÁTICO: Generador 4 Escenas
    # ========================================================================
    elif modo == "🚀 Automático nuevo":
        st.header("🎬 Generador Automático de 4 Escenas TikTok")
        st.info("🪄 Gemini creará automáticamente 4 escenas optimizadas para TikTok. Podrás editarlas después.")
        
        # 🆕 SELECTOR DE PRODUCTO
        producto_key = st.selectbox(
            "📦 Selecciona el Producto:",
            list(PRODUCTOS_DISPONIBLES.keys()),
            help="Cada producto tiene su propio template con capítulos, hooks y CTAs específicos"
        )
        
        # Obtener configuración del producto seleccionado
        producto_config = PRODUCTOS_DISPONIBLES[producto_key]
        
        # Mostrar info del producto seleccionado
        st.caption(f"**{producto_config['nombre']}** | Precio: {producto_config['precio']} | {producto_config['bonos']} bonos incluidos")
        
        # Pre-cargar datos si existen de la URL
        tema_default = st.session_state.url_data.get("dolor_principal", "Gente en depa sin jardín") if st.session_state.url_data else "Gente en depa sin jardín"
        producto_default = st.session_state.url_data.get("nombre_producto", producto_key) if st.session_state.url_data else producto_key
        
        # Inicializar session_state para ideas si no existe
        if 'ideas_auto' not in st.session_state:
            st.session_state.ideas_auto = []
        if 'tema_auto_value' not in st.session_state:
            st.session_state.tema_auto_value = tema_default
        
        # Actualizar tema_auto_value si hay nuevos datos de URL y el tema es el default
        if st.session_state.url_data:
            new_tema = st.session_state.url_data.get("dolor_principal", "Gente en depa sin jardín")
            if st.session_state.tema_auto_value != new_tema:
                st.session_state.tema_auto_value = new_tema
        
        col1, col2 = st.columns(2)
        
        with col1:
            # SIN key para que value sea respetado en cada rerun
            tema_auto = st.text_input(
                "📌 Tema del Video:",
                value=st.session_state.tema_auto_value,
                placeholder="Ej: Personas con poco espacio en casa",
                help="Describe la audiencia o situación objetivo"
            )
            
            # Botón para generar ideas
            if st.button("💡 Generar Ideas", key="ideas_btn_auto", help="Genera 5 ideas de temas virales con Gemini"):
                with st.spinner("🧠 Generando ideas..."):
                    ideas = generate_ideas_tema(producto_key)
                    st.session_state.ideas_auto = ideas
                    st.rerun()
            
            # Mostrar ideas como botones seleccionables
            if st.session_state.ideas_auto:
                st.caption("**💡 Haz clic en una idea para usarla:**")
                for i, idea in enumerate(st.session_state.ideas_auto):
                    if st.button(f"👉 {idea}", key=f"idea_auto_{i}", use_container_width=True):
                        # Limpiar las comillas si las tiene
                        idea_limpia = idea.strip('"').strip("'")
                        st.session_state.tema_auto_value = idea_limpia
                        # Limpiar las ideas después de seleccionar
                        st.session_state.ideas_auto = []
                        st.rerun()
        
        with col2:
            producto_auto = st.text_input(
                "🎯 Producto/Servicio:",
                value=producto_default,
                placeholder=f"Ej: {producto_config['nombre'][:30]}...",
                help="¿Qué estás vendiendo?"
            )
        
        # Hooks dinámicos según el producto seleccionado
        hooks_disponibles = list(producto_config['hooks'].keys())
        hook_auto = st.selectbox(
            "🎣 Tipo de Hook:",
            hooks_disponibles,
            help="El enfoque del hook para captar atención en los primeros 3 segundos"
        )
        
        
        if st.button("🪄 AUTO-GENERAR 4 ESCENAS", type="primary", use_container_width=True):
            if tema_auto and producto_auto:
                with st.spinner("🧠 Gemini está generando tus 4 escenas TikTok..."):
                    escenas_auto = generate_auto_escenas(tema_auto, producto_auto, hook_auto, producto_config)
                    
                    if escenas_auto and len(escenas_auto) == 4:
                        # Convertir escenas auto a formato compatible con Step 2
                        scenes_formatted = []
                        for i, escena in enumerate(escenas_auto):
                            scene_role = "hook" if i == 0 else ("cta" if i == 3 else "body")
                            scenes_formatted.append({
                                "id": i + 1,
                                "role": scene_role,
                                "narration": escena['texto'],
                                "visual_prompt": escena['prompt'],
                                "estimated_duration": 8.0
                            })
                        
                        # Guardar en session_state y avanzar a Step 2
                        st.session_state['script_data'] = {
                            'title': f"Video TikTok: {tema_auto}",
                            'hook_analysis': f"Hook automático tipo {hook_auto} para {tema_auto}",
                            'scenes': scenes_formatted
                        }
                        st.session_state['step'] = 2
                        st.success("✅ ¡4 escenas generadas! Ahora puedes editarlas.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error: Se generaron {len(escenas_auto)} escenas en lugar de 4. Intenta de nuevo.")
            else:
                st.warning("⚠️ Completa todos los campos para generar las escenas.")
    
    # ========================================================================
    # MODO MANUAL: Sistema actual (sin cambios)
    # ========================================================================
    elif modo == "📝 Manual (actual)":
        st.info("💡 Modo manual activado: Usa el sistema de plantillas como siempre 👇")
        
        # 🆕 PLANTILLAS PRE-CONFIGURADAS
        st.markdown("### 🎯 ¿No sabes qué crear? Usa una plantilla:")
        
        templates = {
            "": {"topic": "", "product": ""},  # Opción vacía
            "🎯 Marketing Digital": {
                "topic": "Mis anuncios de Facebook no están convirtiendo",
                "product": "Consultoría de Meta Ads"
            },
            "💪 Fitness & Salud": {
                "topic": "No logro bajar de peso aunque hago ejercicio",
                "product": "Programa de Entrenamiento Personalizado"
            },
            "💰 Finanzas Personales": {
                "topic": "No sé cómo invertir mi dinero de forma segura",
                "product": "Curso de Inversiones para Principiantes"
            },
            "🍔 Comida & Recetas": {
                "topic": "Mis recetas caseras no tienen el sabor profesional de restaurante",
                "product": "Curso de Cocina Profesional Online"
            },
            "🎓 Educación Online": {
                "topic": "Mi hijo tiene problemas para entender matemáticas",
                "product": "Tutorías Personalizadas 1 a 1"
            },
            "🏠 Bienes Raíces": {
                "topic": "Quiero vender mi casa pero no encuentro compradores",
                "product": "Servicio de Marketing Inmobiliario"
            }
        }
        
        template_choice = st.selectbox(
            "Selecciona una plantilla (o deja vacío para crear desde cero):",
            list(templates.keys()),
            help="Esto llenará automáticamente los campos abajo. Puedes editarlos después."
        )
        
        if template_choice != "":
            st.success(f"✅ Plantilla '{template_choice}' cargada. Personaliza los campos abajo.")
        
        st.markdown("---")
        
        # Inicializar session_state para ideas en modo manual
        if 'ideas_manual' not in st.session_state:
            st.session_state.ideas_manual = []
        if 'topic_manual_value' not in st.session_state:
            st.session_state.topic_manual_value = ""
        
        # Inputs con valores pre-cargados de plantilla o de ideas seleccionadas
        col1, col2 = st.columns(2)
        
        with col1:
            # Pre-cargar datos si existen de la URL (Pippit Logic)
            if st.session_state.url_data:
                tema_url_new = st.session_state.url_data.get("dolor_principal", "")
                if st.session_state.topic_manual_value != tema_url_new and tema_url_new:
                    st.session_state.topic_manual_value = tema_url_new

            # Usar el valor guardado primero, luego la plantilla como fallback
            if st.session_state.topic_manual_value:
                initial_topic = st.session_state.topic_manual_value
            elif template_choice:
                initial_topic = templates[template_choice]["topic"]
            else:
                initial_topic = ""
            
            # Usar session_state si hay un valor guardado de las ideas
            display_topic = st.session_state.topic_manual_value if st.session_state.topic_manual_value else initial_topic
            
            # SIN key para que value sea respetado en cada rerun
            topic = st.text_input(
                "💡 Tema / Dolor del Cliente",
                value=display_topic,
                placeholder="Ej: Mis anuncios de Facebook no convierten..."
            )
            
            # Botón para generar ideas
            if st.button("💡 Generar Ideas", key="ideas_btn_manual", help="Genera 5 ideas de temas virales con Gemini"):
                with st.spinner("🧠 Generando ideas..."):
                    ideas = generate_ideas_tema("general")
                    st.session_state.ideas_manual = ideas
                    st.rerun()
            
            # Mostrar ideas como botones seleccionables
            if st.session_state.ideas_manual:
                st.caption("**💡 Haz clic en una idea para usarla:**")
                for i, idea in enumerate(st.session_state.ideas_manual):
                    if st.button(f"👉 {idea}", key=f"idea_manual_{i}", use_container_width=True):
                        # Limpiar las comillas si las tiene
                        idea_limpia = idea.strip('"').strip("'")
                        st.session_state.topic_manual_value = idea_limpia
                        # Limpiar las ideas después de seleccionar
                        st.session_state.ideas_manual = []
                        st.rerun()
        
        with col2:
            default_product = producto_url if producto_url else (templates[template_choice]["product"] if template_choice else "")
            product = st.text_input(
                "🎯 Producto/Servicio a Vender",
                value=default_product,
                placeholder="Ej: Consultoría de Meta Ads"
            )

        # Selector de número de escenas
        num_scenes = st.slider(
            "📊 Número de Escenas",
            min_value=3,
            max_value=5,
            value=4,
            help="Videos más cortos (3 escenas) = Mayor retención. Videos más largos (5 escenas) = Más información."
        )
        st.caption(f"⏱️ Duración estimada: {num_scenes * 8} - {num_scenes * 10} segundos")

        if st.button("⚡ GENERAR GUION MAESTRO (Gemini 2.0 Flash)"):
            if topic and product:
                with st.spinner("🧠 Gemini aplicando lógica de 'Ads Expansive'..."):
                    try:
                        writer = ScriptWriterAgent() 
                        script = writer.generate_script(topic, product, num_scenes=num_scenes)
                        
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
                    help="El sistema inyectará automáticamente el estilo 'Cinematic Style' de Quantum Clic"
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
            # Agents are now initialized in session_state
            if not st.session_state.audio_agent.is_ready():
                st.error("❌ Edge TTS no disponible. Ejecuta: pip install edge-tts")
            elif not st.session_state.visual_agent.is_ready():
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
        st.header("🎨 Fase 3: Producción de Assets")
        st.info(f"🚀 Modo Activo: {'🎥 VIDEO (Veo)' if st.session_state.use_video else '🖼️ IMAGEN (Flux)'}")

    if st.button("🚀 GENERAR / ACTUALIZAR TODOS LOS ASSETS"):
        # Preparar contenedores
        asset_progress = st.progress(0)
        status_text = st.empty()
        
        # Procesar escenas
        scenes = st.session_state['script_data'].get('scenes', [])
        total_scenes = len(scenes)
        total_steps = total_scenes * 2
        current_step = 0
        
        generated_assets = []
        errors = []
        
        # 🎬 PROCESAR CADA ESCENA
        for i, scene in enumerate(scenes):
            scene_num = i + 1
            status_text.markdown(f"### 🎬 Procesando Escena {scene_num}/{total_scenes}...")
            
            # 1️⃣ GENERAR AUDIO
            status_text.text(f"🎙️ Generando audio para escena {scene_num}...")
            audio_file = f"scene_{scene_num}.mp3"
            audio_path = st.session_state.audio_agent.generate_narration(scene['narration'], audio_file)
            
            if audio_path:
                scene['audio_path'] = audio_path
            else:
                errors.append(f"Audio escena {scene_num}")
            
            current_step += 1
            asset_progress.progress(current_step / total_steps)
            
            # 2️⃣ GENERAR VISUAL (Imagen o Video)
            if st.session_state.use_video:
                status_text.text(f"🎥 Generando video Veo para escena {scene_num} (espera ~60s)...")
                video_path = st.session_state.veo_agent.generate_video_clip(scene['visual_prompt'])
                if video_path:
                    scene['image_path'] = video_path
                else:
                    errors.append(f"Video Veo escena {scene_num}")
            else:
                status_text.text(f"🖼️ Mejorando prompt y generando imagen para escena {scene_num}...")
                
                # 🆕 MEJORAR PROMPT VISUAL para coherencia con la narración
                original_prompt = scene['visual_prompt']
                narration = scene.get('narration', '')
                enhanced_prompt = st.session_state.visual_agent.enhance_visual_prompt(original_prompt, narration)
                
                # Guardar el prompt mejorado para debug
                scene['enhanced_prompt'] = enhanced_prompt
                
                img_file = f"scene_{scene_num}.png"
                image_path = st.session_state.visual_agent.generate_image(enhanced_prompt, img_file)
                if image_path:
                    scene['image_path'] = image_path
                else:
                    errors.append(f"Imagen Flux escena {scene_num}")
            
            current_step += 1
            asset_progress.progress(current_step / total_steps)
            generated_assets.append(scene)
            
        # 🎉 RESULTADO FINAL
        asset_progress.progress(1.0)
        status_text.markdown("### ✅ Producción Completada")
        
        if not errors:
            st.session_state['script_data']['scenes'] = generated_assets
            st.balloons()
            st.success("🎉 ¡TODOS LOS ASSETS GENERADOS CORRECTAMENTE!")
            
            # IR DIRECTAMENTE A REVISIÓN (step 3.5) para evitar loop
            st.session_state['step'] = 3.5
            st.info("🔜 Redirigiendo a la revisión de assets...")
            st.rerun()
        else:
            st.error(f"❌ Hubo errores en: {', '.join(errors)}")
            st.session_state['script_data']['scenes'] = generated_assets
            
            for err in errors:
                st.warning(f"• {err}")
            
            if st.button("⬅️ Volver a Editar Escenas"):
                st.session_state['step'] = 2
                st.rerun()

# ========================================================================
# PASO 3.5: REVISIÓN DE ASSETS (Human-in-the-Loop Visual)
# ========================================================================
elif st.session_state['step'] == 3.5:
    st.title("🎨 Revisión de Material Visual")
    st.markdown("Revisa las imágenes y audios generados. Puedes regenerar individualmente antes del ensamblaje final.")
    
    scenes = st.session_state['script_data'].get('scenes', [])
    
    if not scenes:
        st.error("❌ No hay escenas para revisar")
        if st.button("← Volver"):
            st.session_state['step'] = 2
            st.rerun()
    else:
        visual_agent = VisualGeneratorAgent()
        audio_agent = AudioGeneratorAgent()
        
        st.markdown("---")
        
        for idx, scene in enumerate(scenes):
            scene_num = idx + 1
            
            with st.expander(f"🎬 Escena {scene_num} - {'✅ Completa' if scene.get('image_path') and scene.get('audio_path') else '⚠️ Incompleta'}", expanded=True):
                
                col_preview, col_controls = st.columns([2, 1])
                
                # PREVIEW DE ASSETS
                with col_preview:
                    # Mostrar imagen actual
                    if scene.get('image_path') and os.path.exists(scene['image_path']):
                        st.image(scene['image_path'], use_container_width=True)
                    else:
                        st.warning("⚠️ Imagen no disponible")
                    
                    # Mostrar audio actual
                    if scene.get('audio_path') and os.path.exists(scene['audio_path']):
                        st.audio(scene['audio_path'])
                    else:
                        st.warning("⚠️ Audio no disponible")
                    
                    # Mostrar narración
                    st.caption(f"**📝 Narración:** {scene.get('narration', 'N/A')}")
                
                # CONTROLES DE REGENERACIÓN
                with col_controls:
                    st.markdown("**🔄 Regenerar Assets:**")
                    
                    # Input para nuevo prompt visual (opcional)
                    new_prompt = st.text_area(
                        f"Nuevo Prompt Visual (opcional)",
                        value=scene.get('visual_prompt', ''),
                        height=100,
                        key=f"prompt_{scene_num}",
                        help="Edita el prompt en inglés para cambiar la imagen. Deja vacío para usar el original."
                    )
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    # Botón regenerar imagen
                    if col_btn1.button(f"🎨 Regenerar Imagen", key=f"regen_img_{scene_num}", use_container_width=True):
                        with st.spinner(f"🎨 Regenerando imagen {scene_num}..."):
                            # Eliminar imagen vieja
                            if scene.get('image_path') and os.path.exists(scene['image_path']):
                                os.remove(scene['image_path'])
                            
                            # Usar nuevo prompt o el original
                            prompt_to_use = new_prompt if new_prompt.strip() else scene.get('visual_prompt', '')
                            scene['visual_prompt'] = prompt_to_use  # Actualizar en sesión
                            
                            # Generar nueva imagen
                            img_file = f"scene_{scene_num}.png"
                            img_path = visual_agent.generate_image(prompt_to_use, img_file)
                            
                            if img_path:
                                scene['image_path'] = img_path
                                st.success("✅ Imagen regenerada")
                                st.rerun()
                            else:
                                st.error("❌ Error al regenerar imagen")
                    
                    # Botón regenerar audio
                    if col_btn2.button(f"🔊 Regenerar Audio", key=f"regen_audio_{scene_num}", use_container_width=True):
                        with st.spinner(f"🔊 Regenerando audio {scene_num}..."):
                            # Eliminar audio viejo
                            if scene.get('audio_path') and os.path.exists(scene['audio_path']):
                                os.remove(scene['audio_path'])
                            
                            # Generar nuevo audio
                            audio_file = f"scene_{scene_num}.mp3"
                            audio_path = audio_agent.generate_narration(scene['narration'], audio_file)
                            
                            if audio_path:
                                scene['audio_path'] = audio_path
                                st.success("✅ Audio regenerado")
                                st.rerun()
                            else:
                                st.error("❌ Error al regenerar audio")
                
                st.markdown("---")
        
        # BOTONES DE NAVEGACIÓN
        st.markdown("---")
        col_back, col_next = st.columns(2)
        
        with col_back:
            if st.button("⬅️ Volver a Editar Guion", use_container_width=True):
                st.session_state['step'] = 2
                st.rerun()
        
        with col_next:
            # Validar que todos los assets estén listos
            all_ready = all(
                scene.get('image_path') and scene.get('audio_path') 
                for scene in scenes
            )
            
            if all_ready:
                if st.button("🎬 Continuar al Ensamblaje Final", use_container_width=True, type="primary"):
                    st.session_state['step'] = 4
                    st.rerun()
            else:
                st.error("⚠️ Faltan assets por generar. Completa todas las escenas antes de continuar.")

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