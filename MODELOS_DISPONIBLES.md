# Modelos Google Gemini Disponibles en tu cuenta
# Generado: 2026-01-06

## Total de modelos: 54

### Modelos Gemini recomendados para generación de contenido:

1. **gemini-2.0-flash** ⭐ (RECOMENDADO - Usado en el proyecto)
   - Última versión estable
   - Balance perfecto entre velocidad y calidad
   - Soporta multimodal

2. **gemini-2.5-flash** 
   - Versión más reciente (puede estar en preview)
   - Mejor para pruebas de nuevas funcionalidades

3. **gemini-2.5-pro**
   - Máxima capacidad de razonamiento
   - Mejor para tareas complejas

4. **gemini-1.5-pro**
   - Versión anterior Pro, muy estable
   - Excelente para producción

5. **gemini-1.5-flash**
   - Versión anterior Flash, muy confiable
   - Buena opción de fallback

### Lista completa de modelos (primeros 20):
```
models/embedding-gecko-001
models/gemini-2.5-flash
models/gemini-2.5-pro
models/gemini-2.0-flash-exp
models/gemini-2.0-flash
models/gemini-2.0-flash-001
models/gemini-2.0-flash-exp-image-generation-exp-12-2025
models/gemini-2.0-flash-lite-001
models/gemini-2.0-flash-001-image-generation-exp-12-2025
models/gemini-2.0-flash-native-audio-preview-12-2025
models/gemini-2.5-flash-native-audio-preview-12-2025
models/gemini-1.5-flash
models/gemini-1.5-flash-8b
models/gemini-1.5-flash-001
models/gemini-1.5-pro
models/gemini-1.5-pro-001
models/veo-2.0-generate-001
```

## Configuración actual del proyecto:
- Archivo: `agents/scriptwriter.py`
- Modelo usado: `gemini-2.0-flash`
- SDK: `google-genai v1.56.0` (nuevo SDK, activamente mantenido)

## Migración completada:
✅ scriptwriter.py - Migrado a google.genai SDK con gemini-2.0-flash

## Pendientes de migración:
- agents/production_planner.py
- agents/quality_inspector.py
- agents/social_optimizer.py
- agents/visual_prompt_gen.py
- agents/code_doctor.py
- utils/youtube_scraper.py
- utils/debug_models.py
