import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from object_detection import ObjectDetector
from robot_controller import RobotController

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('./resources/ui.ui', self)

        self.setWindowTitle('robot controller')

        # 버튼에 대한 클릭 이벤트 핸들러 연결
        self.connectButton.clicked.connect(self.connect_robot)
        self.disconnectButton.clicked.connect(self.disconnect_robot)
        self.startButton.clicked.connect(self.start_detection)
        self.stopButton.clicked.connect(self.stop_detection)

        self.running = False
        self.object_detector = None
        self.detecting = False
        self.cap = None  # 카메라를 아직 열지 않음
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()  # 프레임 읽어오기
            if not ret:
                print("Error: Cannot grab frame")
                return
            if self.detecting and self.object_detector is not None:
                labels, cords = self.object_detector.detect_objects(frame)
                frame = self.object_detector.draw_boxes(frame, labels, cords)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV에서 PyQt로 이미지 전환
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.imageBox.setPixmap(QPixmap.fromImage(image))  # imageBox에 이미지 표시

    def connect_robot(self):
        self.robot_controller.connect()
        print("Robot connected")

    def disconnect_robot(self):
        self.robot_controller.disconnect()
        print("Robot disconnected")

    def start_detection(self):
        if not self.running:
            self.cap = cv2.VideoCapture(cv2.CAP_DSHOW)  # 카메라 연결
            if not self.cap.isOpened():
                print("Error: Cannot open camera")
                return
            self.object_detector = ObjectDetector('./yolov5s.pt')  # 모델 파일 경로 설정
            self.detecting = True
            self.running = True
            self.timer.start(10)  # 타이머 시작
            print("Object detection started")

    def stop_detection(self):
        if self.running:
            self.timer.stop()  # 타이머 중지
            self.detecting = False
            self.running = False
            if self.cap is not None:
                self.cap.release()
                self.cap = None
        print("Object detection stopped")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())
