import serial
import os
from yaml import load, dump

PATH = os.path.join(os.path.dirname(__file__),"")
PID_SETTINGS = "PIDSettings"
UART_SETTINGS = "UartSettings"


def read_settings(which):
    with open(PATH+'settings.yml', "r") as sets:
        sets_dict = load(sets)
        return sets_dict[which]

def write_settings(which, val):
    with open(PATH+'settings.yml', "r") as sets:
        sets_dict = load(sets)

    sets_dict[which] = val
    with open(PATH+'settings.yml', "w") as sets:
        dump(sets_dict, sets, default_flow_style=False)


class SerialSettings:
    def __init__(self):
        self.com_port ='/dev/ttyUSB0'
        self.baud_rate = serial.Serial.BAUDRATES[12]
        self.data_bits = serial.Serial.BYTESIZES[3]
        self.stop_bits = serial.Serial.STOPBITS[0]
        self.parity = serial.Serial.PARITIES[0]