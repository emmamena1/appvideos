from google import genai
import os
import sys

# Configurar UTF-8 para la salida
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Intenta cargar la API KEY
try:
    # Primero intenta desde variable de entorno
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Si no está en variable de entorno, intenta cargar manualmente del archivo secrets.toml
    if not api_key:
        try:
            import toml
            secrets = toml.load(".streamlit/secrets.toml")
            api_key = secrets["GOOGLE_API_KEY"]
        except FileNotFoundError:
            print("ERROR: No encontre .streamlit/secrets.toml")
            sys.exit(1)
        except KeyError:
            print("ERROR: El archivo secrets.toml no tiene la clave 'GOOGLE_API_KEY'")
            print("\nTu archivo debe tener este formato:")
            print('GOOGLE_API_KEY = "tu_clave_api_aqui"')
            sys.exit(1)

    if not api_key:
        print("ERROR: No encontre la API KEY en ninguna ubicacion")
        sys.exit(1)

    # Configurar el nuevo cliente
    client = genai.Client(api_key=api_key)

    print("\n=== MODELOS DISPONIBLES PARA TU CUENTA ===")
    print("=" * 50)
    found_any = False
    
    # Listar modelos usando el nuevo SDK
    models = client.models.list()
    for m in models:
        print(f"OK: {m.name}")
        found_any = True
    
    if not found_any:
        print("No se encontraron modelos. Revisa tu API Key.")
    else:
        print("\n=== MODELOS RECOMENDADOS ===")
        print("  - gemini-1.5-flash (rapido y economico)")
        print("  - gemini-1.5-pro (mas potente)")
        print("  - gemini-2.0-flash (ultima version)")
        print("\n" + "=" * 50)
        print("TOTAL DE MODELOS:", sum(1 for _ in client.models.list()))

except Exception as e:
    print(f"Error fatal: {e}")
    import traceback
    traceback.print_exc()
