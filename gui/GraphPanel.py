from Tkinter import *
import matplotlib
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from errors.Errors import InvalidPointsException

matplotlib.use('TkAgg')


class GraphPanel(Frame):
    def __init__(self, master, info_panel=None, interval=1, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.set_xlabel("Time (s)")
        self.a.set_ylabel("Temp (C)")
        self.a.set_ylim([-1, 300])
        self.a.set_xlim([-1, 400])

        self.cnt = 0
        self.interval = interval

        self.y_real = []
        self.x_real = []
        self.y_target = []
        self.x_target = []
        self.is_target_set = False
        self.y_pid = []
        self.x_pid = []
        self.y_points = []
        self.x_points = []

        self.target_line, = self.a.plot(self.x_target, self.y_target)
        self.real_line, = self.a.plot(self.x_real, self.y_real, '.r')
        self.pid_line, = self.a.plot(self.x_pid, self.y_pid)
        self.create_line, = self.a.plot(self.x_points, self.y_points, 'ro', picker=5)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        self.f.tight_layout()

        if info_panel is not None:
            self.info_panel = info_panel
            self.bind("<Enter>", lambda event:self.display_info(event, 'Select a graph'))
            self.bind("<Leave>", lambda event: self.remove_info(event, ''))

        def on_mouse_motion(event):
            if (info_panel is not None) and self.is_target_set:
                self.display_info(event,"")
        self.canvas.mpl_connect('motion_notify_event', on_mouse_motion)

        # def on_button_release_event(event):
        #     GraphOptionsDialog(self.master, self.canvas)
        # self.canvas.mpl_connect('button_release_event', on_button_release_event)

    def update_graph(self, value, pid=0):
        self.cnt += self.interval
        self.x_real.append(self.cnt)
        self.y_real.append(value)
        self.x_pid.append(self.cnt)
        self.y_pid.append(pid)

        self.real_line.set_xdata(self.x_real)
        self.real_line.set_ydata(self.y_real)
        self.pid_line.set_xdata(self.x_pid)
        self.pid_line.set_ydata(self.y_pid)

        #self.update_axis()
        self.canvas.draw()

    def update_axis(self):
        self.a.set_ylim([0, 400])
        # self.a.set_xlim([0, max(self.x_real) + 2 * INTERVAL])

    def set_point(self, x, y):
        self.x_points.append(x)
        self.y_points.append(y)

        # Sort it
        yx = zip(self.y_points, self.x_points)
        yx.sort()
        self.x_points = [x for y, x in yx]
        self.y_points = [y for y, x in yx]

        self.create_line.set_xdata(self.x_points)
        self.create_line.set_ydata(self.y_points)

        if max(self.x_points) > (self.a.get_xlim()[1]-10):
            self.a.set_xlim([-1, max(self.x_points)+10])
        if max(self.y_points) > (self.a.get_ylim()[1]-10):
            self.a.set_ylim([-1, max(self.y_points)+10])

        self.canvas.draw()

    def delete_point(self, x, y):
        if (x in self.x_points) and (y in self.y_points):
            self.x_points.remove(x)
            self.y_points.remove(y)

            # Sort it
            yx = zip(self.y_points, self.x_points)
            yx.sort()
            self.x_points = [x for y, x in yx]
            self.y_points = [y for y, x in yx]

            self.create_line.set_xdata(self.x_points)
            self.create_line.set_ydata(self.y_points)

            self.canvas.draw()
        else:
            raise InvalidPointsException("Can not find point: ({0},{1})".format(float(x), float(y)))

    def set_target_graph(self, graph_file_name):
        cnt = 0
        x_vals = []
        y_vals = []
        if graph_file_name:
            try:
                with open(graph_file_name, "r") as file_stream:
                    for line in file_stream:
                        current_line = line.split(",")
                        for val in current_line:
                            if val == '\n':
                                continue
                            y_vals.append(float(val.strip()))
                            x_vals.append(float(cnt))
                            cnt += self.interval

            except Exception as e:
                print e.message
                self.is_target_set = False
                return False

            self.x_target = x_vals
            self.y_target = y_vals
            self.target_line.set_xdata(self.x_target)
            self.target_line.set_ydata(self.y_target)

            max_x = max(self.x_target)
            max_y = max(self.y_target)

            self.a.set_ylim([-1, (max_y + 50)])
            self.a.set_xlim([-1, (max_x + 10)])

            self.is_target_set = True
            self.canvas.draw()

            if self.info_panel is not None:
                self.unbind("<Enter>")

            return True
        else:
            # Return some error
            self.is_target_set = False
            return False

    def get_xy_values(self):
        X,Y = [],[]
        for lines in self.a.get_lines():
            for x,y in lines.get_xydata():
                X.append(x)
                Y.append(y)
        return X, Y

    def display_info(self, event, arg):
        if self.info_panel is not None:
            if self.is_target_set:
                self.info_panel.set_info("x: {}, y: {}".format(event.x, event.y))
            else:
                self.info_panel.set_info(arg)

    def remove_info(self, event, arg):
        if self.info_panel is not None:
            self.info_panel.set_info(arg)