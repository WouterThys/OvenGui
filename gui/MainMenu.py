from Tkinter import *
import tkMessageBox

from gui.Dialogs import SerialSettingsDialog


class MainMenu:
    def __init__(self, parent, settings, serial, end_command):
        self.parent = parent
        self.settings = settings
        self.serial = serial
        self.end_command = end_command

        menu = Menu(parent)
        parent.config(menu=menu)

        start_menu = Menu(menu)
        menu.add_cascade(label="Start", menu=start_menu)
        start_menu.add_command(label="Save", command=self.menu_main_save)
        start_menu.add_separator()
        start_menu.add_command(label="Quit", command=self.menu_main_quit)

        settings_menu = Menu(menu)
        menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Serial", command=self.menu_settings_serial)
        settings_menu.add_command(label="Pid", command=self.menu_settings_pid)
        settings_menu.add_command(label="Graph", command=self.menu_settings_graph)

    def menu_main_save(self):
        tkMessageBox.showinfo("Save", "Saved session!")

    def menu_main_quit(self):
        self.end_command()

    def menu_settings_serial(self):
        SerialSettingsDialog(self.parent, self.serial)


    def menu_settings_pid(self):
        SerialSettingsDialog(self.parent, self.serial)

    def menu_settings_graph(self):
        SerialSettingsDialog(self.parent, self.serial)