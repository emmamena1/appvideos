import os
import toml
from deepgram import DeepgramClient

# Leer secrets
try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    api_key = secrets["DEEPGRAM_API_KEY"]
except Exception as e:
    print(f"Error leyendo secrets: {e}")
    exit()

client = DeepgramClient(api_key=api_key)

text = "Hola, soy Celeste. Esta es una prueba de generación de audio con la nueva voz Aura 2 en español."
filename = "assets/audio/test_aura_celeste.wav"
os.makedirs("assets/audio", exist_ok=True)

print(f"Generando audio con: aura-celeste-es")

try:
    # En Deepgram TTS, 'model' suele ser el identificador de la voz (ej: aura-celeste-es)
    # No existe 'voice' separado en la API estandar TTS v1, el modelo ES la voz.
    response = client.speak.v1.audio.generate(
        text=text,
        model="aura-celeste-es"
    )
    
    # iterar y guardar
    with open(filename, "wb") as f:
        for chunk in response:
            f.write(chunk)
            
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print(f"✅ EXITO: Audio generado en {filename} ({os.path.getsize(filename)} bytes)")
    else:
        print("❌ FALLO: Archivo vacío o no creado")

except Exception as e:
    print(f"❌ ERROR CRÍTICO SDK: {e}")
    print("Intentando alternativa: model='aura-2' voice='aura-celeste-es' en kwargs...")
    try:
         # Intento alternativo por si la sugerencia del usuario de separar params es real
         response = client.speak.v1.audio.generate(
            text=text,
            model="aura-2",
            voice="aura-celeste-es"
        )
         with open(filename, "wb") as f:
            for chunk in response:
                f.write(chunk)
         print(f"✅ EXITO (Alternativa): {filename}")
    except Exception as ex:
        print(f"❌ ERROR ALTERNATIVA: {ex}")
