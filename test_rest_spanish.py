import os
import toml
import requests

try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    api_key = secrets["DEEPGRAM_API_KEY"]
except:
    api_key = os.environ.get("DEEPGRAM_API_KEY")

def try_params(params, desc):
    url = f"https://api.deepgram.com/v1/speak?{params}"
    headers = {"Authorization": f"Token {api_key}", "Content-Type": "application/json"}
    payload = {"text": "Hola soy una prueba en español"}
    print(f"Testing {desc}...")
    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 200:
            print(f"[OK] {desc}")
            with open(f"test_sp_{desc.split()[0]}.wav", "wb") as f:
                f.write(r.content)
            return True
        else:
            print(f"[FAIL] {desc}: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"[ERR] {e}")
        return False

# 1. Sugerencia User
try_params("model=aura-2&voice=carina", "Aura2_Carina")
# 2. Sugerencia User 2
try_params("model=aura-2&language=es", "Aura2_LangES")
# 3. Posible nombre completo
try_params("model=aura-celeste-es", "AuraCelesteES")
# 4. Posible variante
try_params("model=aura-luna-es", "AuraLunaES")
