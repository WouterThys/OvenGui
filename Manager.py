import threading
import Queue
import tkMessageBox

from my_serial.WriteThread import WriteThread
from pid.PID import PID
from my_serial.SerialInterface import SerialInterface
from gui.MainScreen import MainScreen
from my_serial.ReadThread import ReadThread
from utils.Utils import digital_to_temp

TIME_INTERVAL = 1 # Time interval in seconds

class Manager:
    """
    Launch the main part of the GUI and the worker thread. periodic_call and end_application could reside in the GUI
    part, but putting them here means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main (original) thread of the application, which will
        later be used by the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create local instances
        self.my_serial = SerialInterface()
        self.my_serial.configure_serial()

        # Variables
        self.door_state = 'C'  # State of the door, open ('O') or closed ('C')
        self.state = 'N'  # State of the Finite State Machine
        self.heater = 'OFF'
        self.fan = 'OFF'
        self.first_write = True

        # PID values
        self.pid = PID()
        self.pid.configure_pid()
        self.cnt = 0
        self.temp_real = 0
        self.temp_target = []

        # Create the queue and event
        self.read_queue = Queue.Queue()
        self.read_event = threading.Event()
        self.write_event = threading.Event()
        self.last_message = None
        # Set up the GUI
        self.gui = MainScreen(master,  self, TIME_INTERVAL, self.end_application)

        # Set up the threads to do asynchronous I/O.
        self.reading_thread = ReadThread(self.read_event, self.read_queue, self.my_serial)
        self.reading_thread.setDaemon(True)
        self.reading_thread.start()
        self.writing_thread = WriteThread(self.write_event, self.my_serial, TIME_INTERVAL)
        self.writing_thread.setDaemon(True)

        # Start the periodic call in the GUI to check if the queue contains anything, start serial
        self.periodic_call()

    def periodic_call(self):
        """
        Check every 200 ms if there is something new in the queue
        """
        self.do_logic()
        self.gui.process_incoming()
        if self.read_event.is_set():
            # This is the brutal stop of the system. Maybe do some cleanup before actually shutting down
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def do_logic(self):
        # Check if threads and inputs
        if self.write_event.is_set():
            self.gui.forced_stop()
        else:
            if self.door_state == 'O':
                self.gui.forced_stop()
                self.write_event.set()
        if self.read_event.is_set():
            self.gui.forced_stop()

        # Check input messages
        while self.read_queue.qsize():
            try:
                self.last_message = self.read_queue.get(0)
                if self.last_message.type == "message":
                    if self.last_message.command == "AR":
                        val = self.last_message.message
                        try:
                            self.temp_real = float(val)
                            self.temp_real = digital_to_temp(self.temp_real)
                            self.pid.set_point = self.temp_target[self.cnt]  # Point it should be
                            self.cnt += 1
                            pid_output = self.pid.do_work(self.temp_real)
                            self.gui.graph.append_graph(self.temp_real, pid_output)
                        except ValueError:
                            pass

                    elif self.last_message.command == "DL":
                        self.door_state = self.last_message.message

                    else:
                        pass
                elif self.last_message.type == "ack":
                    self.my_serial.acknowledge(self.last_message.message)
                    pass
                else:
                    pass
            except Queue.Empty:
                pass

        # Handle PID values
        if self.pid.output > 0:
            self.heater = 'ON'
            self.fan = 'OFF'
        elif self.pid.output < 0:
            self.heater = 'OFF'
            self.fan = 'ON'
        else:
            self.heater = 'OFF'
            self.fan = 'OFF'

        self.writing_thread.set_heat_and_fan(self.heater, self.fan)

    def start_writing_thread(self):
        self.my_serial.write_buffer = []
        self.my_serial.can_write = True
        self.my_serial.ack_id = 0
        if not self.write_event.is_set:
            self.writing_thread.start()
        else:
            self.write_event.clear()
            self.writing_thread = WriteThread(self.write_event, self.my_serial, TIME_INTERVAL)
            self.writing_thread.setDaemon(True)
            self.writing_thread.start()

    def stop_writing_thread(self):
        self.write_event.set()
        self.writing_thread.join(5)

    def end_application(self):
        self.my_serial.serial_write("CD", "")
        self.master.quit()
        self.read_event.set()
        self.reading_thread.join(5)
        if not self.write_event.is_set:
            self.write_event.set()
            self.writing_thread.join(5)
        self.my_serial.serial_destroy()