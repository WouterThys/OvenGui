""" serial thread file to handle serial connection.
Author: Vincent De Haen
Date: 07/12/2016"""
import threading
import time
from PICClasses import PICMessage


class ReadThread(threading.Thread):
    """ Class handling serial connection to pic"""
    def __init__(self, event, queue, serial_interface, read_interval=0.1):
        """

        :param event:
        :param queue:
        """
        threading.Thread.__init__(self)
        self.serial_interface = serial_interface
        self.event = event
        self.queue = queue
        self.read_interval = read_interval

    def run(self):
        """
        """
        # count = 0
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.is_ready:
                if self.serial_interface.serial_has_input() > 0:
                    msg = self.serial_interface.serial_read()
                    message = PICMessage("Compy")
                    if message.convert(msg) > 0:
                        self.queue.put(message)

            time_delta = time.time()-start_time
            if time_delta < self.read_interval:
                time.sleep(self.read_interval - time_delta)