import tkMessageBox
from Tkinter import *


class SaveAndSetPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.default_bg = self.cget('bg')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Title
        title_lbl = Label(self, text="Save graph", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=2)

        Label(self, text="Name: ", fg="dim gray").grid(row=1, column=0, sticky='ew')
        self.graph_name_ent = Entry(self)
        self.graph_name_ent.grid(row=1, column=1, sticky='ew')

        self.save_btn = Button(self, text="Save")
        self.save_btn.grid(row=2, column=1, sticky='nsew')

        self.set_btn = Button(self, text="Set")
        self.set_btn.grid(row=2, column=0, sticky='nsew')

    def get_graph_name(self):
        return self.graph_name_ent.get()