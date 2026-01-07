import os
import toml
import requests

# Leer secrets
try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    api_key = secrets["DEEPGRAM_API_KEY"]
except:
    api_key = os.environ.get("DEEPGRAM_API_KEY")

def test_rest(model_param, desc):
    print(f"\n--- Testing REST: {desc} ({model_param}) ---")
    url = f"https://api.deepgram.com/v1/speak?{model_param}&encoding=linear16&sample_rate=48000"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"text": "Hola, prueba de audio en español."}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[OK] SUCCESS: {model_param}")
            # Guardar para validar que suena bien
            fname = f"rest_{model_param.replace('=', '_').replace('&', '_')}.wav"
            with open(fname, "wb") as f:
                f.write(response.content)
            print(f"   Saved to {fname}")
        else:
            print(f"[FAIL] FAIL: {response.status_code}")
            print(f"   Body: {response.text}")
    except Exception as e:
        print(f"[ERROR] ERROR: {e}")

# Probamos todas las variantes
test_rest("model=aura-asteria-en", "Control (English)")
test_rest("model=aura-luna-es", "Standard Spanish")
test_rest("model=aura-celeste-es", "Colombian Spanish")
test_rest("model=aura-2", "Aura-2 Auto")
test_rest("model=aura-2&voice=carina", "Aura-2 Carina")
test_rest("model=aura-2&language=es", "Aura-2 Lang ES")
