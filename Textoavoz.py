import pyttsx3
from gtts import gTTS

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Establece el idioma
engine.setProperty('voice', 'es')

# Texto que deseas convertir en voz
texto = "Hola, soy Andrés."

# Utiliza gTTS para convertir el texto en voz
tts = gTTS(texto, lang='es')

# Guarda el archivo de audio
tts.save("Salida.mp3")

# Reproduce el archivo de audio si lo deseas
engine.say(texto)
engine.runAndWait()
