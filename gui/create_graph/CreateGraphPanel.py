import tkMessageBox
import numpy as np
from Tkinter import *
from matplotlib.lines import Line2D
from errors.Errors import InvalidPointsException
from gui.GraphPanel import GraphPanel
from gui.create_graph.PointPanel import PointPanel


class CreateGraphWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=FLAT, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Graph
        self.graph = GraphPanel(self)
        self.graph.grid(row=0,rowspan=3,column=0,sticky='nsew')

        def on_pick_event(event):
            if isinstance(event.artist, Line2D):
                this_line = event.artist
                x_data = this_line.get_xdata()
                y_data = this_line.get_ydata()
                ind = event.ind
                self.point_panel.set_xy_values(str(np.take(x_data, ind)[0]), str(np.take(y_data, ind)[0]))
        self.graph.canvas.mpl_connect('pick_event', on_pick_event)

        # Point panel
        self.point_panel = PointPanel(self)
        self.point_panel.add_btn.configure(command=self.on_add_btn_click)
        self.point_panel.del_btn.configure(command=self.on_delete_btn_click)
        self.point_panel.grid(row=0,column=1, sticky='nsew')

        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())

    """
    Events
    """
    def on_add_btn_click(self):
        xy = self.point_panel.get_xy_values()
        if xy is not None:
            self.graph.set_point(xy[0], xy[1])
            self.point_panel.clear_entries()

    def on_delete_btn_click(self):
        try:
            xy = self.point_panel.get_xy_values()
            if xy is not None:
                self.graph.delete_point(xy[0],xy[1])
                self.point_panel.clear_entries()
        except InvalidPointsException as e:
            tkMessageBox.showerror("Error", e.message)


