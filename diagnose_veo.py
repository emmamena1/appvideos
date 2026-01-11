"""Script de diagnóstico para verificar credenciales de Veo"""
import os
import sys

print("=" * 50)
print("DIAGNÓSTICO DE CREDENCIALES VEO")
print("=" * 50)

# 1. Verificar si podemos importar las librerías
print("\n1. Verificando importaciones...")
try:
    from google.oauth2 import service_account
    print("   ✅ google.oauth2.service_account importado correctamente")
except ImportError as e:
    print(f"   ❌ Error importando google.oauth2: {e}")
    sys.exit(1)

try:
    from google import genai
    print("   ✅ google.genai importado correctamente")
except ImportError as e:
    print(f"   ❌ Error importando google.genai: {e}")
    sys.exit(1)

# 2. Buscar archivo JSON de credenciales
print("\n2. Buscando archivo JSON de credenciales...")
json_path = ".streamlit/gcp_service_account.json"
if os.path.exists(json_path):
    print(f"   ✅ Archivo encontrado: {json_path}")
else:
    print(f"   ❌ Archivo NO encontrado: {json_path}")
    sys.exit(1)

# 3. Crear objeto de credenciales
print("\n3. Creando objeto de credenciales...")
try:
    credentials = service_account.Credentials.from_service_account_file(
        json_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    print("   ✅ Objeto Credentials creado correctamente")
    print(f"   Service account email: {credentials.service_account_email}")
except Exception as e:
    print(f"   ❌ Error creando credenciales: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Crear cliente genai
print("\n4. Creando cliente genai con Vertex AI...")
PROJECT_ID = "gen-lang-client-0706301797"
LOCATION = "us-central1"

try:
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        credentials=credentials
    )
    print("   ✅ Cliente genai creado correctamente")
except Exception as e:
    print(f"   ❌ Error creando cliente: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("🎉 TODAS LAS VERIFICACIONES PASARON")
print("=" * 50)
