import speech_recognition as sr

recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language="es-ES")  # Cambia "es-ES" si necesitas otro idioma
        print("Texto reconocido:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return None
    except sr.RequestError:
        print("Error con el servicio de reconocimiento")
        return None