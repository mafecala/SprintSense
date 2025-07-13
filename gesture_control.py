# gesture_control.py
import cv2
import mediapipe as mp
import time

class GestureController:
    def __init__(self, sprint_state):
        self.sprint_state = sprint_state
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

        self.drawing = mp.solutions.drawing_utils
        self.is_drawing = False
        self.drawing_points = []

    def process_frame(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        h, w, _ = frame.shape
        overlay = frame.copy()

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            self.drawing.draw_landmarks(overlay, hand, self.mp_hands.HAND_CONNECTIONS)
            index = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            y = int(index.y * h)

            self.sprint_state.seleccionar_tarea_por_posicion(y)

            thumb = hand.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            dist = ((index.x - thumb.x)**2 + (index.y - thumb.y)**2)**0.5
            if dist < 0.05:  # gesto de pinza
                self.sprint_state.marcar_completada()

            # Dibujo con dedos
            ix, iy = int(index.x * w), int(index.y * h)
            if dist < 0.05:
                self.drawing_points.append((ix, iy))
                self.is_drawing = True
            else:
                self.is_drawing = False
                self.drawing_points.append(None)

        # Dibujar líneas
        for i in range(1, len(self.drawing_points)):
            pt1, pt2 = self.drawing_points[i - 1], self.drawing_points[i]
            if pt1 and pt2:
                cv2.line(overlay, pt1, pt2, (0, 255, 0), 3)

        return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
