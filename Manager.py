import threading
import Queue

from my_serial.WriteThread import WriteThread
from pid.PID import PID
from settings.Settings import Settings
from my_serial.SerialInterface import SerialInterface
from gui.MainScreen import MainScreen
from my_serial.ReadThread import ReadThread

TIME_INTERVAL = 1 # Time interval in seconds

TARGET_Y = []
TARGET_X = []
for i in range(0,350):
    TARGET_X.append(i)
    if i < 110:
        TARGET_Y.append((180.0/110.0)*float(i))
    if (i >= 110) and (i < 200):
        TARGET_Y.append(180)
    if (i >= 200) and (i < 250):
        TARGET_Y.append((120.0/50.0)*(float(i)-200) + 180)
    if (i >= 250) and (i < 260):
        TARGET_Y.append(300)
    if i >= 260:
        TARGET_Y.append(TARGET_Y[-1]-2)

target = (TARGET_X, TARGET_Y)
print TARGET_Y


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
        self.my_settings = Settings()
        self.serial = SerialInterface()
        self.serial.configure_serial(self.my_settings.serial_settings)

        # PID values
        self.kp = 20
        self.ki = 0.005
        self.kd = 0.01
        self.pid = PID(self.kp, self.ki, self.kd)
        self.pid.dt = TIME_INTERVAL
        self.cnt = 0
        self.temp_real = 0

        # Create the queue and event
        self.queue = Queue.Queue()
        self.read_event = threading.Event()
        self.write_event = threading.Event()
        # Set up the GUI
        self.gui = MainScreen(master, self.my_settings, self.serial, self, self.end_application)

        # Set up the threads to do asynchronous I/O.
        self.reading_thread = ReadThread(self.read_event, self.queue, self.serial)
        self.reading_thread.setDaemon(True)
        self.reading_thread.start()

        self.writing_thread = WriteThread(self.write_event, self.serial)
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
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if msg.command == "AR":
                    val = msg.message
                    try:
                        self.temp_real = float(val)
                        self.temp_real = self.digital_to_temp(self.temp_real)
                        self.pid.set_point = TARGET_Y[self.cnt]  # Point it should be
                        self.cnt += 1
                        pid_output = self.pid.do_work(self.temp_real)
                        self.gui.graph.update(self.temp_real, pid_output)
                    except ValueError:
                        pass
                else:
                    pass
            except Queue.Empty:
                pass

    def digital_to_temp(self, value):
        return value/10

    def start_reading_thread(self):
        self.writing_thread.start()

    def stop_reading_thread(self):
        self.write_event.set()
        self.writing_thread.join(5)

    def end_application(self):
        self.serial.serial_destroy()
        self.master.quit()
        self.read_event.set()
        self.reading_thread.join(5)
        if not self.write_event.is_set:
            self.write_event.set()
            self.writing_thread.join(5)