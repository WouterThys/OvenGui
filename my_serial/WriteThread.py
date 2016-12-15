import threading
import time
import tkMessageBox
from PICClasses import COMMAND_TYPES, MESSAGE_TYPES


class WriteThread(threading.Thread):
    """ Class handling serial connection to pic"""
    def __init__(self, event, serial_interface, write_interval=1):
        """

        :param event:
        """
        threading.Thread.__init__(self)
        self.serial_interface = serial_interface
        self.event = event
        self.write_interval = write_interval

        self.heater = 'OFF'
        self.fan = 'OFF'

        self.message = []
        self.command = []

    def run(self):
        """
        """
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.isReady:
                self.command.append(COMMAND_TYPES.get("Analog read"))
                self.message.append("")

                self.command.append("HE")
                self.message.append(self.heater)

                self.command.append("FA")
                self.message.append(self.fan)

                self.serial_interface.serial_write_block(self.command, self.message, 3)

            time_delta = time.time() - start_time
            if time_delta < self.write_interval:
                time.sleep(self.write_interval - time_delta)

            del self.message[:]
            del self.command[:]

    def set_heat_and_fan(self, heater, fan):
        self.heater = heater
        self.fan = fan