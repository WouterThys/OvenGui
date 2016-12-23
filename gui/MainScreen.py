import os
import tkMessageBox
from Tkinter import *
import sys

import MainMenu
from gui.BottomPanel import BottomPanel
from gui.ControlPanel import ControlPanel
from gui.Dialogs import PicInfoDialog, FileDialog, SerialSettingsDialog, PIDSettingsDialog
from gui.FeedBackPanel import FeedBackPanel
from gui.MessagePanel import MessagePanel
from gui.GraphPanel import GraphPanel
from gui.TemperaturePanel import TemperaturePanel
from my_serial.PICClasses import PICInfo


class MainScreen:
    def __init__(self, master, manager, interval, end_command):
        self.master = master
        self.pic_info = PICInfo
        self.manager = manager
        self.interval = interval
        # Set up the main menu
        MainMenu.MainMenu(master, self.manager.my_serial, self.manager.fsm.pid, self, end_command)
        # Window settings
        self.master.minsize(width=1000, height=500)
        self.master.wm_title("Oven")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Bottom panel
        self.bottom_panel = BottomPanel(master)
        self.bottom_panel.grid(row=3, column=0, columnspan=2, sticky='ew')

        # Graph panel
        self.graph = GraphPanel(master, info_panel=self.bottom_panel, is_create_graph=False, interval=self.interval)
        self.graph.grid(row=0, rowspan=2, column=0, sticky='nsew')

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
        self.feedback_panel.set_kp_value(self.manager.fsm.pid.Kp)
        self.feedback_panel.set_ki_value(self.manager.fsm.pid.Ki)
        self.feedback_panel.set_kd_value(self.manager.fsm.pid.Kd)
        self.feedback_panel.grid(row=1, column=1, sticky='nsew')

        # Temperature panel
        self.temperature_panel = TemperaturePanel(master, self.bottom_panel)
        self.temperature_panel.grid(row=2, column=1, sticky='nsew')

        # Message panel
        self.message_panel = MessagePanel(master)
        self.message_panel.grid(row=2, column=0, sticky='nsew')

        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())

        print self.feedback_panel.pid_ent.cget("width")

    def process_incoming(self):
        """
        Set the appropriate fields
        """
        self.feedback_panel.update_all(self.manager)
        self.temperature_panel.set_temperature_value(self.manager.fsm.temp_real)

        msg = self.manager.last_message
        if not msg is None:
            if not msg.type == "ack":
                self.message_panel.add_new_line(msg.message_time, msg.sender, msg.command, msg.message)
                self.manager.last_message = None

        pass

    def show_pic_info(self):
        PicInfoDialog(self.master, self.pic_info)

    def forced_stop(self):
        if self.graph.is_target_set:
            self.control_panel.enable_start_btn(True)
        else:
            self.control_panel.enable_start_btn(False)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.enable_graph_btn(True)

    """
    Events
    """
    def on_start_btn_click(self):
        if not self.manager.fsm.door_open_state:
            self.control_panel.enable_start_btn(False)
            self.control_panel.enable_stop_btn(True)
            self.control_panel.enable_graph_btn(False)
            self.manager.fsm.should_start = True
        else:
            tkMessageBox.showwarning('Door open', 'Close the oven door before starting...')

    def on_stop_btn_click(self):
        self.control_panel.enable_start_btn(True)
        self.control_panel.enable_stop_btn(False)
        self.control_panel.enable_graph_btn(True)
        self.manager.fsm.should_stop = True

    def on_graph_btn_click(self):
        fd = FileDialog(self.master)
        graph_file = fd.open_file_name()
        if graph_file:
            self.set_target_graph(graph_file)

    def set_target_graph(self, graph_file):
        if os.path.isfile:
            if self.graph.set_target_graph(graph_file):
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
        self.manager.fsm.graph_set = self.graph.is_target_set

    def on_uart_settings_btn_click(self):
        SerialSettingsDialog(self.master, self.manager.my_serial)

    def on_pid_settings_btn_click(self):
        if self.control_panel.stop_btn.cget('state') == 'disabled':
            PIDSettingsDialog(self.master, self.manager.pid)
            self.feedback_panel.set_kp_value(self.manager.pid.Kp)
            self.feedback_panel.set_ki_value(self.manager.pid.Ki)
            self.feedback_panel.set_kd_value(self.manager.pid.Kd)
        else:
            tkMessageBox.showwarning("Warning","First stop running before change PID values")

    def on_graph_settings_btn_click(self):
        print 'uart settings'
