# utils/startup_check.py
"""
Validador de inicio para detectar problemas de compatibilidad antes de que ocurran.
Ejecutar con: python utils/startup_check.py
"""
import sys

def check_dependencies():
    """Verifica que las dependencias críticas estén instaladas correctamente."""
    errors = []
    warnings = []
    
    # 1. Verificar MoviePy
    try:
        import moviepy
        version = moviepy.__version__
        if version.startswith("2."):
            errors.append(f"❌ MoviePy {version} detectado. DEBE ser 1.0.3")
        elif version == "1.0.3":
            print(f"✅ MoviePy {version} OK")
        else:
            warnings.append(f"⚠️ MoviePy {version} - Se recomienda 1.0.3")
    except ImportError:
        errors.append("❌ MoviePy no instalado")
    
    # 2. Verificar decorator
    try:
        import decorator
        version = decorator.__version__
        if version == "4.4.2":
            print(f"✅ Decorator {version} OK")
        else:
            warnings.append(f"⚠️ Decorator {version} - Se recomienda 4.4.2")
    except ImportError:
        errors.append("❌ Decorator no instalado")
    
    # 3. Verificar Pillow y parche ANTIALIAS
    try:
        from PIL import Image
        import PIL
        version = PIL.__version__
        print(f"✅ Pillow {version} OK")
        
        # Aplicar parche si es necesario
        if not hasattr(Image, 'ANTIALIAS'):
            Image.ANTIALIAS = Image.Resampling.LANCZOS
            print("  ↳ Parche ANTIALIAS aplicado automáticamente")
    except ImportError:
        errors.append("❌ Pillow no instalado")
    
    # 4. Verificar importación de moviepy.editor
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
        print("✅ moviepy.editor imports OK")
    except ImportError as e:
        errors.append(f"❌ Error importando moviepy.editor: {e}")
    
    # 5. Verificar FFmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"✅ FFmpeg encontrado: {ffmpeg_path[:50]}...")
    except Exception as e:
        errors.append(f"❌ FFmpeg no disponible: {e}")
    
    # Resumen
    print("\n" + "="*50)
    if errors:
        print("🚨 ERRORES CRÍTICOS:")
        for e in errors:
            print(f"   {e}")
        return False
    elif warnings:
        print("⚠️ ADVERTENCIAS (puede funcionar pero no garantizado):")
        for w in warnings:
            print(f"   {w}")
        return True
    else:
        print("🎉 SISTEMA LISTO - Todas las dependencias OK")
        return True


if __name__ == "__main__":
    print("🔍 Verificando dependencias del sistema...\n")
    success = check_dependencies()
    sys.exit(0 if success else 1)
