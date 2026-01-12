# CONTEXT.md - Video Factory AI

> ⚠️ **INSTRUCCIONES PARA IA:** Lee este archivo COMPLETO antes de ejecutar cualquier tarea. Este es tu "cerebro" del proyecto.

---

## 🎯 RESUMEN EJECUTIVO

| Campo | Valor |
|-------|-------|
| **Proyecto** | Video Factory AI (Quantum Clic) |
| **Versión** | 3.2 |
| **Estado** | ✅ OPERACIONAL (Flux + Art Direction 2.0) |
| **Última actualización** | 2026-01-11 |
| **Último commit** | d8c0bd9 |

**Descripción:** Aplicación Streamlit que genera videos virales (TikTok/Reels/Shorts) usando 5 agentes de IA especializados y la metodología **Quantum Clic**.

---

## 📋 PROTOCOLO OBLIGATORIO (CRÍTICO)

> **⚠️ REGLA DE ORO PARA CUALQUIER IA:**

Al finalizar **CUALQUIER** tarea de código, SIN EXCEPCIÓN:
1. ✅ Actualizar este archivo (`CONTEXT.md`) con el nuevo estado del sistema
2. ✅ Ejecutar: `git add -A` → `git commit -m "descripción"` → `git push`
3. ✅ **NO esperar** a que el usuario lo pida - hacerlo INMEDIATAMENTE
4. ✅ Actualizar la versión si hubo cambios significativos

---

## 🛠️ STACK TECNOLÓGICO

| Componente | Tecnología | Estado | Notas Críticas |
|------------|------------|--------|----------------|
| **Cerebro (Scripts)** | Gemini 2.0 Flash | ✅ OK | SDK: `google-genai` v1.57+ |
| **Video AI** | Google Veo (Vertex AI) | ⚠️ VER NOTA | Modelo: `veo-2`, requiere acceso aprobado |
| **Imágenes** | Together AI Flux-Schnell | ✅ OK | Estilo: Industrial Realism |
| **Audio/Voz** | gTTS (Google TTS) | ✅ OK | Voz: Español Latino neutro |
| **Ensamblaje** | MoviePy | ✅ OK | ⚠️ **VERSIÓN 1.0.3 OBLIGATORIA** (NO 2.x) |
| **PDF Bonos** | fpdf2 | ✅ OK | Mockups 3D para Hotmart |

### ⚠️ NOTA SOBRE GOOGLE VEO:
El modelo `veo-2` requiere acceso especial aprobado por Google. Si aparece error 404 "model not found", significa que el proyecto GCP aún no tiene acceso. Se debe solicitar en: https://cloud.google.com/vertex-ai/docs/generative-ai/video/overview


---

## 🔑 API KEYS REQUERIDAS (en `.streamlit/secrets.toml`)

```toml
GOOGLE_API_KEY = "..."           # Gemini 2.0 Flash
TOGETHER_API_KEY = "..."         # Flux-Schnell (imágenes)
DEEPGRAM_API_KEY = "..."         # Backup TTS
ELEVENLABS_API_KEY = "..."       # Backup TTS premium

[GCP_SERVICE_ACCOUNT]            # Google Veo (Vertex AI)
type = "service_account"
project_id = "gen-lang-client-0706301797"
# ... resto del JSON de la cuenta de servicio
```

---

## 📁 ARQUITECTURA DE ARCHIVOS

```
appvideos/
├── app.py                        # 🎛️ ORQUESTADOR PRINCIPAL (4 fases)
│
├── agents/                       # 🤖 AGENTES DE IA
│   ├── scriptwriter.py           # Gemini → Genera guiones (Ads Expansive)
│   ├── audio_generator.py        # gTTS → Genera voz
│   ├── visual_generator.py       # Flux → Genera imágenes
│   ├── veo_generator.py          # Veo → Genera clips de video ✅
│   └── video_editor.py           # MoviePy → Ensambla video final
│
├── .streamlit/
│   └── secrets.toml              # 🔐 API Keys (git ignored)
│
├── .prompts/                     # 📝 Prompts de sistema detallados
│   ├── ANTIGRAVITY_SYSTEM_PROMPT.md
│   ├── GEMINI_GEM_SYSTEM_PROMPT.md
│   └── PERPLEXITY_SYSTEM_PROMPT.md
│
├── assets/
│   ├── final_output/             # Videos finales listos
│   ├── generated_videos/         # Clips de Veo
│   └── bonos_pdf_final/          # PDFs para Hotmart
│
└── config/
    └── settings.py               # Configuraciones globales
```

---

## 🎬 FLUJO DE LA APLICACIÓN (4 FASES)

```
FASE 1: Estrategia
│   └── Usuario define: Tema + Producto + Hook
│
FASE 2: Aprobación (Human-in-the-Loop)
│   └── Edición manual de escenas y prompts visuales
│
FASE 3: Producción de Assets
│   ├── Audio: gTTS genera narraciones
│   └── Visual: Flux (imágenes) O Veo (videos)
│
FASE 4: Ensamblaje Final
    └── MoviePy: Combina todo → Video MP4 descargable
```

---

## 🎯 METODOLOGÍA QUANTUM CLIC

### 1. ADS EXPANSIVE (Hook en 3 segundos)
```
PASO 1 - DOLOR:       "¿Tus plantas se mueren sin razón?"
PASO 2 - CONSECUENCIA: "El 90% falla por el drenaje..."
PASO 3 - INTRIGA:      "En mi guía, capítulo 3, lo explico..."
```

### 2. MOCKUPS (Industrial Realism)
Vocabulario OBLIGATORIO para prompts visuales:
```
✅ USAR: Rembrandt lighting, golden hour volumetric god rays, global illumination, shallow depth of field, RAW photo quality.
❌ EVITAR: cartoon, illustration, smooth AI skin, plastic textures, text overlays.
```

### 3. TSL (CTA Orgánica)
```
✅ BIEN: "Sígueme para más", "Link en bio"
❌ MAL: "SUSCRÍBETE AHORA", "DALE LIKE"
```

### 4. HUMANIZACIÓN DE GUIONES
```
✅ USAR: PAS Framework (Problem-Agitation-Solution), "En mi guía...", "Te regalo 4 bonos de mi parte..."
❌ EVITAR: "El capítulo 3 revela...", "descubre el secreto...", lenguaje corporativo o robótico.
```

---

## �️ REGLAS CRÍTICAS (NO ROMPER)

### ❌ NUNCA:
- Actualizar MoviePy a versión 2.x (incompatible con decorator)
- Cambiar de `google-genai` a `google-generativeai` (ya migrado)
- Modificar estructura de carpetas `assets/`
- Romper la arquitectura de agentes independientes
- Subir `secrets.toml` a Git

### ✅ SIEMPRE:
- Usar rutas con `os.path.join()` (compatibilidad Windows/Linux)
- Validar `is_ready()` antes de usar cualquier agente
- Incluir traceback completo en errores
- Actualizar `CONTEXT.md` después de cambios importantes
- Hacer `git push` después de cada tarea completada

---

## � PATRONES COMUNES DE DEBUGGING

| Error | Causa Probable | Solución |
|-------|----------------|----------|
| "Agent no está listo" | Falta API key | Verificar `secrets.toml` |
| MoviePy timing error | Clip excede duración | `min(end, audio.duration - 0.1)` |
| "Module not found" | Librería no instalada | `pip install -r requirements.txt` |
| Veo credentials error | Service Account mal configurado | Verificar `[GCP_SERVICE_ACCOUNT]` en secrets |
| Flux no genera imagen | Créditos agotados | Verificar cuenta Together AI |

---

## 📦 SISTEMA MULTI-PRODUCTO

La app soporta múltiples productos con templates únicos:

| Producto | Precio | Bonos | Hooks |
|----------|--------|-------|-------|
| 🍊 Frutíferas en Macetas | $7 | 4 | Drenaje, Dinero, Espacio, Tiempo |
| 💼 Marketing Digital Pro | $27 | 5 | CTR, ROI, Audiencia, Escalamiento |
| 💪 Fitness en Casa | $17 | 3 | Tiempo, Sin Gym, Grasa, Sostenible |

---

## 📊 HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| **3.2** | 2026-01-11 | ✅ Art Direction 2.0 + PAS Framework (Pippit Quality) |
| **3.1** | 2026-01-11 | ✅ Generador de Ideas + Fix Infinite Loop |
| **2.9** | 2026-01-11 | ✅ Google Veo COMPLETAMENTE CONFIGURADO |

---

## 🔗 REFERENCIAS RÁPIDAS

- **Prompts detallados:** `.prompts/ANTIGRAVITY_SYSTEM_PROMPT.md`
- **Metodología completa:** `.prompts/GEMINI_GEM_SYSTEM_PROMPT.md`
- **Proyecto GCP:** `gen-lang-client-0706301797` (luz digital)
- **Archivo de secretos:** `.streamlit/secrets.toml`

---

**Fin del documento. Este archivo es la fuente de verdad para cualquier IA que trabaje en el proyecto.**
