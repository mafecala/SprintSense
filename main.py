import cv2, time, threading, os
from detection import PersonDetector
from gesture_control import GestureController
from voice_control import run_voice_recognition
from sprint_state import SprintState

def exportar_sesion(frame, sprint_state, lineas):
    ts = time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(ts, exist_ok=True)

    # Guardar imagen del dibujo
    dibujo = frame.copy()
    for pt1, pt2 in lineas:
        cv2.line(dibujo, pt1, pt2, (255, 255, 0), 3)
    cv2.imwrite(f"{ts}/dibujo.png", dibujo)

    # Guardar archivo de texto con tareas
    with open(f"{ts}/tareas.txt", "w") as f:
        for t, e in sprint_state.tareas.items():
            f.write(f"{t}: {e}\n")

def main():
    cap = cv2.VideoCapture(1)
    detector = PersonDetector()
    state = SprintState()
    controller = GestureController(state)
    current = None
    last_seen = time.time()

    threading.Thread(target=run_voice_recognition, args=(state, lambda: exportar_sesion(current, state, controller.lineas)), daemon=True).start()

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

        # Mostrar tareas (más separadas)
        for i, (t, e) in enumerate(state.tareas.items()):
            y = 100 + 50 * i
            col = (0,255,0) if e=="Done" else (0,0,255)
            sel = ">" if t == state.seleccionada else " "
            cv2.putText(frame, f"{sel} {t}: {e}", (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, col, 2)

        if state.modo_seleccion:
            cv2.rectangle(frame,(10,10),(200,50),(50,50,200),-1)
            cv2.putText(frame,"Eliminar tarea",(15,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.rectangle(frame,(220,10),(360,50),(100,150,50),-1)
            cv2.putText(frame,"Editar tarea",(225,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        cv2.rectangle(frame,(380,10),(520,50),(150,100,255),-1)
        modo = "Dibujo" if state.modo_dibujo else "Seleccion"
        cv2.putText(frame,f"{modo}",(385,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        cv2.rectangle(frame,(540,10),(700,50),(0,100,100),-1)
        cv2.putText(frame,"+Nueva",(545,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        if state.modo_dibujo:
            cv2.rectangle(frame,(720,10),(860,50),(0,0,100),-1)
            cv2.putText(frame,"Limpiar",(730,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        if state.modo_crear or state.editando:
            label = "Nueva tarea: " if state.modo_crear else "Editando: "
            txt = state.nuevo_texto
            cv2.rectangle(frame,(50,420),(700,460),(0,0,0),-1)
            cv2.putText(frame, label+txt,(60,450),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

        cv2.imshow("SprintSense™", frame)
        key = cv2.waitKey(5)&0xFF
        if key == 27:
            exportar_sesion(current, state, controller.lineas)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
