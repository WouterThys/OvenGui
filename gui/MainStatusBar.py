from Tkinter import *
import time

class StatusBar:
    def __init__(self, master):
        self.status = Label(master, text="", bd=2, relief=SUNKEN, anchor=W)

    def get_status_bar(self):
        return self.status

    def put_status_message(self, msg):
        self.status.config(text=msg)
        # time.sleep(1)
        # self.status.config(text="")