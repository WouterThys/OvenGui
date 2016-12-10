from Tkinter import *


class SettingsPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        title_lbl = Label(self, text="Settings", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.pack(side=TOP, fill=X)

        self.uart_settings_btn = Button(self, text="Uart")
        self.uart_settings_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.pid_settings_btn = Button(self, text="Pid")
        self.pid_settings_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.graph_settings_btn = Button(self, text="Graph")
        self.graph_settings_btn.pack(side=TOP, fill=BOTH, expand=1)