import serial
import tkMessageBox
from PICClasses import PICMessage
from settings.Settings import read_settings, UART_SETTINGS

FAIL = -1

WRITE_STATE_CHECK = 1
WRITE_STATE_WRITE = 2
WRITE_STATE_ACK = 3


class SerialInterface:
    def __init__(self):
        self.isReady = False
        self.ack_id = 0
        self.ser = None

        self.write_buffer = []
        self.can_write = True

    def configure_serial(self):
        uart_settings = read_settings(UART_SETTINGS)

        try:
            if (self.ser is not None) and (self.ser.isOpen()):
                self.ser.close()
            self.ser = serial.Serial(
                port=uart_settings["com_port"],
                baudrate=uart_settings["baud_rate"],
                parity=uart_settings["parity"],
                stopbits=uart_settings["stop_bits"],
                bytesize=uart_settings["data_bits"]
            )
            print self.ser
        except ValueError as e:
            tkMessageBox.showerror("Serial error", "Invalid value: "+e.message)
        except serial.SerialException as e:
            tkMessageBox.showerror("Serial error", "Error opening port: "+e.message)

        if self.ser is not None:
            self.isReady = self.ser.isOpen()
        else:
            self.isReady = False

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
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
            except Exception as e:
                tkMessageBox.showerror("Serial error", "Error clearing input buffer: "+e.message)
        else:
            tkMessageBox.showerror("Serial error", "Serial port is not open")
            return FAIL

    def serial_destroy(self):
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
                self.ser.close()
            except Exception as e:
                tkMessageBox.showerror("Serial error", "Error closing serial: " + e.message)
        else:
            tkMessageBox.showerror("Serial error", "Serial port is not open")

    """
        SERIAL READ
    """
    def serial_read(self):
        if self.ser.isOpen():
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
                return FAIL
        else:
            tkMessageBox.showerror("Serial error", "Serial port is not open")
            return FAIL

    """
        SERIAL WRITE
    """
    def serial_write(self, command, message):
        if self.ser.isOpen():
            if len(self.write_buffer) > 9:
                return FAIL
            self.ack_id += 1
            if self.ack_id >= 9:
                self.ack_id = 0
            msg = PICMessage("Compy")
            txt = msg.construct_message("message", command, message, self.ack_id)
            self.write_buffer.append(txt)
            if self.can_write:
                self.check_write_buffer()
            return self.ack_id
        else:
            return FAIL

    def serial_write_block(self, command, message, count):
        if self.ser.isOpen():
            if len(self.write_buffer) > 9:
                return FAIL
            self.ack_id += 1
            if self.ack_id >= 9:
                self.ack_id = 0
            msg = PICMessage("Compy")
            txt = msg.construct_block("block", command, message, count, self.ack_id)
            self.write_buffer.append(txt)
            if self.can_write:
                self.check_write_buffer()
            return self.ack_id
        else:
            return FAIL


    def check_write_buffer(self):
        if len(self.write_buffer) > 0:
            self.can_write = False
            self.do_write(self.write_buffer[0])
        else:
            self.can_write = True

    def do_write(self, msg):
        print "Output: "+msg
        self.ser.write(msg + '\r\n')

    def acknowledge(self, ack_id):
        for msg in self.write_buffer:
            if msg[-2] == ack_id:
                self.write_buffer.remove(msg)
                self.can_write = True
                self.check_write_buffer()