# 휴머노이드 로봇 통신을 위한 Native APP
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

YOLOv5의 실시간 객체 인식을 이용한 Native app이다.<br>
현재는 실시간 객체 인식 START(카메라 연결), STOP(카메라 정지), Serial 통신 CONNECT(연결), DISCONNECT(연결 해제)의 4가지 기능을 구현한다. <br>
<br>
!Update 실시간 스트림 영상에서 사람을 인지하면 로봇이 인사하는 기능을 추가했다. <br>

## 실행 방법
1. conda 가상환경 제작
2. 환경 세팅
   ``` pip install -r requirements.txt ```
3. YOLOv5 clone
   ``` git clone https://github.com/ultralytics/yolov5 ```
4. `app.py` 파일 실행

## 기능
1. **START DETECTION** : 카메라를 연결하고, Object Detection을 실시한다.
  - 'Person'이 감지되면 보라색 바운딩 박스가 나타난다.
  - 로봇과 통신 연결되었을 때, 사람이 감지되면 로봇이 인사한다. 
2. **STOP DETECTION** : 카메라 화면과 Detection을 정지한다.
3. **CONNECT** : 로봇과 통신을 연결한다.
4. **DISCONNECT** : 로봇과 통신을 해제한다.

## 실행 화면
![image](https://github.com/kingodjerry/yolov5_nativeapp/assets/143167244/0af9701d-e5c3-47cf-a6e5-558ee6bc87f4)
![image](https://github.com/kingodjerry/yolov5_nativeapp/assets/143167244/461851ae-f106-444e-adf3-324a83dc1574)

