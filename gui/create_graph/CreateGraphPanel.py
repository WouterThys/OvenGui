import tkMessageBox
import numpy as np
import os

from scipy.interpolate import interp1d
from Tkinter import *
from matplotlib.lines import Line2D
from matplotlib.text import Text
from errors.Errors import InvalidPointsException
from gui.BottomPanel import BottomPanel
from gui.GraphPanel import GraphPanel
from gui.create_graph.DrawLinePanel import DrawLinePanel
from gui.create_graph.PointPanel import PointPanel
from gui.create_graph.SaveAndSetPanel import SaveAndSetPanel
from gui.create_graph.ToolsPanel import ToolsPanel

PATH = os.path.join(os.path.dirname(__file__),"graphs/")


class CreateGraphWindow(Frame):
    def __init__(self, master, main_screen, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Variables
        master.wm_title("Create graph")
        self.main_screen = main_screen
        self.interpolated_x = []
        self.interpolated_y = []
        self.interpolated = False
        self.saved = False
        self.pick_event = False
        self.adding_text = False
        self.text_fields = []

        self.config(bd=1, relief=FLAT, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Bottom panel
        self.bottom_panel = BottomPanel(self)
        self.bottom_panel.grid(row=4, column=0, columnspan=2, sticky='ew')

        # Graph
        self.graph = GraphPanel(self, info_panel=self.bottom_panel, is_create_graph=True)
        self.xy_points = []
        self.create_line, = self.graph.axes.plot([], [], 'ro', picker=5)
        self.interpol_line, = self.graph.axes.plot([], [])
        self.graph.grid(row=0,rowspan=4,column=0,sticky='nsew')

        def on_pick_event(event):
            self.pick_event = True
            if isinstance(event.artist, Line2D):
                this_line = event.artist
                x_data = this_line.get_xdata()
                y_data = this_line.get_ydata()
                ind = event.ind
                self.point_panel.set_xy_values(str(np.take(x_data, ind)[0]), str(np.take(y_data, ind)[0]))
            if isinstance(event.artist, Text):
                this_text = event.artist
                if this_text in self.text_fields:
                    self.text_fields.remove(this_text)
                this_text.remove()
                self.graph.canvas.draw()

            return True
        self.graph.canvas.mpl_connect('pick_event', on_pick_event)

        def on_click_event(event):
            if self.adding_text:
                txt = self.graph.axes.text(event.xdata, event.ydata, self.tools_panel.text_txt.get(), picker=5)
                self.text_fields.append(txt)
                self.graph.canvas.draw()
                self.adding_text = False
                self.tools_panel.add_txt.set('')
                self.tools_panel.text_txt.set('')
            else:
                if not self.pick_event:
                    try:
                        x = float("{0:.2f}".format(event.xdata))
                        y = float("{0:.2f}".format(event.ydata))
                        self.add_point(x,y)
                        self.point_panel.set_xy_values(x, y)
                    except ValueError:
                        pass
                self.pick_event = False
            return True
        self.graph.canvas.mpl_connect('button_release_event', on_click_event)

        # Point panel
        self.point_panel = PointPanel(self)
        self.point_panel.add_btn.configure(command=self.on_add_btn_click)

        def on_return_event(event):
            self.on_add_btn_click()
        self.point_panel.y_point_ent.bind('<Return>', on_return_event)
        self.point_panel.del_btn.configure(command=self.on_delete_btn_click)
        self.point_panel.grid(row=0,column=1, sticky='nsew')

        # Line panel
        self.line_panel = DrawLinePanel(self)
        self.line_panel.interpolation_btn.configure(command=self.on_interpolate_btn_click)
        self.line_panel.grid(row=1, column=1, sticky='nsew')

        # Tools panel
        self.tools_panel = ToolsPanel(self)
        self.tools_panel.set_axes_btn.configure(command=self.on_set_axes_btn_click)
        self.tools_panel.x_lim_txt.set(str(self.graph.axes.get_xlim()[1]))
        self.tools_panel.y_lim_txt.set(str(self.graph.axes.get_ylim()[1]))
        self.tools_panel.add_text_btn.configure(command=self.on_add_text_btn_clicked)
        self.tools_panel.grid(row=2, column=1, sticky='nsew')

        # Save and set panel
        self.save_and_set_panel = SaveAndSetPanel(self)
        self.save_and_set_panel.save_btn.configure(command=self.on_save_btn_click, state=DISABLED)
        self.save_and_set_panel.set_btn.configure(command=self.on_set_btn_click, state=DISABLED)
        self.save_and_set_panel.grid(row=3, column=1, sticky='nsew')

        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
        master.resizable(0,0)

    def add_point(self, new_x, new_y):
        if (new_x, new_y) not in self.xy_points:
            self.xy_points.append((new_x, new_y))
            # Sort and draw
            self.xy_points.sort()
            self.graph.draw_graph(self.xy_points, self.create_line)
            self.point_panel.clear_entries()

    def delete_point(self, old_x, old_y):
        if (old_x, old_y) in self.xy_points:
            self.xy_points.remove((old_x, old_y))
            # Sort and draw
            self.xy_points.sort()
            self.graph.draw_graph(self.xy_points, self.create_line)
        else:
            raise InvalidPointsException("Can not find point: {0}".format((old_x, old_y)))
        self.point_panel.clear_entries()
    """
    Events
    """
    def on_add_btn_click(self):
        self.saved = False
        xy = self.point_panel.get_xy_values()
        if xy is not None:
            self.add_point(xy[0], xy[1])

    def on_delete_btn_click(self):
        self.saved = False
        try:
            xy = self.point_panel.get_xy_values()
            if xy is not None:
                self.delete_point(xy[0], xy[1])
        except InvalidPointsException as e:
            tkMessageBox.showerror("Error", e.message, parent=self)

    def on_interpolate_btn_click(self):
        self.saved = False
        points = self.xy_points
        if (points is not None) and (len(points) > 0):
            points = sorted(points, key=lambda point:point[0])
            x,y = zip(*points)
            try:
                self.interpolated_x = np.linspace(np.min(x), np.max(x), (np.max(x)-np.min(x)+1))
                self.interpolated_y = interp1d(x,y,kind=self.line_panel.get_interpolation_kind())(self.interpolated_x)
                self.graph.add_interpolated_plot(self.interpolated_x, self.interpolated_y)

                self.interpolated = True
                self.save_and_set_panel.save_btn.configure(state=NORMAL)
                self.save_and_set_panel.set_btn.configure(state=NORMAL)
            except ValueError as e:
                tkMessageBox.showerror("Value error", e.message, parent=self)
            except TypeError as e:
                tkMessageBox.showerror("Interpolation error", "Failed to interpolate points... "+e.message, parent=self)
        else:
            tkMessageBox.showerror("Points error", "First select some points", parent=self)

    def on_save_btn_click(self):
        if (len(self.interpolated_x) == 0) or (len(self.interpolated_y) == 0):
            tkMessageBox.showerror("Invalid line", "Interpolate first!", parent=self)
            return
        xy = zip(self.interpolated_x, self.interpolated_y)
        name = self.save_and_set_panel.get_graph_name()
        if name:
            if str(name).__contains__('.txt'):
                graph_name = name
            else:
                graph_name = name+'.txt'
            with open(PATH+graph_name, "w") as graph_file:
                for i in xy:
                    graph_file.write(str(i)+'\n')
                if len(self.text_fields) > 0:
                    for t in self.text_fields:
                        graph_file.write(str(t)+'\n')
                tkMessageBox.showinfo("Saved", "Graph '{0}'saved to: {1}".format(graph_name, PATH))
            self.saved = True
        else:
            tkMessageBox.showerror("Invalid name", "Name can not be empty!", parent=self)

    def on_set_btn_click(self):
        if not self.saved:
            self.on_save_btn_click()

        name = self.save_and_set_panel.get_graph_name()
        self.main_screen.set_target_graph(PATH+name+'.txt')

    def on_set_axes_btn_click(self):
        try:
            x_txt = self.tools_panel.x_lim_txt.get()
            x_lim = float(x_txt)
            y_lim = float(self.tools_panel.y_lim_txt.get())
            self.graph.set_axes_limits(x_lim, y_lim)
        except ValueError:
            tkMessageBox.showerror("Value error", "X and Y axis limits should be numerical...", parent=self)

    def on_add_text_btn_clicked(self):
        txt = self.tools_panel.text_txt.get()
        if txt:
            self.adding_text = True
            self.tools_panel.add_txt.set("Click on the graph to place the text")
        else:
            tkMessageBox.showerror("Text error", "Add text to put on the graph...", parent=self)






