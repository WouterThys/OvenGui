import tkMessageBox
from Tkinter import *
import sys

import MainMenu
from gui.ControlPanel import ControlPanel
from gui.Dialogs import PicInfoDialog, FileDialog, SerialSettingsDialog
from gui.FeedBackPanel import FeedBackPanel
from gui.graphs import Graph
from my_serial.PICClasses import PICInfo


class MainScreen:
    def __init__(self, master, settings, serial_interface, manager, end_command):
        self.master = master
        self.pic_info = PICInfo
        self.manager = manager
        # Set up the main menu
        MainMenu.MainMenu(master, settings, serial_interface, end_command)
        # Window settings
        self.master.minsize(width=1000, height=500)
        self.master.wm_title("Oven")

        # Graph
        graph_frame = Frame(master)
        graph_frame.pack(side=LEFT, fill=BOTH, expand=1)
        self.graph = Graph(graph_frame)

        # Control panel
        self.control_panel = ControlPanel(master)
        self.control_panel.start_btn.configure(command=self.on_start_btn_click)
        self.control_panel.stop_btn.configure(command=self.on_stop_btn_click)
        self.control_panel.graph_btn.configure(command=self.on_graph_btn_click)
        self.control_panel.enable_start_btn(False)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.pack(side=TOP, fill=BOTH, expand=1)

        # Feed back panel
        self.feedback_panel = FeedBackPanel(master)
        self.feedback_panel.pack(side=TOP,fill=BOTH, expand=1)
        self.feedback_panel.set_kp_value(self.manager.kp)
        self.feedback_panel.set_ki_value(self.manager.ki)
        self.feedback_panel.set_kd_value(self.manager.kd)

        # Ask for the serial settings
        #SerialSettingsDialog(self.master, serial_interface)

    def process_incoming(self):
        """
        Set the appropriate fields
        """
        self.feedback_panel.set_target_value(self.manager.pid.set_point)
        self.feedback_panel.set_sense_value(self.manager.temp_real)
        self.feedback_panel.set_pid_value(self.manager.pid.output)

        pass

    def show_pic_info(self):
        PicInfoDialog(self.master, self.pic_info)

    """
    Events
    """
    def on_start_btn_click(self):
        self.manager.start_reading_thread()
        self.control_panel.enable_start_btn(False)
        self.control_panel.enable_stop_btn(True)
        self.control_panel.enable_graph_btn(False)

    def on_stop_btn_click(self):
        self.manager.stop_reading_thread()
        self.control_panel.enable_start_btn(True)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.enable_graph_btn(True)

    def on_graph_btn_click(self):
        fd = FileDialog(self.master)
        graph_file = fd.open_file_name()
        if graph_file:
            if self.graph.set_target_graph(graph_file):
                self.control_panel.enable_start_btn(True)
                self.control_panel.enable_stop_btn(False)
                self.control_panel.enable_graph_btn(True)
            else:
                tkMessageBox.showerror("Error reading file", "An error occurred because the korean children did not understand it, check if the file was correct...")