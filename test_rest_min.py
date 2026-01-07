import os
import toml
import requests
import json

try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    api_key = secrets["DEEPGRAM_API_KEY"]
except:
    api_key = os.environ.get("DEEPGRAM_API_KEY")

url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
}
payload = {"text": "Hello world"}

print(f"Sending to {url}")
try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Body: {response.text}")
    else:
        print("SUCCESS")
except Exception as e:
    print(f"Error: {e}")
