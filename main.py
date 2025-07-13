# main.py
import cv2
import threading
import time
from detection import PersonDetector
from gesture_control import GestureController
from voice_control import run_voice_recognition
from sprint_state import SprintState

def guardar_sesion(frame, sprint_state):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    cv2.imwrite(f"screenshot_{timestamp}.png", frame)
    with open(f"log_{timestamp}.txt", "w") as f:
        for tarea, estado in sprint_state.tareas.items():
            f.write(f"{tarea}: {estado}\n")
    print("[LOG] Sesión guardada")

def main():
    cap = cv2.VideoCapture(1)
    detector = PersonDetector()
    sprint_state = SprintState()
    controller = GestureController(sprint_state)
    canvas_open = False
    last_seen = time.time()
    current_frame = None

    threading.Thread(target=run_voice_recognition, args=(sprint_state, lambda: guardar_sesion(current_frame, sprint_state)), daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        current_frame = frame.copy()

        if detector.detect_person(frame):
            last_seen = time.time()
            canvas_open = True
        elif time.time() - last_seen > 5:
            canvas_open = False

        if canvas_open:
            frame = controller.process_frame(frame)

            # Mostrar tareas
            for i, (tarea, estado) in enumerate(sprint_state.tareas.items()):
                color = (0, 255, 0) if estado == "Done" else (0, 0, 255)
                highlight = tarea == sprint_state.seleccionada
                cv2.putText(frame, f"{'>' if highlight else ' '} {tarea}: {estado}",
                            (50, 100 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        else:
            cv2.putText(frame, "Esperando presencia humana...", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)

        cv2.imshow("SprintSense™", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
