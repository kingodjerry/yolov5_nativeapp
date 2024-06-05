import serial

class RobotController:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = serial.Serial(port, baud_rate)
        print(f"Connected to {self.port} at {self.baud_rate} baud rate.")

    def disconnect(self):
        self.serial_connection.close()
        print("Disconnected from robot.")

    def robotAction(self, no):
        # 로봇을 움직이는 프로토콜에 의해 명령을 전달
        exeCmd = bytearray([0xff, 0xff, 0x4c, 0x53, 0x00,
                            0x00, 0x00, 0x00, 0x30, 0x0c, 0x03,
                            0x01, 0x00, 100, 0x00])  # 명령어 샘플
        exeCmd[11] = no
        exeCmd[14] = 0x00  # checksum
        
        for i in range(6, 14):
            exeCmd[14] += exeCmd[i]
        
        self.serial_connection.write(exeCmd)
        print(f"Command sent: {exeCmd}")
