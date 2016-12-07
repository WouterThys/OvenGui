import Queue
from Tkinter import *

import MainMenu
from gui.Dialogs import PicInfoDialog
from gui.graphs import Graph
from my_serial.PICClasses import PICInfo


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
            self.graph.update(float(val))
        except ValueError:
            pass

        pass



