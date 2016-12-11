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

    def run(self):
        """
        """
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.isReady:
                self.serial_interface.serial_write(COMMAND_TYPES.get("Analog read"), "")
            time_delta = time.time() - start_time
            if time_delta < self.write_interval:
                time.sleep(self.write_interval - time_delta)