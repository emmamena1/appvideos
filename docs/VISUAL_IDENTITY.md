# 🎨 Actualización: Sistema de Identidad Visual Cinematográfica

**Fecha:** 2026-01-06  
**Archivo modificado:** `agents/production_planner.py`

---

## ¿Qué se actualizó?

Se implementó un **sistema profesional de prompts visuales** para FLUX.1 que transforma las imágenes generadas de "clipart AI" a **fotografía industrial cinematográfica**.

---

## Nuevas Constantes

### 1. VISUAL_IDENTITY
Define el estilo visual general:
- Ultra-realistic cinematic industrial photography
- Physically plausible lighting
- Documentary-fashion hybrid aesthetic

### 2. MASTER_PROMPT_FORMULA
Estructura obligatoria para todos los prompts visuales:
1. Subject (descripción física)
2. Action (momento fotográfico)
3. Context (lógica espacial)
4. Lighting (dirección, temperatura, suavidad)
5. Camera (lente, apertura, sensor)
6. Texture (detalles de materiales)

### 3. GOLD_KEYWORDS (16 palabras)
Keywords que FLUX ama para maximizar realismo:
- "Physically based lighting"
- "Natural skin pores"
- "Sensor noise grain"
- "Documentary realism"
- etc.

### 4. NEGATIVE_PROMPTS (13 conceptos)
Conceptos prohibidos para eliminar el "AI look":
- cartoon, CGI, 3D render
- plastic skin, beauty filter
- exaggerated proportions
- etc.

---

## Ejemplo de Prompt Generado

**Antes (genérico):**
```
Close up of industrial worker, natural lighting, realistic
```

**Ahora (cinematográfico):**
```
Ultra-realistic cinematic photograph of weathered industrial worker, 45 years old, 
natural skin pores visible, grease-stained blue coveralls, soft window light from 
left at 5200K, medium format look, 85mm f/2.8, shallow depth of field, filmic grain, 
surface imperfections, documentary realism
```

---

## Cómo Funciona

Cuando Gemini genera el guion, ahora:
1. Lee la **VISUAL_IDENTITY** (el estilo general)
2. Aplica la **MASTER_PROMPT_FORMULA** (estructura)
3. Inyecta **GOLD_KEYWORDS** (calidad)
4. Evita **NEGATIVE_PROMPTS** (anti-AI)

Resultado: Prompts técnicos de 50-100 palabras que FLUX interpreta como fotografía profesional.

---

## Reglas de Oro

1. ✅ **NUNCA** modificar VISUAL_IDENTITY sin probar primero
2. ✅ **SIEMPRE** mantener los GOLD_KEYWORDS actualizados según lo que funcione
3. ✅ **AGREGAR** nuevos NEGATIVE_PROMPTS si aparecen defectos recurrentes
4. ❌ **NO** usar palabras genéricas como "beautiful" o "amazing"
5. ❌ **NO** empezar prompts con "A photo of..." o "Image of..."

---

## Blindaje

Este sistema está protegido por:
- **Constantes en mayúsculas** (difíciles de modificar por error)
- **Documentación clara** en el prompt para Gemini
- **Ejemplos específicos** que guían a la IA

Si necesitas ajustar el estilo visual, modifica solo `VISUAL_IDENTITY`. El resto debe permanecer estable.
