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

        self.to_be_ack = []

    def run(self):
        """
        """
        while not self.event.is_set():
            start_time = time.time()
            if self.serial_interface.isReady:
                ack_id = self.serial_interface.serial_write(COMMAND_TYPES.get("Analog read"), "")
                if len(self.to_be_ack) > 4:
                    # 5 Values not acknowledged...
                    self.event.set()
                    tkMessageBox.showerror("Acknowledge error", "PIC seems not available, check connection...")
                else:
                    self.to_be_ack.append(ack_id)
            time_delta = time.time() - start_time
            if time_delta < self.write_interval:
                time.sleep(self.write_interval - time_delta)

    def acknowledge(self, id):
        print "To be ack: {}".format(id)
        print "Ack list: {}".format(self.to_be_ack)
        try:
            if int(id) in self.to_be_ack:
                self.to_be_ack.remove(int(id))
            else:
                pass
        except ValueError as e:
            tkMessageBox.showerror("Acknowledge error", "PIC acknowledged faulty... \n Error: "+e.message)