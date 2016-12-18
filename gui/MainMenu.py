import tkMessageBox
from Tkinter import *

from gui.Dialogs import SerialSettingsDialog, PIDSettingsDialog
from gui.create_graph.CreateGraphPanel import CreateGraphWindow


class MainMenu:
    def __init__(self, parent, serial, pid, end_command):
        self.parent = parent
        self.serial = serial
        self.pid = pid
        self.end_command = end_command

        menu = Menu(parent)
        parent.config(menu=menu)

        start_menu = Menu(menu)
        start_menu.add_command(label="Save", command=self.menu_main_save)
        start_menu.add_separator()
        start_menu.add_command(label="Quit", command=self.menu_main_quit)

        settings_menu = Menu(menu)
        settings_menu.add_command(label="Serial", command=self.menu_settings_serial)
        settings_menu.add_command(label="Pid", command=self.menu_settings_pid)
        settings_menu.add_command(label="Graph", command=self.menu_settings_graph)

        graph_menu = Menu(menu)
        graph_menu.add_command(label="View")
        graph_menu.add_command(label="Create", command=self.menu_graph_create)

        menu.add_cascade(label="Start", menu=start_menu)
        menu.add_cascade(label="Settings", menu=settings_menu)
        menu.add_cascade(label="Graph", menu=graph_menu)

    def menu_main_save(self):
        tkMessageBox.showinfo("Save", "Saved session!")

    def menu_main_quit(self):
        self.end_command()

    def menu_settings_serial(self):
        SerialSettingsDialog(self.parent, self.serial)

    def menu_settings_pid(self):
        PIDSettingsDialog(self.parent, self.pid)

    def menu_settings_graph(self):
        SerialSettingsDialog(self.parent, self.serial)

    def menu_graph_create(self):
        new_window = Toplevel(self.parent)
        create_graph = CreateGraphWindow(new_window)
        create_graph.pack()