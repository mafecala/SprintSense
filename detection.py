# detection.py
from ultralytics import YOLO

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect_person(self, frame):
        results = self.model(frame, verbose=False)[0]
        for box in results.boxes:
            cls = int(box.cls[0])
            if self.model.names[cls] == "person":
                return True
        return False
