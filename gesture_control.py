import cv2
import mediapipe as mp

class GestureController:
    def __init__(self, sprint_state):
        self.sprint_state = sprint_state
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.frame_count = 0
        self.cooldown = 15

    def process_frame(self, frame):
        self.frame_count += 1
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                index_tip = hand.landmark[8]
                x = int(index_tip.x * w)
                y = int(index_tip.y * h)
                cv2.circle(frame, (x, y), 12, (0, 255, 255), -1)

                if self.frame_count % self.cooldown != 0:
                    continue

                if self.sprint_state.modo_seleccion:
                    if 10 <= x <= 200 and 10 <= y <= 50:
                        self.sprint_state.eliminar_tarea()
                    elif 220 <= x <= 360 and 10 <= y <= 50:
                        self.sprint_state.iniciar_edicion()

                if 380 <= x <= 520 and 10 <= y <= 50:
                    self.sprint_state.toggle_modo_dibujo()

                if 540 <= x <= 700 and 10 <= y <= 50:
                    self.sprint_state.iniciar_creacion()

                if self.sprint_state.modo_seleccion and 100 <= y <= 100 + len(self.sprint_state.tareas) * 30:
                    index = (y - 100) // 30
                    tareas = list(self.sprint_state.tareas.keys())
                    if 0 <= index < len(tareas):
                        self.sprint_state.seleccionada = tareas[index]

        return frame
