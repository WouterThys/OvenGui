from Tkinter import *


class FeedBackPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        title_lbl = Label(self, text="Values", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=3)