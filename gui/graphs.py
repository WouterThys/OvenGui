import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Graph:

    def __init__(self, master):
        self.f = Figure(figsize=(5,4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.t = arange(0.0, 3.0, 0.01)
        self.s = sin(2*pi*self.t)

        self.a.plot(self.t, self.s)

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