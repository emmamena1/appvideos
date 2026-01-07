import warnings
warnings.filterwarnings("ignore")
import os
import sys

# Suppress stderr
sys.stderr = open(os.devnull, 'w')

from deepgram import DeepgramClient
import inspect

try:
    c = DeepgramClient(api_key="test")
    sig = inspect.signature(c.speak.v1.audio.generate)
    print(f"SIGNATURE: {sig}")
except Exception as e:
    print(f"Error: {e}")
