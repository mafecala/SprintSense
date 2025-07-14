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
        dedos.append(lm[4].x < lm[3].x)  # Pulgar
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

                if self.sprint_state.modo_dibujo and distancia < 40:
                    if self.prev_point:
                        self.lineas.append((self.prev_point, (x_index, y_index)))
                    self.prev_point = (x_index, y_index)
                    self.dibujando = True
                else:
                    self.prev_point = None
                    self.dibujando = False

                if self.sprint_state.modo_seleccion and distancia < 40 and self.sprint_state.seleccionada:
                    self.sprint_state.marcar_completada()

                if self.sprint_state.modo_dibujo and self.dedos_extendidos(lm):
                    self.lineas.clear()

                if self.frame_count % self.cooldown != 0:
                    continue

                if self.sprint_state.modo_seleccion:
                    if 10 <= x_index <= 200 and 10 <= y_index <= 50:
                        self.sprint_state.eliminar_tarea()
                    elif 220 <= x_index <= 360 and 10 <= y_index <= 50:
                        self.sprint_state.iniciar_edicion()

                if 380 <= x_index <= 520 and 10 <= y_index <= 50:
                    self.sprint_state.toggle_modo_dibujo()

                if 540 <= x_index <= 700 and 10 <= y_index <= 50:
                    self.sprint_state.iniciar_creacion()

                if self.sprint_state.modo_dibujo and 720 <= x_index <= 860 and 10 <= y_index <= 50:
                    self.lineas.clear()

                if self.sprint_state.modo_seleccion and 100 <= y_index <= 100 + len(self.sprint_state.tareas) * 50:
                    index = (y_index - 100) // 50
                    tareas = list(self.sprint_state.tareas.keys())
                    if 0 <= index < len(tareas):
                        self.sprint_state.seleccionada = tareas[index]

        if self.sprint_state.modo_dibujo:
            for pt1, pt2 in self.lineas:
                cv2.line(frame, pt1, pt2, (255, 255, 0), 3)

        return frame
