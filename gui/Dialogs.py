import os
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from Tkinter import *

import serial
from my_serial.SerialInterface import SerialInterface


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

        self.port_sp = Spinbox(master, values=SerialInterface.serial_ports(), textvariable=port_str)
        self.baud_sp = Spinbox(master, values=serial.Serial.BAUDRATES, textvariable=baud_str)
        self.bits_sp = Spinbox(master, values=serial.Serial.BYTESIZES, textvariable=bits_str)
        self.stop_sp = Spinbox(master, values=serial.Serial.STOPBITS,  textvariable=stop_str)
        self.pari_sp = Spinbox(master, values=serial.Serial.PARITIES,  textvariable=pari_str)

        port_str.set(self.my_serial.ser.port)
        baud_str.set(self.settings.get("baudrate"))
        bits_str.set(self.settings.get("bytesize"))
        stop_str.set(self.settings.get("stopbits"))
        pari_str.set(self.settings.get("partity"))

        self.port_sp.grid(row=0, column=1)
        self.baud_sp.grid(row=1, column=1)
        self.bits_sp.grid(row=2, column=1)
        self.stop_sp.grid(row=3, column=1)
        self.pari_sp.grid(row=4, column=1)

        return self.baud_sp # Initial focus

    def validate(self):
        try:
            # result = dict([('parity', pari), ('baudrate', baud), ('bytesize', bits), ('stopbits', stop)])
            self.settings['parity'] = str(self.pari_sp.get())
            self.settings['baudrate'] = int(self.baud_sp.get())
            self.settings['bytesize'] = int(self.bits_sp.get())
            self.settings['stopbits'] = int(self.stop_sp.get())

            self.my_serial.ser.port = str(self.port_sp.get())
            self.my_serial.ser.applySettingsDict(self.settings)
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