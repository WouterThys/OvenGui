from Tkinter import *


class ControlPanel(Frame):
    def __init__(self, master=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        title_lbl = Label(self, text="Control", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.pack(side=TOP, fill=X)

        self.start_btn = Button(self, text="START")
        self.start_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.stop_btn = Button(self, text="STOP")
        self.stop_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.graph_btn = Button(self, text="Graph")
        self.graph_btn.pack(side=TOP, fill=BOTH, expand=1)

    """
    Useful functions for this frame
    """
    def enable_start_btn(self, enable):
        if enable:
            self.start_btn.config(state=NORMAL)
        else:
            self.start_btn.config(state=DISABLED)

    def enable_stop_btn(self, enable):
        if enable:
            self.stop_btn.config(state=NORMAL)
        else:
            self.stop_btn.config(state=DISABLED)

    def enable_graph_btn(self, enable):
        if enable:
            self.graph_btn.config(state=NORMAL)
        else:
            self.graph_btn.config(state=DISABLED)

            # # options for buttons
            # 10
            # button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
            # 11
            # 12  # define buttons
            # 13
            # Tkinter.Button(self, text='askopenfile', command=self.askopenfile).pack(**button_opt)
            # 14
            # Tkinter.Button(self, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)
            # 15
            # Tkinter.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
            # 16
            # Tkinter.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)
            # 17
            # Tkinter.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)