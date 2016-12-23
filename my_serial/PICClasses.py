import time

pMESSAGE = dict([("message", "[M]"), ("register", "[R]"), ("ack", "[A]"), ("block", "[B]")])
pCOMMAND = dict([("Initialize", "IN"), ("Analog read", "AR"), ("Get name", "GN")])

class PICMessage:
    def __init__(self, name):
        # Message values
        self.start_char = '&'
        self.stop_char = '$'
        self.my_name = name

        # Message variables
        self.message_time = time.time()  # Time the message was send/received
        self.sender = ""  # Sender of the message
        self.command = ""  # Command of the message
        self.message = ""  # Message itself
        self.type = "" # Type of the message
        self.ack_id = 0  # An id to add to the message, that will get acknowledged by the receiver if everything is ok

        # Info about PIC
        self.pic_info = PICInfo

    def construct_message(self, type, command, message, ack_id):
        """
        Construct a message.
        :param type: type of the message as string ("message", "register", "ack")
        :param command: a command to send to other device
        :param message: the message
        :param ack_id: id number of the message
        :return: string with the constructed message
        """
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = self.start_char + pMESSAGE.get(
                type) + ":" + self.my_name + ":"+ str(1) +":" + command + ":" + message + ":" + str(ack_id) + self.stop_char
        return send_txt

    def construct_block(self, type, command, message, length, ack_id):
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = self.start_char + pMESSAGE.get(type) + ":" + self.my_name + ":" + str(length) + ":"

            cnt = 0
            for c in command:
                send_txt += c + ":" + message[cnt] + ":"
                cnt += 1

            send_txt = send_txt + str(ack_id) + self.stop_char
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
            if t == pMESSAGE.get("message"):
                input_msg = input_msg[3:]
                m = input_msg.split(":")
                self.type = "message"
                self.sender = m[0]
                self.command = m[1]
                self.message = m[2]
                self.message_time = time.time()
                self.write_to_file()
                return 1
            elif t == pMESSAGE.get("ack"):
                input_msg = input_msg[3:]
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
