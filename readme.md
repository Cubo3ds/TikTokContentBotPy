# 🤖 TikTok Automation Bot: Generación de Contenido (Texto y Audio)

Este proyecto es la base de un bot de automatización en Python, diseñado para generar el contenido central (guion viral y narración de voz) para videos cortos (como TikTok o Shorts). El enfoque inicial es la automatización de temas de **programación** y **tecnología**.

## ⚙️ Módulos Funcionales

El código actual maneja las dos primeras fases del proceso:

1.  **Módulo 1: Generación de Guion (Gemini API):**
    * Crea un guion viral optimizado, estructurado con las etiquetas **GANCHO**, **CUERPO** y **CIERRE**.
    * Utiliza un sistema de **caché** (`.txt`) para guardar el guion y evitar llamadas repetitivas a la API de Gemini si la idea del video no cambia, ahorrando costes.
2.  **Módulo 2: Generación de Audio (pyttsx3):**
    * Toma el guion de texto generado y lo convierte en una narración de voz en formato `.mp3`.
    * Esta narración es **100% gratuita** al utilizar la funcionalidad *Text-to-Speech* (TTS) integrada en el sistema operativo Windows.

---

## 🛠️ Requisitos y Configuración

### 1. Requisitos de Sistema

* **Python 3.x**
* **Git** (Para control de versiones)
* **Paquete de Voz en Español de Windows** (Esencial para evitar un acento extranjero. Debes instalar el paquete de "Voz" para el idioma Español - España o México desde la configuración de Windows).

### 2. Entorno Virtual

Se recomienda trabajar dentro de un entorno virtual (`venv`) para aislar las dependencias:

```bash
# 1. Crear el entorno virtual
python -m venv venv
# 2. Activar el entorno (Windows PowerShell)
.\venv\Scripts\activate

pip install google-genai pyttsx3 requests pathlib


🔑 Configuración de Clave (Gemini API)El bot requiere acceso a la API de Google Gemini para la generación de guiones.Las claves sensibles (API Keys) NUNCA se suben a GitHub.VariableServicioFunciónGEMINI_API_KEYGoogle AI (Gemini)Obligatorio para generar el guion inicial (Módulo 1).

💻 Cómo Configurar en Windows PowerShell
Ejecuta este comando en tu terminal antes de correr el script (reemplaza TU_CLAVE con tu valor real):

PowerShell

$env:GEMINI_API_KEY="TU_CLAVE_DE_GEMINI_AQUI"

🚀 Ejecución
Asegúrate de que el entorno virtual esté activo y la clave GEMINI_API_KEY configurada.

Abre el archivo tiktok_automation.py y define la variable IDEA_VIDEO dentro del bloque if __name__ == "__main__": con el tema de tu video.

Ejecuta el script principal:

Bash

python tiktok_automation.py

2. 🔑 Ejecutar el Comando de Desbloqueo
Una vez en la ventana de administrador, ejecuta este comando:

PowerShell

Set-ExecutionPolicy RemoteSigned -Scope Process