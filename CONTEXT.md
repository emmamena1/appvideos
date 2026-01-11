# CONTEXT.md - Video Factory AI

**INSTRUCCIONES PARA ANTIGRAVITY:**
1. Lee estos archivos antes de responder.
2. ⚠️ **PROTOCOLO OBLIGATORIO:** Al finalizar CUALQUIER tarea de código, DEBES actualizar este archivo (`CONTEXT.md`) con el nuevo estado del sistema y realizar un `git push` de todos los cambios inmediatamente. NO ESPERES a que el usuario lo pida.

---

## 🎯 PROYECTO: Video Factory AI (v2.8)
**Estado:** ✅ SISTEMA PREMIUM - Multi-Producto + Google Veo + Bonos Hotmart

---

**Última actualización:** 2026-01-11  
**Versión:** 2.8 (Google Veo Integration + Auth Resiliency)  
**Proyecto:** Video Factory AI (Quantum Clic)

---

## 📊 Resumen Técnico

### Stack Tecnológico Completo

| Componente | Tecnología | Versión | Estado |
|------------|------------|---------|--------|
| **Scripts** | Google Gemini 2.0 Flash | API v1.57.0 | ✅ Operacional |
| **Video AI** | **Google Veo (Beta)** | Vertex AI | ⚠️ Configuración Credenciales |
| **Audio** | gTTS (Google TTS) | v2.5.4 | ✅ Operacional |
| **Imágenes** | Together AI Flux-Schnell | Latest | ✅ Operacional |
| **Video Editor** | MoviePy | v1.0.3 | ✅ Soporta Clips MP4 |
| **PDF Bonos** | fpdf2 | v2.8.5 | ✅ Operacional |

---

### Versiones Recientes

| Versión | Fecha | Cambios Principales |
|---------|-------|---------------------|
| **2.8** | 2026-01-11 | Integración Google Veo (Vertex AI) + Soporte Service Account |
| **2.7** | 2026-01-11 | Bonos Premium PDF para Hotmart (Portadas 3D + Automation) |
| **2.6** | 2026-01-11 | Humanización de Guiones (Natural, Posesivos, Anti-IA) |

---

### Características Críticas

✅ **Generación de Video Cinemático (v2.8)**:
- Integración con Google Veo vía Vertex AI.
- Selector Global en Sidebar: Imagen (Flux) vs Video (Veo).
- Soporte para mezcla de clips MP4 en el ensamblaje MoviePy.

✅ **Bonos Premium (v2.7)**:
- 4 Guías PDF profesionales para Frutíferas.
- Mockups 3D de portadas generados por IA.

✅ **Sistema Multi-Producto**:
- Soporte para Frutíferas, Marketing Digital y Fitness.
- Templates dinámicos y hooks inteligentes por nicho.

---

## 🔑 CONFIGURACIÓN VEO (IMPORTANTE)

El sistema busca credenciales en este orden:
1. `GCP_SERVICE_ACCOUNT` en `.streamlit/secrets.toml`.
2. `GOOGLE_APPLICATION_CREDENTIALS` (variable de entorno).
3. `gcloud auth application-default login`.

---

## 📁 ESTRUCTURA CLAVE:
```
appvideos/
├── agents/
│   ├── scriptwriter.py       (Gemini 2.0)
│   ├── audio_generator.py    (gTTS)
│   ├── visual_generator.py   (Flux)
│   ├── veo_generator.py      (Google Veo)
│   └── video_editor.py       (MoviePy 1.0.3)
├── assets/
│   ├── final_output/         (TikToks Listos)
│   ├── generated_videos/     (Clips de Veo)
│   └── bonos_pdf_final/      (Bonos Hotmart)
└── app.py                    (Orquestador 4 fases)
```

**Último commit**: 3fec5da
