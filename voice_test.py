import speech_recognition as sr

recognizer = sr.Recognizer()

def test_microfono():
    try:
        with sr.Microphone() as mic:
            print("🎤 Di algo... (grabando por 5 segundos)")
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic, timeout=5)
            print("🧠 Procesando...")
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"✅ Lo que dijiste fue: {texto}")
    except sr.WaitTimeoutError:
        print("⏳ No se detectó voz a tiempo.")
    except sr.UnknownValueError:
        print("😕 No se entendió lo que dijiste.")
    except sr.RequestError:
        print("❌ Error al conectar con el servicio de reconocimiento.")
    except Exception as e:
        print(f"🚨 Otro error: {e}")

test_microfono()
