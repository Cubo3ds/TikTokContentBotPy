

# tiktok_automation.py

# --- 1. IMPORTACIONES ---
from google import genai
from pathlib import Path
import hashlib # <--- ¡Asegúrate de agregar esta línea!
import pyttsx3
import os
import re



# --- 2. CONFIGURACIÓN DE RUTAS ---
# Carpeta donde se guardarán todos los archivos generados (audio, video, etc.)
OUTPUT_DIR = Path("output_content")
OUTPUT_DIR.mkdir(exist_ok=True)

client = None

if "GEMINI_API_KEY" in os.environ:
    try:
        client = genai.Client()
    except Exception as e:
        print(f"❌ Error al inicializar el cliente de Gemini: {e}")

# ----------------------------------------------------------------------
# MÓDULO 1: GENERAR GUION VIRAL (GEMINI - GRATUITO)
# ----------------------------------------------------------------------

def generar_guion_viral(idea_principal):
    """
    Toma una idea simple y la convierte en un guion de TikTok viral.
    Utiliza un caché local (.txt) para evitar llamadas repetitivas a la API.
    """
    if client is None:
        print("❌ ERROR: La clave GEMINI_API_KEY no está establecida o el cliente falló.")
        return None
    
    print(f"--- MÓDULO 1: Generación de Guion ---")
    
    # 1. GENERAR NOMBRE DE ARCHIVO CACHÉ (usamos un hash simple de la idea)
    # Esto asegura que cada idea tenga su propio archivo de caché.
    import hashlib
    hash_object = hashlib.sha1(idea_principal.encode())
    cache_filename = f"guion_{hash_object.hexdigest()[:10]}.txt"
    cache_path = OUTPUT_DIR / cache_filename
    
    # 2. INTENTAR CARGAR DESDE CACHÉ
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            guion = f.read()
        print(f"✅ Guion cargado exitosamente desde caché: {cache_path.name}")
        return guion
        
    # 3. SI NO HAY CACHÉ, LLAMAR A LA API (el código que ya tenías)
    print(f"Guion no encontrado en caché. Llamando a la API de Gemini...")
    
    prompt = f"""
    Eres un experto en la creación de guiones de video cortos y virales para TikTok, enfocados en temas de programación y tecnología.
    Tu objetivo es tomar la idea principal del usuario y expandirla a un guion con la estructura viral clave para mantener la atención.
    
    El guion debe ser corto, dinámico y tener una duración máxima de 30 segundos.
    
    DEVUELVE LA RESPUESTA ÚNICAMENTE USANDO ESTA ESTRUCTURA DE FORMATO, SIN TEXTO ADICIONAL NI INTRODUCCIONES:
    
    GANCHO: [Máximo 5 segundos, pregunta impactante o declaración atrevida relacionada con la idea]
    CUERPO: [Desarrollo rápido de la idea, explicación concisa, incluye términos técnicos en español si es necesario]
    CIERRE: [Llamada a la acción (CTA) clara, como "Sígueme" o "Deja tu comentario"]
    
    IDEA PRINCIPAL: {idea_principal}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt
        )
        guion_generado = response.text
        
        # 4. GUARDAR EN CACHÉ ANTES DE RETORNAR
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(guion_generado)
            
        print("✅ Guion generado y guardado en caché exitosamente.")
        return guion_generado
        
    except Exception as e:
        print(f"❌ Error al contactar con la API de Gemini: {e}")
        return None

# ----------------------------------------------------------------------
# MÓDULO 2: GENERACIÓN DE AUDIO MEJORADO (pyttsx3 - 100% GRATUITO)
# ----------------------------------------------------------------------

def generar_audio_gratis(guion_completo, nombre_archivo="narracion_bot_tts.mp3"):
    """
    Toma el guion completo (cargado desde caché o generado por Gemini), 
    extrae el texto de narración y lo convierte a voz con ajustes de calidad.
    """
    
    # 1. Limpieza del Texto: Extraer solo la parte del diálogo.
    # Esto elimina las etiquetas como "GANCHO:" y los corchetes "[]"
    dialogo_lines = []
    for line in guion_completo.splitlines():
        # Busca el contenido después de los dos puntos.
        if ':' in line:
            # Quitamos la etiqueta, y luego eliminamos corchetes para obtener el texto limpio.
            texto_linea = line.split(':', 1)[1].strip().replace('[', '').replace(']', '')
            dialogo_lines.append(texto_linea)
            
    texto_a_narrar = " ".join(dialogo_lines)
    
    if len(texto_a_narrar.strip()) < 10:
        print("❌ Error: No se encontró texto para narrar. Verifique el formato del guion (GANCHO: [...] etc).")
        return None

    try:
        engine = pyttsx3.init()
        ruta_audio = OUTPUT_DIR / nombre_archivo

        print(f"\n--- MÓDULO 2 MEJORADO: Generación de Audio ---")
        
        # --- CONFIGURACIÓN PARA MEJORAR LA VOZ ---
        
        # 1. Ajustar la VELOCIDAD (Rate): Ritmo más lento y natural que el predeterminado
        engine.setProperty('rate', 165) 

        # 2. SELECCIÓN DE VOZ: 
        # Intenta usar la voz secundaria para evitar la predeterminada más robótica.
        try:
             voices = engine.getProperty('voices')
             # Usamos el segundo índice disponible (prueba con [0], [1], [2] si no te gusta)
             engine.setProperty('voice', voices[1].id) 
        except Exception:
             print("⚠️ No se pudo cambiar la voz. Usando la predeterminada del sistema.")


        print(f"Narrando texto con ritmo ajustado...")
        
        # Guarda el audio en un archivo
        engine.save_to_file(texto_a_narrar, str(ruta_audio))
        engine.runAndWait() 
        
        print(f"✅ Audio guardado exitosamente de forma gratuita en: {ruta_audio}")
        return ruta_audio
        
    except Exception as e:
        print(f"❌ Ocurrió un error al generar el audio TTS local. {e}")
        return None

# --- FUNCIÓN PRINCIPAL DEL BOT (EJECUCIÓN) ---
if __name__ == "__main__":
    
    print("\n=======================================================")
    print("🚀 INICIO DEL PROCESO DE GENERACIÓN AUTOMÁTICA DE VIDEO 🚀")
    print("=======================================================\n")
    
    # 1. DEFINICIÓN DE VARIABLES BASE
    
    # ⚠️ IDEA DEL VIDEO: Define qué paso de la construcción del bot estás cubriendo.
    IDEA_VIDEO = "Estamos por codificar la parte del bot que convierte el guion de texto en una narración de voz usando pyttsx3, usando la caché del guion."
    
    # Nombre del archivo de audio que se creará
    NOMBRE_AUDIO = "audio_tts_mejorado.mp3" 
    
    # Tema para la búsqueda visual (Módulo 3)
    TEMA_VISUAL = "programación python automatización" 

    
    # 2. EJECUTAR MÓDULO 1: GENERACIÓN DE GUION (CON CACHÉ)
    # Si el guion ya existe en caché (.txt), se carga. Si no, llama a Gemini.
    guion_final = generar_guion_viral(IDEA_VIDEO)

    if guion_final:
        print("\n--- Guion Final ---")
        print(guion_final)
        
        # 3. EJECUTAR MÓDULO 2: GENERACIÓN DE AUDIO (VOZ MEJORADA)
        ruta_audio = generar_audio_gratis(guion_final, NOMBRE_AUDIO)
        
        if ruta_audio:
            print(f"\n✅ Guion y Audio listos. Duración de la narración: [Necesita MoviePy para calcular]")
            
            # 4. PRÓXIMO PASO: EJECUTAR MÓDULO 3 (ADQUISICIÓN DE VISUALES)
            print("\n--- Preparando Módulo 3 (Adquisición de Visuales) ---")
            # video_path = adquirir_visuales_pexels(TEMA_VISUAL) 
            # Si el video se descarga, encadenaríamos al Módulo 4.
        
    print("\n=======================================================")
    print("✅ PROCESO DE CONTENIDO TEXTO/AUDIO COMPLETADO.         ")
    print("=======================================================")