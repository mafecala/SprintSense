import cv2
import mediapipe as mp

class GestureController:
    def __init__(self, sprint_state):
        self.sprint_state = sprint_state
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.frame_count = 0
        self.cooldown = 15
        self.dibujando = False
        self.prev_point = None
        self.lineas = []

    def dedos_extendidos(self, lm):
        dedos = []
        # Pulgar
        dedos.append(lm[4].x < lm[3].x)  # Mano derecha: x del pulgar menor al de la base
        # Índice a meñique
        for tip in [8, 12, 16, 20]:
            dedos.append(lm[tip].y < lm[tip - 2].y)
        return all(dedos)

    def process_frame(self, frame):
        self.frame_count += 1
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                lm = hand.landmark
                index_tip = lm[8]
                thumb_tip = lm[4]

                x_index = int(index_tip.x * w)
                y_index = int(index_tip.y * h)
                x_thumb = int(thumb_tip.x * w)
                y_thumb = int(thumb_tip.y * h)

                cv2.circle(frame, (x_index, y_index), 10, (0, 255, 255), -1)

                distancia = ((x_index - x_thumb)**2 + (y_index - y_thumb)**2)**0.5

                # 🤏 Dibujo con pinza
                if self.sprint_state.modo_dibujo and distancia < 40:
                    if self.prev_point:
                        self.lineas.append((self.prev_point, (x_index, y_index)))
                    self.prev_point = (x_index, y_index)
                    self.dibujando = True
                else:
                    self.prev_point = None
                    self.dibujando = False

                # ✋ Gesto de mano abierta para limpiar
                if self.sprint_state.modo_dibujo and self.dedos_extendidos(lm):
                    self.lineas.clear()

                # ⚙️ Botones por zonas
                if self.frame_count % self.cooldown != 0:
                    continue

                if self.sprint_state.modo_seleccion:
                    if 10 <= x_index <= 200 and 10 <= y_index <= 50:
                        self.sprint_state.eliminar_tarea()
                    elif 220 <= x_index <= 360 and 10 <= y_index <= 50:
                        self.sprint_state.iniciar_edicion()

                # 🔄 Toggle dibujo/selección
                if 380 <= x_index <= 520 and 10 <= y_index <= 50:
                    self.sprint_state.toggle_modo_dibujo()

                # ➕ Crear tarea
                if 540 <= x_index <= 700 and 10 <= y_index <= 50:
                    self.sprint_state.iniciar_creacion()

                # 🧹 Limpiar dibujo (botón)
                if self.sprint_state.modo_dibujo and 720 <= x_index <= 860 and 10 <= y_index <= 50:
                    self.lineas.clear()

                # ☝️ Seleccionar tarea
                if self.sprint_state.modo_seleccion and 100 <= y_index <= 100 + len(self.sprint_state.tareas) * 30:
                    index = (y_index - 100) // 30
                    tareas = list(self.sprint_state.tareas.keys())
                    if 0 <= index < len(tareas):
                        self.sprint_state.seleccionada = tareas[index]

        # ✍️ Dibuja las líneas
        if self.sprint_state.modo_dibujo:
            for pt1, pt2 in self.lineas:
                cv2.line(frame, pt1, pt2, (255, 255, 0), 3)

            # 🧹 Botón "Limpiar"
            cv2.rectangle(frame, (720, 10), (860, 50), (0, 0, 100), -1)
            cv2.putText(frame, "Limpiar", (730, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame
