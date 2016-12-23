import os
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from Tkinter import *
import ttk

import serial

from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

from my_serial.SerialInterface import SerialInterface
from settings.Settings import read_settings, UART_SETTINGS, write_settings, PID_SETTINGS


class SerialSettingsDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, my_serial):
        self.my_serial = my_serial
        self.settings = self.my_serial.ser.getSettingsDict()
        tkSimpleDialog.Dialog.__init__(self, master, "Serial settings")

    def body(self, master):
        Label(master, text="Com port").grid(row=0, sticky=W)
        Label(master, text="Baud rate").grid(row=1, sticky=W)
        Label(master, text="Data bits").grid(row=2, sticky=W)
        Label(master, text="Stop bits").grid(row=3, sticky=W)
        Label(master, text="Parity").grid(row=4, sticky=W)

        port_str = StringVar()
        baud_str = StringVar()
        bits_str = StringVar()
        stop_str = StringVar()
        pari_str = StringVar()

        self.port_cb = ttk.Combobox(master, values=SerialInterface.serial_ports(), textvariable=port_str)
        self.baud_cb = ttk.Combobox(master, values=serial.Serial.BAUDRATES, textvariable=baud_str)
        self.bits_cb = ttk.Combobox(master, values=serial.Serial.BYTESIZES, textvariable=bits_str)
        self.stop_cb = ttk.Combobox(master, values=serial.Serial.STOPBITS, textvariable=stop_str)
        self.pari_cb = ttk.Combobox(master, values=serial.Serial.PARITIES, textvariable=pari_str)

        port_str.set(self.my_serial.ser.port)
        baud_str.set(self.settings.get("baudrate"))
        bits_str.set(self.settings.get("bytesize"))
        stop_str.set(self.settings.get("stopbits"))
        pari_str.set(self.settings.get("partity"))

        self.port_cb.grid(row=0, column=1)
        self.baud_cb.grid(row=1, column=1)
        self.bits_cb.grid(row=2, column=1)
        self.stop_cb.grid(row=3, column=1)
        self.pari_cb.grid(row=4, column=1)

        return self.baud_cb # Initial focus

    def validate(self):
        try:
            self.settings['parity'] = str(self.pari_cb.get())
            self.settings['baudrate'] = int(self.baud_cb.get())
            self.settings['bytesize'] = int(self.bits_cb.get())
            self.settings['stopbits'] = int(self.stop_cb.get())
            return 1
        except Exception as e:
            tkMessageBox.showerror(
                "Bad input",
                "Illegal values, please try again: "+e.message
            )
            return 0

    def apply(self):
        yaml_dict = read_settings(UART_SETTINGS)
        yaml_dict['parity'] = str(self.pari_cb.get())
        yaml_dict['baud_rate'] = int(self.baud_cb.get())
        yaml_dict['data_bits'] = int(self.bits_cb.get())
        yaml_dict['stop_bits'] = int(self.stop_cb.get())
        yaml_dict['com_port'] = str(self.port_cb.get())
        write_settings(UART_SETTINGS, yaml_dict)

        self.my_serial.serial_destroy()
        self.my_serial.configure_serial()


class PIDSettingsDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, pid):
        self.pid = pid

        self.kp_ent = None
        self.ki_ent = None
        self.kd_ent = None
        self.dt_ent = None
        self.wu_ent = None

        tkSimpleDialog.Dialog.__init__(self, master, "PID settings")

    def body(self, master):
        Label(master, text="Kp").grid(row=0, sticky=W)
        Label(master, text="Ki").grid(row=1, sticky=W)
        Label(master, text="Kd").grid(row=2, sticky=W)
        Label(master, text="dt").grid(row=3, sticky=W)
        Label(master, text="Wu").grid(row=4, sticky=W)

        kp_str = StringVar()
        ki_str = StringVar()
        kd_str = StringVar()
        dt_str = StringVar()
        wu_str = StringVar()

        self.kp_ent = Entry(master, textvariable=kp_str)
        self.ki_ent = Entry(master, textvariable=ki_str)
        self.kd_ent = Entry(master, textvariable=kd_str)
        self.dt_ent = Entry(master, textvariable=dt_str)
        self.wu_ent = Entry(master, textvariable=wu_str)

        kp_str.set(self.pid.Kp)
        ki_str.set(self.pid.Ki)
        kd_str.set(self.pid.Kd)
        dt_str.set(self.pid.dt)
        wu_str.set(self.pid.Wu)

        self.kp_ent.grid(row=0, column=1)
        self.ki_ent.grid(row=1, column=1)
        self.kd_ent.grid(row=2, column=1)
        self.dt_ent.grid(row=3, column=1)
        self.wu_ent.grid(row=4, column=1)

        return self.kp_ent # Initial focus

    def validate(self):
        try:
            yaml_dict = read_settings(PID_SETTINGS)
            yaml_dict['Kd'] = float(self.kd_ent.get())
            yaml_dict['Ki'] = float(self.ki_ent.get())
            yaml_dict['Kp'] = float(self.kp_ent.get())
            yaml_dict['Wu'] = float(self.wu_ent.get())
            yaml_dict['dt'] = float(self.dt_ent.get())
            write_settings(PID_SETTINGS, yaml_dict)

            self.pid.configure_pid()
            return 1
        except Exception as e:
            tkMessageBox.showerror(
                "Bad input",
                "Illegal values, please try again: "+e.message
            )
            return 0

    def apply(self):
        pass


class PicInfoDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, PICInfo):
        self.pic_info = PICInfo
        tkSimpleDialog.Dialog.__init__(self, master, "PIC Info")

    def body(self, master):
        Label(master, text="PIC name: ").grid(row=0, sticky=W)
        Label(master, text="Last communication: ").grid(row=1, sticky=W)

        Entry(master, text=self.pic_info.pic_name).grid(row=0, column=1)
        Entry(master, text=self.pic_info.pic_last_communication).grid(row=1, column=1)


class FileDialog:
    def __init__(self, master):
        self.master = master

        initial_path = sys.executable
        if sys.platform.startswith('win'):
            initial_path = os.path.splitdrive(sys.executable)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('Text files', '.txt'),('All files', '.*')]
        options['initialdir'] = initial_path
        #options['initialfile'] = 'graph.txt'
        options['parent'] = self.master
        options['title'] = 'Select a file'

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = initial_path
        options['mustexist'] = False
        options['parent'] = self.master
        options['title'] = 'Select a directory'

    def open_file(self):
        return tkFileDialog.askopenfile(mode='r', **self.file_opt)

    def open_file_name(self):
        # Get file name
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        # if filename:
        #     return open(filename, 'r')
        return filename

    def save_file(self):
        return tkFileDialog.asksaveasfile(mode='w', **self.file_opt)

    def save_file_name(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        # if filename:
        #     return open(filename, 'w')
        return filename

    def ask_directory(self):
        return tkFileDialog.askdirectory(**self.dir_opt)


class GraphOptionsDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, canvas):
        self.canvas = canvas
        tkSimpleDialog.Dialog.__init__(self, master, "PID settings")

    def body(self, master):
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill=BOTH, expand=1)

    def apply(self):
        pass