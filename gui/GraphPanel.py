from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')


INTERVAL = 1
MIN = 60


class GraphPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.set_xlabel("Time")
        self.a.set_ylabel("Temp")

        self.cnt = 0
        self.y_real = []
        self.x_real = []
        self.y_target = []
        self.x_target = []
        self.y_pid = []
        self.x_pid = []

        self.target_line, = self.a.plot(self.x_target, self.y_target)
        self.real_line, = self.a.plot(self.x_real, self.y_real, '.r')
        self.pid_line, = self.a.plot(self.x_pid, self.y_pid)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        self.f.tight_layout()

        # self.toolbar = NavigationToolbar2TkAgg(self.canvas, master)
        # self.toolbar.update()
        # self.canvas._tkcanvas.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)
        #
        # self.canvas.mpl_connect('key_press_event', self.on_key_event

    # def on_key_event(self, event):
    #     print("you pressed %s" % event.key)
    #     key_press_handler(event, self.canvas, self.toolbar)

    def update_graph(self, value, pid=0):
        self.cnt += INTERVAL
        self.x_real.append(self.cnt)
        self.y_real.append(value)
        self.x_pid.append(self.cnt)
        self.y_pid.append(pid)

        self.real_line.set_xdata(self.x_real)
        self.real_line.set_ydata(self.y_real)
        self.pid_line.set_xdata(self.x_pid)
        self.pid_line.set_ydata(self.y_pid)

        self.update_axis()
        self.canvas.draw()

    def update_axis(self):
        self.a.set_ylim([0, 400])
        # self.a.set_xlim([0, max(self.x_real) + 2 * INTERVAL])

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
                            y_vals.append(float(val.strip()))
                            x_vals.append(float(cnt))
                            cnt += 1

            except Exception as e:
                print e.message
                return False

            self.x_target = x_vals
            self.y_target = y_vals
            self.target_line.set_xdata(self.x_target)
            self.target_line.set_ydata(self.y_target)

            max_x = max(self.x_target)
            max_y = max(self.y_target)

            self.a.set_ylim([-1, (max_y + 50)])
            self.a.set_xlim([-1, (max_x + 10)])

            self.canvas.draw()
            return True
        else:
            # Return some error
            return False
