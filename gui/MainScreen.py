import Queue
from Tkinter import *
from numpy import arange, full
import MainMenu
from gui.ControlPanel import ControlPanel
from gui.Dialogs import PicInfoDialog
from gui.FeedBackPanel import FeedBackPanel
from gui.graphs import Graph
from my_serial.PICClasses import PICInfo
from pid.PID import PID

TARGET_Y = []
TARGET_X = []
for i in range(0,350):
    TARGET_X.append(i)
    if i < 110:
        TARGET_Y.append((180.0/110.0)*float(i))
    if (i >= 110) and (i < 200):
        TARGET_Y.append(180)
    if (i >= 200) and (i < 250):
        TARGET_Y.append((120.0/50.0)*(float(i)-200) + 180)
    if (i >= 250) and (i < 260):
        TARGET_Y.append(300)
    if i >= 260:
        TARGET_Y.append(TARGET_Y[-1]-2)

TARGET = (TARGET_X, TARGET_Y)


class MainScreen:
    def __init__(self, master, queue, settings, serial, manager, end_command):
        self.master = master
        self.queue = queue
        self.serial = serial
        self.pic_info = PICInfo
        self.manager = manager
        # Set up the main menu
        MainMenu.MainMenu(master, settings, serial, end_command)
        # Window settings
        self.master.minsize(width=400, height=400)
        self.master.wm_title("Oven")

        # Graph
        graph_frame = Frame(master)
        graph_frame.pack(side=LEFT, fill=BOTH, expand=1)
        self.graph = Graph(graph_frame, TARGET)

        # Control panel
        self.control_panel = ControlPanel(master)
        self.control_panel.pack(side=TOP, fill=BOTH, expand=1)

        # Feed back panel
        self.feedback_panel = FeedBackPanel(master)
        self.feedback_panel.pack(side=TOP,fill=BOTH, expand=1)
        self.feedback_panel.set_kp_value(self.manager.kp)
        self.feedback_panel.set_ki_value(self.manager.ki)
        self.feedback_panel.set_kd_value(self.manager.kd)

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