import os
try:
    import tomllib
except ImportError:
    import toml as tomllib

from deepgram import DeepgramClient

# Leer secret manualmente
with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

key = secrets.get("DEEPGRAM_API_KEY")
if not key:
    print("No key found")
    exit(1)

print(f"Key found: {key[:5]}...")

client = DeepgramClient(api_key=key)

print("Calling generate...")
try:
    # Usando el método que creemos que es correcto
    response = client.speak.v1.audio.generate(
        text="Prueba de audio",
        model="aura-luna-es"
    )
    
    print(f"Response type: {type(response)}")
    print(f"Response dir: {dir(response)}")
    
    # Intentar guardar
    filename = "debug_output.wav"
    with open(filename, "wb") as f:
        if hasattr(response, 'stream'):
            print("Has .stream, using getvalue()")
            f.write(response.stream.getvalue())
        else:
            print("Iterating response...")
            count = 0
            for chunk in response:
                f.write(chunk)
                count += 1
            print(f"Written {count} chunks")
            
    print(f"File size: {os.path.getsize(filename)}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
