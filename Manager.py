import threading
import Queue

from fsm.FSM import FSM
from my_serial.SerialInterface import SerialInterface
from gui.MainScreen import MainScreen
from my_serial.ReadThread import ReadThread

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

        # Create the queue and event
        self.read_queue = Queue.Queue()
        self.read_event = threading.Event()
        self.last_message = None

        # Set up the threads to do asynchronous I/O.
        self.reading_thread = ReadThread(self.read_event, self.read_queue, self.my_serial)
        self.reading_thread.setDaemon(True)
        self.reading_thread.start()

        # The FSM
        self.fsm = FSM(self.my_serial)

        # Set up the GUI
        self.gui = MainScreen(master, self, TIME_INTERVAL, self.end_application)

        # Start the periodic call in the GUI to check if the queue contains anything, start serial
        self.periodic_call()

    def periodic_call(self):
        """
        Check every 200 ms if there is something new in the queue
        """
        self.check_queue()
        self.fsm.do_fsm_tick()
        self.gui.process_incoming()
        if self.read_event.is_set():
            # This is the brutal stop of the system. Maybe do some cleanup before actually shutting down
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def check_queue(self):
        # Check if thread is ok
        if self.read_event.is_set():
            self.gui.forced_stop()

        # Check input messages
        while self.read_queue.qsize():
            try:
                self.last_message = self.read_queue.get(0)
                if self.last_message.type == "message":
                    if self.last_message.command == "AR":
                        val = self.last_message.message
                        self.fsm.sensor_value = val

                    elif self.last_message.command == "DL":
                        door = self.last_message.message
                        if door == "O":
                            self.fsm.door_open_state = True
                        else:
                            self.fsm.door_open_state = False

                    elif self.last_message.command == "IN":
                        self.fsm.pic_initialized = True

                    else:
                        pass
                elif self.last_message.type == "ack":
                    self.my_serial.acknowledge(self.last_message.message)
                    pass
                else:
                    pass
            except Queue.Empty:
                pass

    def end_application(self):
        self.my_serial.serial_write("CD", "")
        self.master.quit()
        self.read_event.set()
        self.reading_thread.join(5)
        self.my_serial.serial_destroy()