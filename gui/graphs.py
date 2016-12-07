import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

INTERVAL = 0.01


class Graph:
    def __init__(self, master):
        self.f = Figure(figsize=(5,4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.set_xlabel("Time")
        self.a.set_ylabel("Temp")

        self.cnt = 0
        self.y = []
        self.x = []

        self.line1, = self.a.plot(self.x, self.y)

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

    def update(self, value):
        self.cnt += INTERVAL
        self.x.append(self.cnt)
        self.y.append(value)

        self.line1.set_xdata(self.x)
        self.line1.set_ydata(self.y)

        self.a.set_ylim([max(self.y)-500, max(self.y)+500])
        self.a.set_xlim([0, max(self.x)+2*INTERVAL])

        self.canvas.draw()