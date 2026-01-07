import warnings
warnings.filterwarnings("ignore")
import os
import sys
sys.stderr = open(os.devnull, 'w')
from deepgram import DeepgramClient
import inspect

try:
    c = DeepgramClient(api_key="test")
    sig = inspect.signature(c.speak.v1.audio.generate)
    params = list(sig.parameters.keys())
    print("PARAMS:", params)
    
    if 'voice' in params: print("✅ HAS_VOICE")
    else: print("❌ NO_VOICE")
    
    if 'model' in params: print("✅ HAS_MODEL")
    else: print("❌ NO_MODEL")
    
    if 'options' in params: print("✅ HAS_OPTIONS")
    else: print("❌ NO_OPTIONS")
    
except Exception as e:
    print(f"Error: {e}")
