from Tkinter import *


class BottomPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        content_frame = Frame(self, bd=1, relief=SUNKEN, padx=1, pady=1)
        content_frame.grid(sticky='nsew')

        self.info_txt = StringVar()
        self.info_lbl = Label(content_frame, textvariable=self.info_txt, fg='dim gray')\
            .pack(side=LEFT, fill=X)
        self.name_lbl = Label(content_frame, text='All rights reserved, Vonny and Waldo productions', fg='dim gray')\
            .pack(side=RIGHT, fill=X)

        self.info_txt.set(" ")

    def set_info(self, text):
        self.info_txt.set(str(text))