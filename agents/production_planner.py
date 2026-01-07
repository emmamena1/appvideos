import os
import json
from google import genai
from google.genai import types
from config import settings

# --- 💎 IDENTIDAD VISUAL CINEMATOGRÁFICA (LA MINA DE ORO) ---

VISUAL_IDENTITY = """
STYLE: Ultra-realistic cinematic industrial photography. Documentary-fashion hybrid aesthetic.
PRIORITY: Physically plausible lighting, real-world optics, material accuracy.
TEXTURES: Visible skin pores, fabric wrinkles, grease, dust, worn metal, micro-imperfections.
LIGHTING: Inverse-square falloff, soft penumbra shadows, bounced fill. NO artificial glow.
CAMERA: Medium-to-large sensor look, controlled depth of field, neutral highlights.
MOOD: Serious, credible, functional, high-end engineering brand campaign.
"""

MASTER_PROMPT_FORMULA = """
STRICT PROMPT STRUCTURE (Order matters):
1. [Subject]: Physical description (age, wear, clothing, anatomy).
2. [Action]: Frozen photographic moment.
3. [Context]: Spatial logic, scale, background elements.
4. [Lighting]: Direction, softness, color temp (e.g., 5200K), interaction.
5. [Camera]: Lens (e.g., 50mm, 85mm), aperture (f/2.8), sensor feel.
6. [Texture]: Specific material details (rust, oil, sweat, grime).
"""

GOLD_KEYWORDS = [
    "Ultra-realistic photography", "Physically based lighting", "Natural skin pores",
    "Surface imperfections", "Subtle asymmetry", "Cinematic color grading",
    "Depth of field", "Optical realism", "High dynamic range", "Filmic contrast",
    "Soft shadow falloff", "Material accuracy", "Sensor noise grain",
    "Micro-detail fidelity", "Real-world scale", "Documentary realism"
]

NEGATIVE_PROMPTS = [
    "cartoon", "illustration", "anime", "CGI", "3D render", "synthetic look",
    "plastic skin", "overly smooth skin", "beauty filter", "unreal lighting",
    "exaggerated proportions", "watermark", "text overlay", "distorted anatomy"
]

# Estructuras de Copywriting probadas para retención
VIRAL_HOOKS_FRAMEWORK = """
COPYWRITING RULES:
1. ONE IDEA: Focus on a single core concept per video.
2. FRICTION BEFORE VALUE: Break expectations immediately.
3. TONE: Conversational, not corporate. Short sentences. Visual rhythm.
4. NO "HELLO": Never start with "Welcome" or "Hi friends".
5. STRUCTURE:
   - Hook (0-3s): Disruptive. Use patterns like: "Nadie te dijo esto sobre...", "El error silencioso que mata...", "No es falta de X, es esto."
   - Reframe: Change the viewer's mental perspective.
   - Micro-proof/Insight: Deliver the value quickly.
   - CTA: Soft consequence, not a command (e.g., "Si quieres X, sígueme" instead of "SUsCribetE").
"""

class ProductionPlannerAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = "gemini-2.0-flash"  # Modelo más rápido y capaz

    def create_plan(self, project_id, topic, language="Español"):
        """
        Genera un guion detallado y prompts visuales usando el Framework Industrial.
        """
        
        # Configuración de Idioma
        if language == "Español":
            lang_instruction = "OUTPUT LANGUAGE: SPANISH (Español Latino Neutro). Natural, colloquial, authentic."
            hook_examples = "'Nadie te dijo esto...', 'El error silencioso...', 'Esto suena mal, pero es verdad...'"
        else:
            lang_instruction = "OUTPUT LANGUAGE: ENGLISH. Native, conversational, punchy."
            hook_examples = "'No one told you this about...', 'The silent error killing your...', 'This sounds wrong, but it's true...'"

        # El MEGA PROMPT CON IDENTIDAD VISUAL PROFESIONAL
        prompt = f"""
        ROLE: You are an Elite Viral Content Producer and Cinematic Art Director specializing in FLUX.1 Pro.
        TASK: Create a script and ultra-realistic visual prompts for a Short/TikTok about: '{topic}'.
        
        {lang_instruction}
        
        === SECTION 1: COPYWRITING INTELLIGENCE (Apply strictly) ===
        {VIRAL_HOOKS_FRAMEWORK}
        USE THESE HOOK PATTERNS: {hook_examples}
        
        === SECTION 2: VISUAL IDENTITY (STRICT ENFORCEMENT) ===
        {VISUAL_IDENTITY}
        
        === SECTION 3: PROMPT ENGINEERING RULES ===
        When creating 'visual_description', YOU MUST FOLLOW THIS FORMULA:
        {MASTER_PROMPT_FORMULA}
        
        BOOST QUALITY WITH THESE GOLD KEYWORDS:
        {", ".join(GOLD_KEYWORDS)}
        
        AVOID THESE (NEGATIVE PROMPTS):
        {", ".join(NEGATIVE_PROMPTS)}
        
        CRITICAL RULES FOR visual_description:
        - Write in ENGLISH (even if narration is Spanish).
        - Start directly with the subject. NO "Image of..." or "A photo of...".
        - Use DENSE, TECHNICAL language. Ex: "Ultra-realistic cinematic photograph of weathered industrial worker, 45 years old, natural skin pores visible, grease-stained blue coveralls, soft window light from left at 5200K, medium format look, 85mm f/2.8, shallow depth of field, filmic grain..."
        - ALWAYS include: Subject + Action + Lighting specs + Camera specs + Texture details
        - Match visual mood to the script segment.
        
        === OUTPUT FORMAT (Strict JSON) ===
        Return a LIST of objects. Each object = one scene.
        [
            {{
                "scene_number": 1,
                "visual_description": "YOUR ULTRA-REALISTIC FLUX PROMPT HERE (Dense, technical, English)",
                "narration": "The spoken text (in {language}). Match the copywriting tone.",
                "estimated_duration": 4
            }},
             ... (4-6 scenes total)
        ]
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Limpieza del JSON (a veces Gemini pone ```json ... ```)
            text_response = response.text.strip()
            if text_response.startswith("```"):
                text_response = text_response.replace("```json", "").replace("```", "")
            
            script_data = json.loads(text_response)
            return script_data

        except Exception as e:
            print(f"Error planning video: {e}")
            return None
