from Tkinter import *


class SettingsPanel(Frame):
    def __init__(self, master, info_panel, *args, **kwargs):
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

        if info_panel is not None:
            self.info_panel = info_panel
            self.uart_settings_btn.bind("<Enter>", lambda event:self.display_info(event, 'Uart settings.'))
            self.uart_settings_btn.bind("<Leave>", lambda event:self.display_info(event, ''))
            self.pid_settings_btn.bind("<Enter>", lambda event:self.display_info(event, 'PID settings.'))
            self.pid_settings_btn.bind("<Leave>", lambda event:self.display_info(event, ''))
            self.graph_settings_btn.bind("<Enter>", lambda event:self.display_info(event, 'Graph settings.'))
            self.graph_settings_btn.bind("<Leave>", lambda event:self.display_info(event, ''))

    def display_info(self, event, arg):
        if self.info_panel is not None:
            self.info_panel.set_info(arg)