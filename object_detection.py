import torch
import cv2

# windows path error 해결 코드
import pathlib
pathlib.PosixPath = pathlib.WindowsPath

class ObjectDetector:
    def __init__(self, model_path):
        self.model = torch.hub.load('./yolov5', 'custom', path=model_path, source='local')
        self.model.eval()

    def detect_objects(self, frame):
        results = self.model(frame)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cords

    def draw_boxes(self, frame, labels, cords):
        n = len(labels)
        for i in range(n):
            row = cords[i]
            if row[4] >= 0.2:  # confidence threshold
                x1, y1, x2, y2 = int(row[0] * frame.shape[1]), int(row[1] * frame.shape[0]), int(row[2] * frame.shape[1]), int(row[3] * frame.shape[0])
                # 사람 감지
                if self.model.names[int(labels[i])] == 'person':
                    bgr = (255, 71, 151) 
                else:
                    bgr = (255, 255, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, f'{self.model.names[int(labels[i])]} {row[4]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame
