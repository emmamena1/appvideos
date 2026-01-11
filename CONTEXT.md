# CONTEXT.md - Video Factory AI

**INSTRUCCIONES PARA ANTIGRAVITY:**
1. Lee estos archivos antes de responder.
2. ⚠️ **PROTOCOLO OBLIGATORIO:** Al finalizar CUALQUIER tarea de código, DEBES actualizar este archivo (`CONTEXT.md`) con el nuevo estado del sistema y realizar un `git push` de todos los cambios inmediatamente. NO ESPERES a que el usuario lo pida.

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

## 🎯 PROYECTO: Video Factory AI

### Stack Tecnológico:
- **Frontend:** Streamlit
- **Cerebro:** Gemini 2.0 Flash (google-genai SDK v1.57.0)
- **Voz:** Edge TTS Hardened (Gratis, Anti-403, es-MX-DaliaNeural)
- **Visual:** Together AI Flux-Schnell (1024x1792, 9:16)
- **Video:** MoviePy 1.0.3 + Pillow (Latest w/ ANTIALIAS Patch)

### Metodología: Quantum Clic
1. **Ads Expansive:** Hook de 3 pasos (Dolor → Consecuencia → Intriga)
2. **Mockups:** Estilo "Cinematic Pro" (Adaptable al contexto)
3. **TSL:** CTA orgánica (nunca agresiva)

### Arquitectura de Agentes:
```
agents/
├── scriptwriter.py        (Gemini - Ads Expansive)
├── audio_generator.py     (Edge TTS Hardened - Reintentos)
├── visual_generator.py    (Flux - Adaptable Style)
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
- Cache Deshabilitado: Garantizar contenido fresco (imágenes y audio únicos cada vez)

---

## 🚀 FLUJO DE PRODUCCIÓN:

```
Fase 1: Input (Plantillas Pre-configuradas o Manual)
   ↓
Fase 2: Gemini genera Guion (Ads Expansive)
   ↓
Fase 3: Human-in-the-Loop (Aprobación + TSL)
   ↓
Fase 3.5: Asset Review (Regeneración Selectiva) ✅ NUEVO
   ↓
Fase 4: Producción Final (Ensamblaje MoviePy)
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
│   ├── visual_generator.py           (Flux - Ultra HD)
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
**Fix:** Código parcheado (`PIL.Image.ANTIALIAS = LANCZOS`) en `app.py`.

### Error común: Module not found
**Fix:** `python -m pip install [package]`

---

## ✅ ESTADO ACTUAL:

- ✅ Gemini 2.0 Flash migrado y funcionando
- ✅ **gTTS (Google Text-to-Speech)** configurado (Audio TTS Gratis + Sin bloqueos)
  - Migrado desde Edge TTS (Microsoft bloqueaba con 403)
  - Español mexicano con acento natural
  - Sin límites ni API keys
- ✅ Together AI Flux configurado (imágenes cinematográficas)
- ✅ **Dependencias actualizadas**:
  - google-genai v1.57.0 (SDK oficial de Gemini)
  - moviepy v1.0.3 (ensamblaje de videos)
  - gTTS v2.5.4 (generación de audio)
- ✅ App con 4 fases implementadas
- ✅ **Fase 1 (Input) MEJORADA:**
  - Sistema de Plantillas Pre-configuradas (Marketing, Fitness, etc.)
  - Input manual flexible
  - 🆕 **MODO AUTOMÁTICO**: Generador de 4 escenas TikTok con Gemini
    - Radio button para alternar Manual/Automático/Paste
    - Inputs simplificados (tema, producto, hook)
    - Genera 4 escenas optimizadas al instante
    - Escenas editables en Fase 2
    - 🔥 **SISTEMA MULTI-PRODUCTO v2.5** (PROBADO Y VALIDADO):
      - ✅ **3 productos incluidos**:
        * 🍊 Frutíferas en Macetas ($7, 4 bonos)
        * 💼 Marketing Digital Pro ($27, 5 bonos)
        * 💪 Fitness en Casa ($17, 3 bonos)
      - ✅ Selector de producto en UI Modo Automático
      - ✅ Cada producto con template único, hooks específicos, precio y bonos
      - ✅ Templates dinámicos inyectados en prompts de Gemini
      - ✅ Hooks inteligentes por producto:
        * Frutíferas: Drenaje, Dinero, Espacio, Tiempo
        * Marketing: CTR, ROI, Audiencia, Escalamiento  
        * Fitness: Tiempo, Sin Gym, Grasa, Sostenible
      - ✅ CTAs 100% on-brand por producto
      - ✅ Auto-completado de precio según producto seleccionado
      - ✅ **TEST EXITOSO** (2026-01-09):
        - Producto: Frutíferas en Macetas con hook "Drenaje"
        - Resultado: 4 escenas generadas correctamente
        - Validado: Capítulo 3 mencionado, CTA exacto "$7 + 4 bonos"
        - Prompts: Todos en inglés con estilo cinematográfico
      - ✅ Escalable: agregar productos = editar diccionario (5 min)
  - 🆕 **MODO PASTE GEMINI**: Parser de guiones existentes
    - Pega texto de Gemini generado externamente
    - Extracción automática con regex (timestamps + prompts)
    - Soporta múltiples formatos de salida de Gemini
    - Auto-rellena campos para edición
- ✅ **Fase 3.5 (Asset Review) COMPLETA:**
  - Regeneración selectiva de imágenes (Flux)
  - Regeneración selectiva de audio (Edge TTS)
  - Validación antes del ensamblaje
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

**Última actualización:** 2026-01-11  
**Versión:** 2.7 (Hotmart Bonus PDFs + Humanized Scripts)  
**Proyecto:** Video Factory AI (Quantum Clic)
**Estado:** ✅ SISTEMA COMPLETO - Listo para Producción

---

## 📊 Resumen Técnico del Proyecto

### Stack Tecnológico Completo

| Componente | Tecnología | Versión | Estado |
|------------|------------|---------|--------|
| **Scripts** | Google Gemini 2.0 Flash | API v1.57.0 | ✅ Operacional |
| **Audio** | gTTS (Google TTS) | v2.5.4 | ✅ Operacional |
| **Imágenes** | Together AI Flux-Schnell | Latest | ✅ Operacional |
| **Video** | MoviePy | v1.0.3 | ✅ Operacional |
| **PDF Bonos** | fpdf2 | v2.8.5 | ✅ Operacional |

---

### Versiones Recientes

| Versión | Fecha | Cambios Principales |
|---------|-------|---------------------|
| **2.7** | 2026-01-11 | Bonos Premium PDF para Hotmart |
| **2.6** | 2026-01-11 | Humanización de Guiones + Bonos |

### Características Implementadas

✅ **Generación de Bonos Premium (v2.7)**:
- Portadas 3D profesionales generadas por IA.
- Automatización PDF con `generate_pdfs.py`.
- 4 guías completas para el nicho de frutíferas.

✅ **Humanización de Guiones (v2.6)**:
- Lenguaje natural, posesivos y mención personal de bonos.
- Anti-IA patterns (bloqueo de palabras clichés).

✅ **Flujo Completo**
1. **Fase 1**: Input (Manual/Automático/Paste)
2. **Fase 2**: Aprobación humana (editable)
3. **Fase 3**: Generación paralela de assets
4. **Fase 4**: Ensamblaje final de video

### Problemas Resueltos

| Problema | Solución | Fecha |
|----------|----------|-------|
| Edge TTS bloqueado 403 | Migración a gTTS | 2026-01-09 |
| Asyncio conflictos Streamlit | Subprocess helper (pre-gTTS) | 2026-01-09 |
| Falta de product templates | Sistema multi-producto | 2026-01-09 |
| CTAs inconsistentes | Templates con CTAs fijos | 2026-01-09 |

---

## 🚀 Para Empezar

**Requisitos**:
```bash
pip install google-genai==1.57.0 moviepy==1.0.3 gTTS==2.5.4 streamlit
```

**Configurar API Keys** en `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "tu-api-key-gemini"
TOGETHER_API_KEY = "tu-api-key-together"
```

**Ejecutar**:
```bash
streamlit run app.py
```

**Generar Video**:
1. Seleccionar "🚀 Automático nuevo"
2. Elegir producto (ej: Frutíferas en Macetas)
3. Ingresar tema y hook
4. Click "AUTO-GENERAR 4 ESCENAS"
5. Aprobar y producir assets
6. Descargar video final

---

**Desarrollado por**: Emmanuel  
**GitHub**: [appvideos](https://github.com/emmamena1/appvideos)  
**Último commit**: 61b0379
