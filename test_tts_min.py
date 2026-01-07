import asyncio
import edge_tts

async def main():
    voice = "es-MX-DaliaNeural"
    text = "Hola mundo prueba"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("test_min.mp3")

try:
    asyncio.run(main())
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
