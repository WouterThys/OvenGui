import tkMessageBox
from Tkinter import *
from scipy.interpolate import interp1d
import ttk


class DrawLinePanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.default_bg = self.cget('bg')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Title
        title_lbl = Label(self, text="Line", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=2)

        # Widgets
        vals = ('zero', 'slinear', 'quadratic', 'cubic')
        self.interpolation_txt = StringVar()
        self.interpolation_cb = ttk.Combobox(self, textvariable=self.interpolation_txt, values=vals)
        self.interpolation_cb.current(0)
        self.interpolation_cb.grid(row=1, column=0, columnspan=2)

        self.interpolation_btn = Button(self, text="Interpolate")
        self.interpolation_btn.grid(row=2, column=1)

    def interpolate_points(self, x_points, y_points):
        interpolation_kind = str(self.interpolation_cb.get())
        try :
            return interp1d(x_points, y_points, kind=interpolation_kind)
        except ValueError as e:
            tkMessageBox.showerror("Value error", e.message)
        except TypeError as e:
            tkMessageBox.showerror("Type error", e.message)
        except Exception as e:
            tkMessageBox.showerror("Error", e.message)

    def get_interpolation_kind(self):
        return str(self.interpolation_cb.get())