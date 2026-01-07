# CONTEXT.md - Industrial Video Factory v2

**INSTRUCCIONES PARA ANTIGRAVITY:** Lee estos archivos antes de responder cualquier pregunta sobre este proyecto.

---

## 📚 ARCHIVOS DE CONTEXTO OBLIGATORIOS:

### 1. System Prompt Principal
**Archivo:** `.prompts/ANTIGRAVITY_SYSTEM_PROMPT.md`
- Contiene: Reglas de desarrollo, metodología, arquitectura
- **LEER PRIMERO:** Este archivo define cómo debes trabajar en el proyecto

### 2. Metodología del Proyecto
**Archivo:** `IMPLEMENTACION_QUANTUM_CLIC.md`
- Contiene: Alineación con Quantum Clic, arquitectura final, configuración
- **LEER SEGUNDO:** Este archivo explica la estrategia del negocio

### 3. Historial de Correcciones (Opcional)
**Archivo:** `CORRECCIONES_GEMINI.md`
- Contiene: Errores detectados y corregidos anteriormente
- **LEER SI HAY BUGS:** Para entender el historial de problemas

---

## 🎯 PROYECTO: Industrial Video Factory v2

### Stack Tecnológico:
- **Frontend:** Streamlit
- **Cerebro:** Gemini 2.0 Flash (google-genai SDK v1.56.0)
- **Voz:** Edge TTS Hardened (Gratis, Anti-403, es-MX-DaliaNeural)
- **Visual:** Together AI Flux-Schnell (1024x1792, 9:16)
- **Video:** MoviePy 1.0.3 (NUNCA 2.x) + Pillow 9.5.0 (Strict)

### Metodología: Quantum Clic
1. **Ads Expansive:** Hook de 3 pasos (Dolor → Consecuencia → Intriga)
2. **Mockups:** Estilo "Industrial Realism" (50mm f/2.8, textura visible)
3. **TSL:** CTA orgánica (nunca agresiva)

### Arquitectura de Agentes:
```
agents/
├── scriptwriter.py        (Gemini - Ads Expansive)
├── audio_generator.py     (Edge TTS Hardened - Reintentos)
├── visual_generator.py    (Flux - Industrial Realism)
└── video_editor.py        (MoviePy - Ensamblaje)

app.py                     (Orquestador - 4 fases)
```

---

## 🔑 API KEYS REQUERIDAS:

En `.streamlit/secrets.toml`:
- `GOOGLE_API_KEY` - Gemini 2.0 Flash
- `TOGETHER_API_KEY` - Imágenes Flux

---

## ⚠️ REGLAS CRÍTICAS:

### ❌ NUNCA:
- Actualizar MoviePy a 2.x
- Cambiar arquitectura de agentes sin preguntar
- Modificar estructura de carpetas `assets/`
- Romper validaciones `is_ready()`

### ✅ SIEMPRE:
- Usar rutas absolutas: `os.path.join()`
- Validar agentes antes de producir
- Incluir traceback completo en errores
- Alinear decisiones con Quantum Clic
- Mantener cache inteligente (ahorro de créditos)

---

## 🚀 FLUJO DE PRODUCCIÓN:

```
Fase 1: Input (Tema + Producto)
   ↓
Fase 2: Gemini genera Guion (Ads Expansive)
   ↓
Fase 3: Human-in-the-Loop (Aprobación + TSL)
   ↓
Fase 4: Producción (Audio + Visual en paralelo)
   ↓ 
Fase 5: Ensamblaje (MoviePy 1.0.3) ✅ IMPLEMENTADO
   ├── Zoom Ken Burns (retención visual)
   ├── Subtítulos Hormozi (amarillo + borde negro)
   ├── Audio Ducking (música 15% + narración 100%)
   └── Exportación MP4 (9:16, 1080x1920, 24fps)
```

---

## 📁 ESTRUCTURA DEL PROYECTO:

```
appvideos/
├── .prompts/
│   ├── ANTIGRAVITY_SYSTEM_PROMPT.md  (tus instrucciones)
│   └── GEMINI_GEM_SYSTEM_PROMPT.md   (para Gem)
├── agents/
│   ├── scriptwriter.py               (Hook Ads Expansive)
│   ├── audio_generator.py            (Edge TTS Gratis)
│   ├── visual_generator.py           (Flux Industrial)
│   └── video_editor.py               (MoviePy - Ken Burns + Hormozi)
├── assets/
│   ├── audio/                        (archivos .mp3)
│   ├── images/                       (archivos .png)
│   ├── final_output/                 (videos .mp4)
│   └── background_music.mp3          (música opcional)
├── .streamlit/
│   └── secrets.toml                  (API keys - gitignored)
├── app.py                            (UI principal - 4 fases completas)
├── requirements.txt                  (dependencias BLOQUEADAS)
├── IMPLEMENTACION_QUANTUM_CLIC.md    (metodología)
├── CORRECCIONES_GEMINI.md            (historial)
└── CONTEXT.md                        (este archivo)
```

---

## 💡 USO DE ESTE ARCHIVO:

### Cuando inicies una nueva conversación conmigo:

**Opción 1 (Rápida):**
```
"Lee CONTEXT.md y ayúdame con [tu pregunta]"
```

**Opción 2 (Completa):**
```
"Carga el contexto completo del proyecto y [tu pregunta]"
```

Yo automáticamente leeré:
1. `.prompts/ANTIGRAVITY_SYSTEM_PROMPT.md`
2. `IMPLEMENTACION_QUANTUM_CLIC.md`
3. Este archivo (CONTEXT.md)

Y estaré listo para ayudarte con contexto completo de:
- Metodología Quantum Clic
- Arquitectura del proyecto
- Reglas de desarrollo
- Stack tecnológico

---

## 🐛 DEBUG RÁPIDO:

### Error común: "Agent no está listo"
**Fix:** Verifica API keys en `secrets.toml`

### Error común: Edge TTS 403 / Handshake
**Fix:** Sistema de reintentos automáticos ya implementado (Hardened).

### Error común: MoviePy timing
**Fix:** Clamp: `min(end, audio.duration - 0.1)`

### Error común: Flux no genera
**Fix:** Verifica créditos en Together AI + formato .png

### Error común: Pillow ANTIALIAS
**Fix:** Downgrade obligatorio: `pip install Pillow==9.5.0`

### Error común: Module not found
**Fix:** `python -m pip install [package]`

---

## ✅ ESTADO ACTUAL:

- ✅ Gemini 2.0 Flash migrado y funcionando
- ✅ Edge TTS Hardened configurado (Audio TTS Gratis + Anti-403)
- ✅ Together AI Flux configurado (imágenes industriales)
- ✅ App con 4 fases implementadas
- ✅ **Fase 4 (Ensamblaje) COMPLETA:**
  - VideoEditorAgent con MoviePy 1.0.3
  - Zoom Ken Burns para retención
  - Subtítulos Hormozi (amarillo + borde)
  - Audio ducking profesional
  - Exportación MP4 vertical 9:16
- ✅ Metodología Quantum Clic al 100%
- ✅ **SISTEMA COMPLETO Y OPERACIONAL**

---

## 📞 CONTACTO RÁPIDO:

**Cuando necesites ayuda:**
1. Menciona "Lee CONTEXT.md"
2. Describe el problema
3. Incluye logs/errores si hay

**Estaré completamente contextualizado y listo para ayudar.** 🚀

---

**Última actualización:** 2026-01-07  
**Versión:** 2.0 (Fase 4 Completa)  
**Proyecto:** Industrial Video Factory v2 (Quantum Clic)
**Estado:** ✅ SISTEMA COMPLETO - Listo para Producción
