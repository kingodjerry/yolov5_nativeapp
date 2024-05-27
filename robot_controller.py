import serial

class RobotController:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = serial.Serial(port, baud_rate)

    def connect(self):
        if not self.serial_connection.is_open:
            self.serial_connection.open()
        print(f"Connected to {self.port} at {self.baud_rate} baud rate.")

    def disconnect(self):
        if self.serial_connection.is_open:
            self.serial_connection.close()
        print("Disconnected from robot.")

