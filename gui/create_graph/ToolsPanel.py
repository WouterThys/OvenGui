from Tkinter import *


class ToolsPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.default_bg = self.cget('bg')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # Title
        title_lbl = Label(self, text="Tools", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=3, sticky='ew')

        Label(self, text="Time axis:", fg="dim gray").grid(row=1, column=0, sticky='ew')
        Label(self, text="Temp. axis:", fg="dim gray").grid(row=1, column=1, sticky='ew')

        self.x_lim_txt = StringVar()
        self.y_lim_txt = StringVar()
        self.x_lim_ent = Entry(self, textvariable=self.x_lim_txt, justify=CENTER, width=8)
        self.x_lim_ent.grid(row=2, column=0, sticky='ew')
        self.y_lim_ent = Entry(self, textvariable=self.y_lim_txt, justify=CENTER, width=8)
        self.y_lim_ent.grid(row=2, column=1, sticky='ew')

        self.set_axes_btn = Button(self, text="Set")
        self.set_axes_btn.grid(row=2, column=2, sticky='nsew')

        Label(self, text="Text: ", fg="dim gray").grid(row=3, column=0, sticky='ew')
        self.text_txt = StringVar()
        self.text_ent = Entry(self, textvariable=self.text_txt)
        self.text_ent.grid(row=4, column=0, columnspan=2, sticky='ew')

        self.add_text_btn = Button(self, text="Add")
        self.add_text_btn.grid(row=4, column=2, sticky='nsew')

        self.add_txt = StringVar()
        Label(self, textvariable=self.add_txt, fg="dim gray").grid(row=5, column=0, columnspan=3, sticky='ew')
