import cv2, time, threading
from detection import PersonDetector
from gesture_control import GestureController
from voice_control import run_voice_recognition
from sprint_state import SprintState

def guardar_sesion(frame, sprint_state):
    ts = time.strftime("%Y%m%d-%H%M%S")
    cv2.imwrite(f"screenshot_{ts}.png", frame)
    with open(f"log_{ts}.txt", "w") as f:
        for t, e in sprint_state.tareas.items():
            f.write(f"{t}: {e}\n")

def main():
    cap = cv2.VideoCapture(1)
    detector = PersonDetector()
    state = SprintState()
    controller = GestureController(state)
    current = None
    last_seen = time.time()

    threading.Thread(target=run_voice_recognition, args=(state, lambda: guardar_sesion(current, state)), daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        current = frame.copy()

        if detector.detect_person(frame):
            last_seen = time.time()
        elif time.time() - last_seen > 5:
            cv2.putText(frame, "Esperando presencia...", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(100,100,100),2)
            cv2.imshow("SprintSense™", frame)
            if cv2.waitKey(5)&0xFF==27: break
            continue

        frame = controller.process_frame(frame)

        for i, (t, e) in enumerate(state.tareas.items()):
            col = (0,255,0) if e=="Done" else (0,0,255)
            sel = ">" if t==state.seleccionada else " "
            cv2.putText(frame, f"{sel} {t}: {e}", (50,100+30*i), cv2.FONT_HERSHEY_SIMPLEX,0.8,col,2)

        if state.modo_seleccion:
            cv2.rectangle(frame,(10,10),(200,50),(50,50,200),-1)
            cv2.putText(frame,"Eliminar tarea",(15,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.rectangle(frame,(220,10),(360,50),(100,150,50),-1)
            cv2.putText(frame,"Editar tarea",(225,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        cv2.rectangle(frame,(380,10),(520,50),(150,100,255),-1)
        modo = "Dibujo" if state.modo_dibujo else "Seleccionar"
        cv2.putText(frame,f"Modo: {modo}",(385,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        cv2.rectangle(frame,(540,10),(700,50),(0,100,100),-1)
        cv2.putText(frame,"+ Nueva tarea",(545,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        if state.modo_crear or state.editando:
            label = "Nueva tarea: " if state.modo_crear else "Editando: "
            txt = state.nuevo_texto
            cv2.rectangle(frame,(50,420),(700,460),(0,0,0),-1)
            cv2.putText(frame, label+txt,(60,450),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

        cv2.imshow("SprintSense™", frame)
        key = cv2.waitKey(5)&0xFF
        if key==27: break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
