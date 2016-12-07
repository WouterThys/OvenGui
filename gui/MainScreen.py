import Queue
import random
import threading
from Tkinter import *

import MainMenu
from gui.Dialogs import PicInfoDialog
from gui.graphs import Graph
from my_serial import SerialThread
from my_serial.SerialUart import SerialInterface, PICMessage, PICInfo
from settings.Settings import Settings


class MainScreen:
    def __init__(self, master, queue, settings, serial, end_command):
        self.master = master
        self.queue = queue
        self.serial = serial
        self.pic_info = PICInfo
        # Set up the main menu
        MainMenu.MainMenu(master, settings, serial, end_command)
        # Window settings
        self.master.minsize(width=400, height=400)
        self.master.wm_title("Oven")

        graph_frame = Frame(master)
        button_frame = Frame(master)
        graph_frame.pack(side=LEFT, fill=BOTH)
        button_frame.pack(side=RIGHT, fill=BOTH)

        # Buttons
        self.pic_info_btn = Button(button_frame, text="PIC Info", state=DISABLED, command=self.show_pic_info)
        self.pic_info_btn.pack(side=TOP, fill=X)
        #
        self.pic_awake_btn = Button(button_frame, text="Wake PIC", command=self.send_get_name_request)
        self.pic_awake_btn.pack(side=TOP, fill=X)
        # Graph
        self.graph = Graph(graph_frame)

        # Set up status bar
        # self.status = StatusBar(master)
        # self.status.get_status_bar().pack(side=BOTTOM)
        # self.status.put_status_message("Initializing")

    def process_incoming(self):
        """
        Handle all the messages currently in the queue (if any)
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check the contents of the message and so something with it
                #self.status.put_status_message("Message from: "+msg.sender)
                self.handle_message(msg)
            except Queue.Empty:
                pass

    def show_pic_info(self):
        PicInfoDialog(self.master, self.pic_info)

    def send_analog_read_request(self):
        self.serial.serial_write("AR", "abc")

    def send_get_name_request(self):
        self.serial.serial_write("GN", "abc")

    def handle_message(self, message):
        if message.type == "ack":
            self.pic_info = message.pic_info
            self.pic_info_btn["state"] = "normal"
        else:
            if message.command == "AR":
                self.do_logic(message.message)
            else:
                pass

    def do_logic(self, val):
        try:
            val = int(val)
        except ValueError:
            pass

        pass


class ThreadedClient:
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
        self.thread1 = SerialThread.SerialThread(self.event, self.queue)
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
        if not self.event.is_set():
            # This is the brutal stop of the system. Maybe do some cleanup before actually shutting down
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.serial.serial_destroy()
        self.master.quit()
        self.event.set()
        self.thread1.join(5)

rand = random.Random()
root = Tk()
client = ThreadedClient(root)
root.mainloop()


