import os
import toml
from deepgram import DeepgramClient

# Leer secrets
try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    api_key = secrets["DEEPGRAM_API_KEY"]
except:
    api_key = os.environ.get("DEEPGRAM_API_KEY")

client = DeepgramClient(api_key=api_key)

models_to_test = [
    "aura-asteria-en", # Control
    "aura-luna-es",    # Antiguo target
    "aura-celeste-es", # Nuevo target
    "aura-zeus-en"
]

for model in models_to_test:
    print(f"--- Testing {model} ---")
    try:
        response = client.speak.v1.audio.generate(
            text="Hello testing 1 2 3. Hola probando.",
            model=model
        )
        print(f"✅ SUCCESS with {model}")
        with open(f"test_{model}.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)
    except Exception as e:
        print(f"❌ FAILED {model}: {e}")
