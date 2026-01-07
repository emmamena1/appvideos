# 🎬 AI Video Production Suite

Un sistema profesional de producción de videos automatizada con 8 agentes de IA trabajando en equipo para crear videos de calidad profesional desde una simple idea.

## 🎯 Características Principales

- **8 Agentes de IA Especializados**: Pipeline completo de producción automatizada
- **Interfaz Web Profesional**: Aplicación Streamlit con tema oscuro y diseño moderno
- **Scraping de YouTube**: Análisis de canales y videos para inspirar contenido
- **Generación de Imágenes**: Usando Together AI (Flux-Schnell) o Stability AI
- **Voiceover Profesional**: Integración con ElevenLabs para narración
- **Edición Avanzada**: MoviePy con efectos Ken Burns, transiciones, subtítulos
- **Optimización Social**: Metadata automática para redes sociales
- **Base de Datos SQLite**: Gestión completa de proyectos y videos

## 📋 Requisitos

- Python 3.9 o superior
- API Keys (ver sección de configuración)
- FFmpeg instalado (requerido por MoviePy)

### Instalación de FFmpeg

**Windows:**
```bash
# Usando Chocolatey
choco install ffmpeg

# O descargar desde https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## 🚀 Instalación

1. **Clonar o descargar el repositorio**
```bash
cd appvideos
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar API Keys**

Crea un archivo `.streamlit/secrets.toml` en el directorio raíz:

```toml
GEMINI_API_KEY = "tu_gemini_api_key"
ELEVENLABS_API_KEY = "tu_elevenlabs_api_key"
TOGETHER_API_KEY = "tu_together_api_key"
STABILITY_API_KEY = "tu_stability_api_key"  # Opcional
SUNO_API_KEY = "tu_suno_api_key"  # Opcional
```

O configúralas como variables de entorno:

```bash
# Windows
set GEMINI_API_KEY=tu_api_key
set ELEVENLABS_API_KEY=tu_api_key

# macOS/Linux
export GEMINI_API_KEY=tu_api_key
export ELEVENLABS_API_KEY=tu_api_key
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 🔑 Obtener API Keys

### 1. Google Gemini API Key
1. Visita https://makersuite.google.com/app/apikey
2. Crea un nuevo proyecto o selecciona uno existente
3. Genera una nueva API key
4. Copia la key en `.streamlit/secrets.toml`

### 2. ElevenLabs API Key
1. Visita https://elevenlabs.io
2. Crea una cuenta
3. Ve a tu perfil → API Keys
4. Genera una nueva key
5. Copia la key en `.streamlit/secrets.toml`

### 3. Together AI API Key
1. Visita https://together.xyz
2. Crea una cuenta
3. Ve a API Keys en tu dashboard
4. Genera una nueva key
5. Copia la key en `.streamlit/secrets.toml`

### 4. Stability AI API Key (Opcional)
1. Visita https://platform.stability.ai
2. Crea una cuenta
3. Ve a Account → API Keys
4. Genera una nueva key
5. Copia la key en `.streamlit/secrets.toml`

### 5. Suno API Key (Opcional, para música personalizada)
1. Visita https://suno.ai
2. Crea una cuenta
3. Obtén tu API key
4. Copia la key en `.streamlit/secrets.toml`

## 📖 Uso

### Crear un Video

1. Ve a la pestaña **"🎬 Crear Video"**
2. Describe tu idea de video en el campo de texto
3. Selecciona:
   - Estilo visual (Profesional, Moderno, Cinematográfico, etc.)
   - Duración (15s, 30s, 60s, 90s, 120s)
   - Formato (Vertical 9:16, Horizontal 16:9, Cuadrado 1:1)
   - Opciones adicionales (subtítulos, música personalizada)
4. Haz clic en **"🚀 Generar Video con IA"**
5. Espera mientras los 8 agentes trabajan en secuencia
6. Descarga tu video cuando esté listo

### Analizar Canal de YouTube

1. Ve a la pestaña **"🔍 Investigación & Scraping"**
2. Ingresa la URL del canal de YouTube
3. Haz clic en **"🔍 Analizar Canal"**
4. Revisa los insights generados por IA
5. Usa las sugerencias para crear videos similares

### Biblioteca de Videos

1. Ve a la pestaña **"📊 Biblioteca de Videos"**
2. Filtra por estado (Completados, En Proceso, Error)
3. Busca videos por título
4. Ve, descarga o elimina videos

### Configuración

1. Ve a la pestaña **"⚙️ Configuración"**
2. Ingresa tus API keys
3. Configura preferencias (voz, música, idioma)
4. Guarda la configuración

## 🤖 Los 8 Agentes

### 1. 🎯 Production Planner
- Analiza la idea del usuario
- Crea un plan completo de producción
- Define estilo visual, duración, concepto
- Usa: Google Gemini 1.5 Pro

### 2. ✍️ Scriptwriter
- Escribe un guion profesional con escenas
- Incluye narración, timing y descripciones visuales
- Usa: Google Gemini 1.5 Pro

### 3. 🎨 Visual Prompt Generator
- Convierte el script en prompts para IA
- Genera descripciones detalladas para cada escena
- Optimiza prompts para Flux/DALL-E/Stable Diffusion
- Usa: Google Gemini 1.5 Pro

### 4. 🎬 Video Generator
- Genera imágenes usando los prompts
- Usa Together AI (Flux-Schnell) o Stability AI
- Descarga y organiza los assets
- Salida: Carpeta con imágenes generadas

### 5. ✅ Quality Inspector
- Revisa la calidad de los assets generados
- Verifica que coincidan con el concepto
- Decide si necesita regeneración
- Usa: Google Gemini Vision
- Salida: Reporte de calidad + decisión

### 6. 🎵 Audio Director
- Genera el voiceover del script
- Selecciona música de fondo apropiada
- Define niveles de audio y mixing
- Usa: ElevenLabs + música de biblioteca
- Salida: Audio completo con música

### 7. ✂️ Video Editor
- Ensambla todo con MoviePy
- Añade transiciones, efectos, subtítulos
- Ajusta timing, zoom, animaciones
- Formato vertical (9:16) o personalizado
- Salida: Video MP4 final

### 8. 📱 Social Optimizer
- Genera título, descripción, hashtags
- Crea sugerencias de thumbnails
- Sugiere mejores horarios de publicación
- Usa: Google Gemini 1.5 Pro
- Salida: Metadata completa para redes

## 📁 Estructura del Proyecto

```
appvideos/
├── app.py                          # Aplicación principal Streamlit
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
│
├── agents/                         # Agentes de IA
│   ├── __init__.py
│   ├── production_planner.py      # Agente 1
│   ├── scriptwriter.py            # Agente 2
│   ├── visual_prompt_gen.py       # Agente 3
│   ├── video_generator.py         # Agente 4
│   ├── quality_inspector.py       # Agente 5
│   ├── audio_director.py          # Agente 6
│   ├── video_editor.py            # Agente 7
│   └── social_optimizer.py        # Agente 8
│
├── utils/                          # Utilidades
│   ├── __init__.py
│   ├── youtube_scraper.py         # Scraping de YouTube
│   ├── audio_processor.py         # Procesamiento de audio
│   ├── video_processor.py         # Procesamiento de video
│   ├── database.py                # Base de datos SQLite
│   └── config_loader.py           # Carga de configuración
│
├── config/                         # Configuraciones
│   ├── __init__.py
│   ├── settings.py                # Settings generales
│   └── prompts.py                 # Prompts para agentes
│
├── assets/                         # Assets del proyecto
│   ├── music/                     # Música de fondo
│   ├── fonts/                     # Fuentes para subtítulos
│   └── templates/                 # Templates de video
│
└── output/                         # Videos generados
    ├── projects/                  # Por proyecto
    └── final/                     # Videos finales
```

## 🔧 Troubleshooting

### Error: "FFmpeg not found"
- **Solución**: Instala FFmpeg siguiendo las instrucciones arriba
- Verifica que FFmpeg esté en tu PATH: `ffmpeg -version`

### Error: "API Key not configured"
- **Solución**: Verifica que tus API keys estén en `.streamlit/secrets.toml`
- Asegúrate de que las keys sean válidas y tengan créditos

### Error: "Module not found"
- **Solución**: Reinstala las dependencias: `pip install -r requirements.txt`
- Asegúrate de estar en el entorno virtual correcto

### Error: "Image generation failed"
- **Solución**: Verifica tus API keys de Together AI o Stability AI
- Revisa que tengas créditos disponibles
- Intenta reducir el número de escenas o la resolución

### Error: "Voiceover generation failed"
- **Solución**: Verifica tu API key de ElevenLabs
- Asegúrate de tener créditos en tu cuenta
- Verifica que la voz ID sea válida

### Videos generados son muy grandes
- **Solución**: El sistema usa compresión automática
- Puedes ajustar la bitrate en `config/settings.py`
- Considera usar formatos más cortos para reducir tamaño

### Proceso se detiene en un agente específico
- **Solución**: Revisa los logs en la consola
- Verifica que todos los agentes anteriores hayan completado
- Intenta generar un video más simple primero

## 💡 Tips y Mejores Prácticas

1. **Empieza Simple**: Crea videos cortos (15-30s) primero para probar
2. **Describe Bien**: Cuanto más detallada sea tu idea, mejor será el resultado
3. **Revisa los Prompts**: Los prompts se pueden personalizar en `config/prompts.py`
4. **Música Personalizada**: Añade tus propios archivos MP3 a `assets/music/`
5. **Monitorea Créditos**: Revisa regularmente el uso de tus APIs
6. **Backup de Videos**: Los videos se guardan en `output/final/`

## 🛣️ Roadmap

- [ ] Soporte para múltiples idiomas en voiceover
- [ ] Integración con Suno AI para música personalizada
- [ ] Generación de videos en batch
- [ ] Exportación directa a YouTube
- [ ] Templates predefinidos
- [ ] Sistema de cola para procesamiento asíncrono
- [ ] Integración con más modelos de generación de imágenes
- [ ] Editor de video manual
- [ ] Análisis de rendimiento de videos publicados

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de usarlo, modificarlo y compartirlo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Soporte

Si encuentras problemas o tienes preguntas:
1. Revisa la sección de Troubleshooting
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## ⚠️ Notas Importantes

- Las API keys son sensibles, nunca las compartas
- Los videos generados pueden consumir mucho espacio
- Algunos agentes pueden tardar varios minutos en completar
- El costo de las APIs depende de tu uso
- Revisa los términos de servicio de cada API que uses

## 🎉 ¡Disfruta Creando Videos!

Este sistema está diseñado para hacer que la creación de videos profesionales sea accesible para todos. ¡Experimenta, crea y comparte tus videos!

---

**Versión**: 1.0.0  
**Última actualización**: 2024
