from Tkinter import *


class ControlPanel(Frame):
    def __init__(self, master=None, info_panel=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        title_lbl = Label(self, text="Control", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.pack(side=TOP, fill=X)

        btn_pack_opt = {'side': TOP, 'fill': BOTH, 'expand': 1}

        self.start_btn = Button(self, text="START")
        self.start_btn.pack(**btn_pack_opt)

        self.stop_btn = Button(self, text="STOP")
        self.stop_btn.pack(**btn_pack_opt)

        self.graph_btn = Button(self, text="Graph")
        self.graph_btn.pack(**btn_pack_opt)

        self.info_panel = info_panel

    """
    Useful functions for this frame
    """
    def enable_start_btn(self, enable):
        if enable:
            self.start_btn.config(state=NORMAL)
            self.start_btn.unbind("<Enter>")
            self.start_btn.unbind("<Leave>")
            self.start_btn.bind("<Enter>", lambda event: self.display_info(event, 'Start sampling.'))
            self.start_btn.bind("<Leave>", lambda event: self.display_info(event, ''))
        else:
            self.start_btn.config(state=DISABLED)
            self.start_btn.unbind("<Enter>")
            self.start_btn.unbind("<Leave>")
            self.start_btn.bind("<Enter>", lambda event: self.display_info(event, 'Select a graph to start.'))
            self.start_btn.bind("<Leave>", lambda event: self.display_info(event, ''))

    def enable_stop_btn(self, enable):
        if enable:
            self.stop_btn.config(state=NORMAL)
            self.stop_btn.unbind("<Enter>")
            self.stop_btn.unbind("<Leave>")
            self.stop_btn.bind("<Enter>", lambda event: self.display_info(event, 'Stop sampling.'))
            self.stop_btn.bind("<Leave>", lambda event: self.display_info(event, ''))
        else:
            self.stop_btn.config(state=DISABLED)
            self.stop_btn.unbind("<Enter>")
            self.stop_btn.unbind("<Leave>")
            self.stop_btn.bind("<Enter>", lambda event: self.display_info(event, 'Select a graph and select start before you can stop.'))
            self.stop_btn.bind("<Leave>", lambda event: self.display_info(event, ''))

    def enable_graph_btn(self, enable):
        if enable:
            self.graph_btn.config(state=NORMAL)
            self.graph_btn.unbind("<Enter>")
            self.graph_btn.unbind("<Leave>")
            self.graph_btn.bind("<Enter>", lambda event: self.display_info(event, 'Select a graph.'))
            self.graph_btn.bind("<Leave>", lambda event: self.display_info(event, ''))
        else:
            self.graph_btn.config(state=DISABLED)
            self.graph_btn.unbind("<Enter>")
            self.graph_btn.unbind("<Leave>")
            self.graph_btn.bind("<Enter>", lambda event: self.display_info(event, 'First stop sampling.'))
            self.graph_btn.bind("<Leave>", lambda event: self.display_info(event, ''))

    """
    Info of the widgets
    """
    def add_info_to_widgets(self):
        pass

    def display_info(self, event, arg):
        if self.info_panel is not None:
            self.info_panel.set_info(arg)