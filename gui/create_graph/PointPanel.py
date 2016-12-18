import tkMessageBox
from Tkinter import *

class PointPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        # Frame.__init__(self, master, width=50, height=100, *args, **kwargs)
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.default_bg = self.cget('bg')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Title
        title_lbl = Label(self, text="Points", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=2)

        # Widgets
        Label(self, text="X point", fg="dim gray").grid(row=1, column=0, sticky='w')
        Label(self, text="Y point", fg="dim gray").grid(row=1, column=1, sticky='w')

        self.x_point_txt = StringVar()
        self.y_point_txt = StringVar()
        self.x_point_ent = Entry(self, textvariable=self.x_point_txt, justify=CENTER, width=8)
        self.x_point_ent.grid(row=2, column=0, sticky='ew')
        self.x_point_ent.focus()
        self.y_point_ent = Entry(self, textvariable=self.y_point_txt, justify=CENTER, width=8)
        self.y_point_ent.grid(row=2, column=1, sticky='ew')

        self.add_btn = Button(self, text="Add")
        self.add_btn.grid(row=3, column=0)
        self.del_btn = Button(self, text="Delete")
        self.del_btn.grid(row=3, column=1)

    def set_xy_values(self, x, y):
        self.x_point_txt.set(str(x))
        self.y_point_txt.set(str(y))

    def get_xy_values(self):
        try:
            if self.x_point_ent.get() == "":
                tkMessageBox.showerror("Error", "X point can not be empty!")
                return None
            if float(self.x_point_ent.get()) < 0:
                tkMessageBox.showerror("Error", "X point has to be bigger than 0!")
                return None
            if self.y_point_ent.get() == "":
                tkMessageBox.showerror("Error", "Y point can not be empty!")
                return None
            if float(self.y_point_ent.get()) < 0:
                tkMessageBox.showerror("Error", "Y point has to be bigger than 0!")
                return None

            return float(self.x_point_ent.get()), float(self.y_point_ent.get())

        except ValueError as e:
            tkMessageBox.showerror("Error", "Input value has to be numeric: "+e)

    def clear_entries(self):
        self.x_point_ent.delete(0,END)
        self.y_point_ent.delete(0,END)

