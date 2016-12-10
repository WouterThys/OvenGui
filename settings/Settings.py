import serial


class Settings:
    def __init__(self):
        self.serial_settings = SerialSettings()
        self.window_settings = WindowSettings()


class SerialSettings:
    def __init__(self):
        self.com_port ='/dev/ttyUSB0'
        self.baud_rate = serial.Serial.BAUDRATES[12]
        self.data_bits = serial.Serial.BYTESIZES[3]
        self.stop_bits = serial.Serial.STOPBITS[0]
        self.parity = serial.Serial.PARITIES[0]


class WindowSettings:
    def __init__(self):
        self.width = 900