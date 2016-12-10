from Tkinter import *
import re


class HoverInfo(Menu):
    def __init__(self, parent, text, command=None):
        self.com = command
        Menu.__init__(self, parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
        to_text = re.split('\n', text)
        for t in to_text:
            self.add_command(label=t)
        self.configure(fg='dim gray')
        self.displayed = False
        self.master.bind("<Enter>", self.display_it)
        self.master.bind("<Leave>", self.remove_it)

    def __del__(self):
        self.master.unbind("<Enter>")
        self.master.unbind("<Leave>")

    def display_it(self, event):
        if not self.displayed:
            self.displayed = True
            self.post(event.x_root, event.y_root)
        if self.com is not None:
            self.master.unbind_all("<Return>")
            self.master.bind_all("<Return>", self.click_it)
        pass

    def remove_it(self, event):
        if self.displayed:
            self.displayed = False
            self.unpost()
        if self.com is not None:
            self.unbind_all("<Return>")

    def click_it(self, event):
        self.com()
