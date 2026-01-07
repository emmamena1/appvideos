from deepgram import DeepgramClient
import inspect
try:
    c = DeepgramClient(api_key="test")
    # Navegar a la función
    # Puede ser c.speak.v1.audio.generate o similar
    # A veces es una propiedad dinámica.
    sig = inspect.signature(c.speak.v1.audio.generate)
    print(f"SIGNATURE: {sig}")
except Exception as e:
    print(f"Error: {e}")
