import serial
import time
import tkMessageBox

FAIL = -1


class PICMessage:
    def __init__(self, name):
        # Message values
        self.start_char = '&'
        self.stop_char = '$'
        self.message_type = dict([("message", "[M]"), ("register", "[R]"), ("ack", "[A]")])
        self.my_name = name

        # Message variables
        self.message_time = time.time()  # Time the message was send/received
        self.sender = ""  # Sender of the message
        self.command = ""  # Command of the message
        self.message = ""  # Message itself
        self.type = "" # Type of the message
        self.id = 0  # An id to add to the message, that will get acknowledged by the receiver if everything is ok

        # Info about PIC
        self.pic_info = PICInfo

    def construct(self, type, command, message, id):
        """
        Construct a message.
        :param type: type of the message as string ("message", "register", "ack")
        :param command: a command to send to other device
        :param message: the message
        :param id: id number of the message
        :return: string with the constructed message
        """
        send_txt = ""
        if self.message_type.__contains__(type):
            if id > 9:
                id = 0
            self.id = id
            send_txt = self.start_char + self.message_type.get(
                type) + ":" + self.my_name + ":" + command + ":" + message + ":" + str(id) + self.stop_char
        print "Output: "+send_txt
        return send_txt

    def convert(self, input_msg):
        """
        Convert the message (from the PIC) to the appropriate message variables
        :param input_msg: The received string
        :return: 1 if OK, -1 if not OK
        """
        self.sender = ""
        self.command = ""
        self.message = ""

        print "Input: "+str(input_msg)

        # Typecast and check
        input_msg = str(input_msg)
        if not input_msg:
            return -1

        if input_msg[0] != self.start_char:
            return -1
        if input_msg[-1] != self.stop_char:
            return -1

        # Remove start character
        input_msg = input_msg[1:-1]

        # Check message type
        try:
            t = input_msg[0:3]
            if t == self.message_type.get("message"):
                input_msg = input_msg[3:]
                m = input_msg.split(":")
                self.type = "message"
                self.sender = m[0]
                self.command = m[1]
                self.message = m[2]
                self.message_time = time.time()
                self.write_to_file()
                return 1
            elif t == self.message_type.get("ack"):
                self.message = input_msg
                self.message_time = time.time()
                self.type = "ack"
                self.pic_info.pic_name = self.sender
                self.pic_info.pic_last_communication = self.message_time
                self.write_to_file()
                return 1
        except IOError:
            return -1

    def write_to_file(self):
        with open("log" + time.strftime("%d:%m:%Y") + ".txt", "a") as uart_log:
            uart_log.write("* time: {}, sender: {}, type: {}, command: {}, message: {}\n".
                format(time.strftime("%H:%M:%S", time.localtime(self.message_time)),
                    self.sender, self.type, self.command, self.message))


class PICInfo:
    def __init__(self):
        self.pic_name = ""
        self.pic_last_communication = time.time()


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


            # # configure the serial connections (the parameters differs on the device you are connecting to)
            # ser = serial.Serial(
            #     port='/dev/ttyUSB0',
            #     baudrate=9600,
            #     parity=serial.PARITY_NONE,
            #     stopbits=serial.STOPBITS_ONE,
            #     bytesize=serial.EIGHTBITS
            # )
            #
            # ser.isOpen()
            #
            # print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
            #
            # input=1
            # while 1 :
            #     # get keyboard input
            #     input = raw_input(">> ")
            #     if input == 'exit':
            #         ser.close()
            #         exit()
            #     else:
            #         # send the character to the device
            #         # (note that I append a \r\n carriage return and line feed to the characters - this is requested by my device)
            #         ser.write(input + '\r\n')
            #         out = ''
            #         # let's wait one second before reading output (let's give device time to answer)
            #         time.sleep(1)
            #         while ser.inWaiting() > 0:
            #             out += ser.read(1)
            #
            #         if out != '':
            #             print ">>" + out
