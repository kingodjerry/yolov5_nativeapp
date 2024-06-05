import sys
import cv2
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from object_detection import ObjectDetector
from robot_controller import RobotController

class Controller_app(QMainWindow):
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
        self.robot_controller = None  # 로봇 컨트롤러 속성 추가

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
        port = 'COM7'
        baud_rate = 115200
        self.robot_controller = RobotController(port, baud_rate)  # 로봇 컨트롤러 인스턴스 생성
        self.robot_controller.connect()  # 로봇 컨트롤러 연결
        print("Robot connected")

    def disconnect_robot(self):
        if self.robot_controller is not None:
            self.robot_controller.disconnect()  # 로봇 컨트롤러 연결 해제
        print("Robot disconnected")

    def start_detection(self):
        print("Camera Connecting ...")
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

            # 사람 감지할 때 로봇 인사
            self.timer.timeout.connect(self.person_detection)

    def stop_detection(self):
        if self.running:
            self.timer.stop()  # 타이머 중지
            self.detecting = False
            self.running = False
            if self.cap is not None:
                self.cap.release()
                self.cap = None
        print("Object detection stopped")

    def person_detection(self):
        if self.detecting and self.object_detector is not None:
            ret, frame = self.cap.read()  # 프레임 읽어오기
            if not ret:
                print("Error: Cannot grab frame")
                return
            labels, cords = self.object_detector.detect_objects(frame)
            for i in range(len(labels)):
                if self.object_detector.model.names[int(labels[i])] == 'person':
                    print("사람 감지! 인사합니다.")
                    self.robot_controller.robotAction(19)
                    time.sleep(10)
                    break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller_app()
    window.show()
    sys.exit(app.exec_())
