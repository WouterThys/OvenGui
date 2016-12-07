import threading
import Queue
from settings.Settings import Settings
from my_serial.SerialInterface import SerialInterface
from gui.MainScreen import MainScreen
from my_serial.SerialThread import SerialThread


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
        self.settings = Settings()
        self.serial = SerialInterface()

        # Create the queue and event
        self.queue = Queue.Queue()
        self.event = threading.Event()
        # Set up the GUI
        self.gui = MainScreen(master, self.queue, self.settings, self.serial, self.end_application)

        # Set up the thread to do asynchronous I/O. (more should prolly be done here)
        self.thread1 = SerialThread(self.event, self.queue, self.serial)
        self.thread1.setDaemon(True)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains anything, start serial
        self.periodic_call()
        self.serial.configure_serial(self.settings)

    def periodic_call(self):
        """
        Check every 100 ms if there is something new in the queue
        """
        self.gui.process_incoming()
        if self.event.is_set():
            # This is the brutal stop of the system. Maybe do some cleanup before actually shutting down
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.serial.serial_destroy()
        self.master.quit()
        self.event.set()
        self.thread1.join(5)