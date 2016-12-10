import os
import tkMessageBox
from Tkinter import *
import sys

import MainMenu
from gui.BottomPanel import BottomPanel
from gui.ControlPanel import ControlPanel
from gui.Dialogs import PicInfoDialog, FileDialog, SerialSettingsDialog
from gui.FeedBackPanel import FeedBackPanel
from gui.SettingsPanel import SettingsPanel
from gui.MessagePanel import MessagePanel
from gui.GraphPanel import GraphPanel
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
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Bottom panel
        self.bottom_panel = BottomPanel(master)
        self.bottom_panel.grid(row=4, column=0, columnspan=2, sticky='nsew')

        # Graph panel
        self.graph = GraphPanel(master, self.bottom_panel)
        self.graph.grid(row=0, rowspan=3, column=0, sticky='nsew')

        # Control panel
        self.control_panel = ControlPanel(master, self.bottom_panel)
        self.control_panel.start_btn.configure(command=self.on_start_btn_click)
        self.control_panel.stop_btn.configure(command=self.on_stop_btn_click)
        self.control_panel.graph_btn.configure(command=self.on_graph_btn_click)
        self.control_panel.enable_start_btn(False)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.enable_graph_btn(True)
        self.control_panel.grid(row=0, column=1, sticky='nsew')

        # Feed back panel
        self.feedback_panel = FeedBackPanel(master)
        self.feedback_panel.set_kp_value(self.manager.kp)
        self.feedback_panel.set_ki_value(self.manager.ki)
        self.feedback_panel.set_kd_value(self.manager.kd)
        self.feedback_panel.grid(row=1, column=1, sticky='nsew')

        # Settings panel
        self.settings_panel = SettingsPanel(master, self.bottom_panel)
        self.settings_panel.uart_settings_btn.configure(command=self.on_uart_settings_btn_click)
        self.settings_panel.pid_settings_btn.configure(command=self.on_pid_settings_btn_click)
        self.settings_panel.graph_settings_btn.configure(command=self.on_graph_settings_btn_click)
        self.settings_panel.grid(row=2, column=1, sticky='nsew')

        # Message panel
        self.message_panel = MessagePanel(master)
        self.message_panel.grid(row=3, column=0, sticky='nsew')

        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())

    def process_incoming(self):
        """
        Set the appropriate fields
        """
        self.feedback_panel.set_target_value(self.manager.pid.set_point)
        self.feedback_panel.set_sense_value(self.manager.temp_real)
        self.feedback_panel.set_error_value(self.manager.pid.error)
        self.feedback_panel.set_pid_value(self.manager.pid.output)

        msg = self.manager.last_message
        if not msg is None:
            if not msg.type == "ack":
                self.message_panel.add_new_line(msg.message_time, msg.sender, msg.command, msg.message)
                self.manager.last_message = None

        pass

    def show_pic_info(self):
        PicInfoDialog(self.master, self.pic_info)

    def forced_stop(self):
        self.on_stop_btn_click()

    """
    Events
    """

    def on_start_btn_click(self):
        self.manager.start_writing_thread()
        self.control_panel.enable_start_btn(False)
        self.control_panel.enable_stop_btn(True)
        self.control_panel.enable_graph_btn(False)

    def on_stop_btn_click(self):
        self.manager.stop_writing_thread()
        self.control_panel.enable_start_btn(True)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.enable_graph_btn(True)

    def on_graph_btn_click(self):
        fd = FileDialog(self.master)
        graph_file = fd.open_file_name()
        if graph_file:
            if os.path.isfile:
                if self.graph.set_target_graph(graph_file):
                    self.manager.temp_target = self.graph.y_target
                    self.control_panel.enable_start_btn(True)
                    self.control_panel.enable_stop_btn(False)
                    self.control_panel.enable_graph_btn(True)
                else:
                    tkMessageBox.showerror("Error reading file",
                                           "An error occurred because the korean children did not understand it, "
                                           "check if the file was correct...")
            else:
                tkMessageBox.showerror("Error file type",
                                       "We have decided this is not a valid file type...")

    def on_uart_settings_btn_click(self):
        SerialSettingsDialog(self.master, self.manager.my_serial)

    def on_pid_settings_btn_click(self):
        print 'uart settings'

    def on_graph_settings_btn_click(self):
        print 'uart settings'
