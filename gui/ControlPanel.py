from Tkinter import *


class ControlPanel(Frame):
    def __init__(self, master=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        title_lbl = Label(self, text="Control", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.pack(side=TOP, fill=X)

        self.start_btn = Button(self, text="START", command=self.on_start_btn_click)
        self.start_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.stop_btn = Button(self, text="STOP", command=self.on_stop_btn_click)
        self.stop_btn.pack(side=TOP, fill=BOTH, expand=1)

        self.graph_btn = Button(self, text="Graph", command=self.on_graph_btn_click)
        self.graph_btn.pack(side=TOP, fill=BOTH, expand=1)

    """
    Button click events
    """
    def on_start_btn_click(self):
        print "start"

    def on_stop_btn_click(self):
        print "stop"

    def on_graph_btn_click(self):
        print "graph"

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