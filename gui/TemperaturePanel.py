# -*- coding: utf-8 -*-
from Tkinter import *


class TemperaturePanel(Frame):
    def __init__(self, master=None, info_panel=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        title_lbl = Label(self, text="Temperature", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.temperature = 0.00
        self.temp_txt = StringVar()
        self.temp_lbl = Label(self, textvariable=self.temp_txt, font=("consolas", 80)).grid(row=1, column=0,sticky='nsew')
        self.temp_txt.set("...")
        self.unit_lbl = Label(self, text='°C', font=("consolas", 40)).grid(row=1, column=1, sticky='nsew')

        self.bind("<Enter>", lambda event: self.display_info(event,"Current temperature: {0:f} °C".format(
                                                                          self.temperature)))
        self.bind("<Leave>", lambda event: self.display_info(event, ''))

        self.info_panel = info_panel

    def set_temperature_value(self, temperature):
        self.temperature = temperature
        if temperature < 10:
            self.temp_txt.set("{0:.2f}".format(temperature))
        if (temperature >= 10) and (temperature < 100):
            self.temp_txt.set("{0:.1f}".format(temperature))
        if temperature >= 100:
            self.temp_txt.set("{0:.0f}".format(temperature))

    def display_info(self, event, arg):
        if self.info_panel is not None:
            self.info_panel.set_info(arg)
