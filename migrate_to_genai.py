"""
Script de migración automática de google.generativeai a google.genai
"""
import os
import re

# Archivos a actualizar
files_to_update = [
    "agents/production_planner.py",
    "agents/quality_inspector.py",
    "agents/social_optimizer.py",
    "agents/visual_prompt_gen.py",
    "agents/code_doctor.py",
    "utils/youtube_scraper.py",
    "utils/debug_models.py"
]

def migrate_file(filepath):
    """Migra un archivo del antiguo SDK al nuevo"""
    print(f"\n📝 Procesando: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"  ⚠️ Archivo no encontrado, saltando...")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Actualizar imports
    content = content.replace(
        "import google.generativeai as genai",
        "from google import genai\nfrom google.genai import types"
    )
    
    # 2. Actualizar configuración
    content = re.sub(
        r'genai\.configure\(api_key=([^\)]+)\)',
        r'client = genai.Client(api_key=\1)',
        content
    )
    
    # 3. Actualizar creación de modelos
    content = re.sub(
        r'genai\.GenerativeModel\(([^\)]+)\)',
        r'# Usar client.models.generate_content() en lugar de GenerativeModel',
        content
    )
    
    if content != original_content:
        # Hacer backup
        backup_path = filepath + ".backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"  💾 Backup creado: {backup_path}")
        
        # Guardar cambios
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Migrado exitosamente")
    else:
        print(f"  ℹ️ No se requieren cambios")

print("🔄 INICIANDO MIGRACIÓN A google.genai")
print("=" * 50)

for filepath in files_to_update:
    migrate_file(filepath)

print("\n" + "=" * 50)
print("✨ MIGRACIÓN COMPLETADA")
print("\n⚠️ NOTA IMPORTANTE:")
print("Las migraciones automáticas necesitan revisión manual.")
print("Especialmente los métodos generate_content() que ahora requieren:")
print("  client.models.generate_content(model='nombre', contents='...')")
