import serial
import tkMessageBox
from PICClasses import PICMessage

FAIL = -1


class SerialInterface:
    def __init__(self):
        self.isReady = False
        self.ser = serial.Serial()
        self.configure_serial(None)
        self.serial_clear()
        self.id = 0

    def configure_serial(self, settings):
        if settings is None:
            try:
                if self.ser.isOpen():
                    self.ser.close()
                port = self.serial_ports()
                if len(port) > 0:
                    self.ser = serial.Serial(
                        port=port[0],
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=5
                    )
            except ValueError as e:
                tkMessageBox.showerror("Serial error", "Invalid value: "+e.message)
            except serial.SerialException as e:
                tkMessageBox.showerror("Serial error", "Error opening port: "+e.message)

        else:
            s = settings.serial_settings
            try:
                if self.ser.isOpen():
                    self.ser.close()
                # self.ser = serial.Serial(
                #     port=s.com_port,
                #     baudrate=s.baud_rate,
                #     parity=s.parity,
                #     stopbits=s.stop_bits,
                #     bytesize=s.data_bits
                # )
                self.ser = serial.Serial(
                    port='/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=5
                )
            except ValueError as e:
                tkMessageBox.showerror("Serial error", "Invalid value: "+e.message)
            except serial.SerialException as e:
                tkMessageBox.showerror("Serial error", "Error opening port: "+e.message)
        self.isReady = self.ser.isOpen()
        print self.ser.getSettingsDict()

    @staticmethod
    def serial_ports():
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        import sys
        import glob
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
            except (OSError, serial.SerialException):
                pass
        return result

    def serial_has_input(self):
        try:
            return self.ser.inWaiting()
        except Exception:
            pass

    def serial_clear(self):
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
        except Exception as e:
            tkMessageBox.showerror("Serial error", "Error clearing input buffer: "+e.message)

    def serial_destroy(self):
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.close()
        except Exception as e:
            tkMessageBox.showerror("Serial error", "Error closing serial: " + e.message)

    def serial_read(self):
        try:
            if self.isReady:
                out = ""
                c = ''
                cnt = 0
                while c != '$':
                    c = self.ser.read(1)
                    if not c:
                        return FAIL
                    out += c
                    cnt += 1
                    if cnt > 500:  # Takes way to long before stop character came
                        return FAIL
                return str(out)
        except Exception as e:
            tkMessageBox.showerror("Serial error", "Error reading: "+e.message)
            return -1

    def serial_write(self, command, message):
        self.id += 1
        if self.id >= 9:
            self.id = 0
        msg = PICMessage("Compy")
        txt = msg.construct("message", command, message, self.id)
        self.ser.write(txt+'\r\n')