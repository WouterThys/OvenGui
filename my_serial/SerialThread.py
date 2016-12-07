""" serial thread file to handle serial connection.
Author: Vincent De Haen
Date: 07/12/2016"""
import threading
import time
from SerialUart import PICMessage, SerialInterface

RETRY_TIME = 0.1
SEND_TIME = 10

class SerialThread(threading.Thread):
    """ Class handeling serial connection to pic"""
    def __init__(self, event, queue ):
        """

        :param event:
        :param queue:
        """
        threading.Thread.__init__(self)
        self.serial_interface = SerialInterface()
        self.event = event
        self.queue = queue

    def run(self):
        """
        """
        count = 0
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.serial_has_input() > 0:
                msg = self.serial_interface.serial_read()
                message = PICMessage("Compy")
                if message.convert(msg) > 0:
                    self.queue.put(message)

            time_delta = time.time()-start_time
            if time_delta < RETRY_TIME:
                time.sleep(RETRY_TIME-time_delta)
            count += 1
            if count >= SEND_TIME:
                # send a command to pic
                self.serial_interface.serial_write("AR","")
                count = 0