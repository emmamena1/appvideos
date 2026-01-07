# 🚀 Guía Rápida de Configuración

## Paso 1: Configurar API Keys

Abre el archivo `.streamlit/secrets.toml` y agrega las siguientes claves:

```toml
GOOGLE_API_KEY = "tu_api_key_de_google_gemini"
DEEPGRAM_API_KEY = "tu_api_key_de_deepgram"
TOGETHER_API_KEY = "tu_api_key_de_together_ai"
```

### Dónde obtener las keys:

1. **Google Gemini**: https://aistudio.google.com/app/apikey
2. **Deepgram**: https://console.deepgram.com/ (Sign up → Create API Key)
3. **Together AI**: https://api.together.xyz/settings/api-keys (Sign up → API Keys)

---

## Paso 2: Instalar dependencias (si es necesario)

```bash
python -m pip install together deepgram-sdk
```

---

## Paso 3: Ejecutar la aplicación

```bash
streamlit run app.py
```

---

## Paso 4: Flujo de uso

1. **Ingresar tema y producto** → Clic en "Generar Plan Maestro"
2. **Revisar y editar escenas** → Modificar narración y prompts visuales
3. **Aprobar y producir** → Los agentes generarán audio + imágenes
4. **Ver resultados** → Preview de todos los assets generados

---

## 🎯 Notas Importantes

- Los assets se guardan en `assets/audio/` y `assets/images/`
- Si ya existen, se reutilizan (ahorro de créditos)
- Cada escena toma ~10-30 segundos en generar
- Puedes volver a editar en cualquier momento

---

## ⚠️ Troubleshooting

**Error: "Agent no está listo"**
→ Verifica que la API key esté en `secrets.toml`

**Error: "Module not found"**
→ Ejecuta: `python -m pip install together deepgram-sdk`

**Imágenes no se generan**
→ Revisa tu crédito/plan en Together AI

**Audio no se genera**
→ Revisa tu crédito en Deepgram
