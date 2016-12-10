import threading
import time

WRITE_INTERVAL = 2  # Write interval in seconds


class WriteThread(threading.Thread):
    """ Class handling serial connection to pic"""
    def __init__(self, event, serial_interface):
        """

        :param event:
        """
        threading.Thread.__init__(self)
        self.serial_interface = serial_interface
        self.event = event

    def run(self):
        """
        """
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.isReady:
                self.serial_interface.serial_write("AR", "")
            time_delta = time.time() - start_time
            if time_delta < WRITE_INTERVAL:
                time.sleep(WRITE_INTERVAL - time_delta)