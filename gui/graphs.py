import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

INTERVAL = 1
MIN = 60


class Graph:
    def __init__(self, master, target):
        self.f = Figure(figsize=(5,4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.set_xlabel("Time")
        self.a.set_ylabel("Temp")

        self.cnt = 0
        self.y_real = []
        self.x_real = []
        self.y_target = target[1]
        self.x_target = target[0]
        self.y_pid = []
        self.x_pid = []

        self.guide_line, = self.a.plot(self.x_target, self.y_target)
        self.real_line, = self.a.plot(self.x_real, self.y_real, '.r')
        self.pid_line, = self.a.plot(self.x_pid, self.y_pid)

        self.canvas = FigureCanvasTkAgg(self.f, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.canvas.mpl_connect('key_press_event', self.on_key_event)

    def on_key_event(self, event):
        print("you pressed %s" % event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    def update(self, value, pid=0):
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
        #self.a.set_xlim([0, max(self.x_real) + 2 * INTERVAL])