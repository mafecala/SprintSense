# voice_control.py
import speech_recognition as sr
import pyttsx3

def run_voice_recognition(sprint_state, guardar_callback):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    def hablar(mensaje):
        engine.say(mensaje)
        engine.runAndWait()

    while True:
        try:
            with mic as source:
                print("[VOICE] Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="es-CO").lower()
                print(f"[VOICE] Heard: {text}")

                if "done" in text:
                    sprint_state.marcar_completada()
                    hablar("Tarea marcada como completada")
                elif "save" in text:
                    guardar_callback()
                    hablar("Sesión guardada")

        except Exception as e:
            print("[VOICE] Error:", e)
