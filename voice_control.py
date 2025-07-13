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
                print("[VOICE] 🎧 Escuchando...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="es-CO").lower()
                print(f"[VOICE] ✍️  Escuchado: {text}")

                if "done" in text or "completada" in text:
                    sprint_state.marcar_completada()
                    hablar("Tarea marcada como completada")
                elif "save" in text or "guardar" in text:
                    guardar_callback()
                    hablar("Sesión guardada")
                elif sprint_state.modo_crear or sprint_state.editando:
                    sprint_state.nuevo_texto = text
                    if sprint_state.modo_crear:
                        sprint_state.crear_nueva_tarea()
                        hablar("Tarea creada")
                    else:
                        sprint_state.confirmar_edicion()
                        hablar("Tarea editada")

        except Exception as e:
            print("[VOICE] Error:", e)
