import tkMessageBox
from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from errors.Errors import InvalidPointsException

matplotlib.use('TkAgg')


class GraphPanel(Frame):
    def __init__(self, master, info_panel=None, is_create_graph=False, interval=1, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.is_create_graph = is_create_graph
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Temp (C)")
        self.axes.set_ylim([-1, 300])
        self.axes.set_xlim([-1, 400])

        self.cnt = 0
        self.interval = interval

        self.xy_real = []
        self.xy_target = []
        self.is_target_set = False
        self.xy_pid = []
        self.xy_points = []

        self.target_line, = self.axes.plot([], [])
        self.real_line, = self.axes.plot([], [], '.r')
        self.pid_line, = self.axes.plot([], [])
        self.create_line, = self.axes.plot([], [], 'ro', picker=5)
        self.interpol_line, = self.axes.plot([], [])

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        self.figure.tight_layout()

        if is_create_graph:
            self.axes.grid(True)

        if info_panel is not None:
            self.info_panel = info_panel
            if not is_create_graph:
                self.bind("<Enter>", lambda event:self.display_info(event, 'Select a graph'))
                self.bind("<Leave>", lambda event: self.remove_info(event, ''))

        def on_mouse_motion(event):
            if not is_create_graph:
                if (info_panel is not None) and self.is_target_set:
                    self.display_info(event,"")
            else:
                if (info_panel is not None):
                    self.display_info(event,"")
        self.canvas.mpl_connect('motion_notify_event', on_mouse_motion)

    def append_graph(self, new_x, new_y, pid_x, pid_y):
        self.xy_real.append((new_x, new_y))
        self.xy_pid.append((pid_x, pid_y))

        self.real_line.set_xdata(zip(*self.xy_real)[0])
        self.real_line.set_ydata(zip(*self.xy_real)[1])
        self.pid_line.set_xdata(zip(*self.xy_pid)[0])
        self.pid_line.set_ydata(zip(*self.xy_pid)[0])

        self.canvas.draw()

    def draw_graph(self, xy_values, line):
        if len(xy_values) > 0:
            x = zip(*xy_values)[0]
            y = zip(*xy_values)[1]

            if max(x) > (self.axes.get_xlim()[1] - 10):
                self.axes.set_xlim([-1, max(x) + 10])
            if max(y) > (self.axes.get_ylim()[1] - 10):
                self.axes.set_ylim([-1, max(y) + 10])
        else:
            x = []
            y = []

        line.set_xdata(x)
        line.set_ydata(y)

        self.canvas.draw()

    def update_axis(self):
        self.axes.set_ylim([0, 400])
        # self.a.set_xlim([0, max(self.x_real) + 2 * INTERVAL])

    def set_point(self, new_x, new_y):
        if (new_x, new_y) not in self.xy_points:
            self.xy_points.append((new_x,new_y))
        # Sort and draw
        self.xy_points.sort()
        self.draw_graph(self.xy_points, self.create_line)

    def delete_point(self, new_x, new_y):
        if (new_x, new_y) in self.xy_points:
            self.xy_points.remove((new_x, new_y))
            # Sort and draw
            self.xy_points.sort()
            self.draw_graph(self.xy_points, self.create_line)
        else:
            raise InvalidPointsException("Can not find point: {0}".format((new_x, new_y)))

    def set_target_graph2(self, graph_file_name):
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

            self.xy_target = zip(x_vals, y_vals)
            self.draw_graph(self.xy_target, self.target_line)
            self.is_target_set = True

            if self.info_panel is not None:
                self.unbind("<Enter>")

            return True
        else:
            # Return some error
            self.is_target_set = False
            return False

    def set_target_graph(self, graph_file_name):
        result = []
        if graph_file_name:
            try:
                with open(graph_file_name, "r") as fs:
                    for i in fs.readlines():
                        tmp = i.split(',')
                        x_str = tmp[0]
                        y_str = tmp[1]
                        try:
                            result.append((float(x_str[1:]),(float(y_str[:-2]))))
                        except:
                            pass

            except Exception as e:
                tkMessageBox.showerror("Reading error", e.message)
                self.is_target_set = False
                return False

            self.xy_target = result
            self.draw_graph(self.xy_target, self.target_line)
            self.is_target_set = True

            if self.info_panel is not None:
                self.unbind("<Enter>")

            return True
        else:
            # Return some error
            self.is_target_set = False
            return False

    def get_xy_point_values(self):
        return self.xy_points

    def add_interpolated_plot(self, x, y):
        if len(self.axes.lines) > 1:
            self.axes.lines.pop(-1)

        self.interpol_line = self.axes.plot(x, y, '--')
        self.canvas.draw()

    def display_info(self, event, arg):
        if self.info_panel is not None:
            if self.is_target_set or self.is_create_graph:
                self.info_panel.set_info("x: {}, y: {}".format(event.x, event.y))
            else:
                self.info_panel.set_info(arg)

    def remove_info(self, event, arg):
        if self.info_panel is not None:
            self.info_panel.set_info(arg)