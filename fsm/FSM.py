from my_serial.PICClasses import pCOMMAND
from pid.PID import PID
from fsm.FsmTimer import FsmTimer
from my_serial import PICClasses

# when pic message was 'AR': get val
# try:
#     self.temp_real = float(val)
#     self.temp_real = digital_to_temp(self.temp_real)
#     self.pid.set_point = self.temp_target[self.cnt]  # Point it should be
#     self.cnt += 1
#     pid_output = self.pid.do_work(self.temp_real)
#     self.gui.graph.append_graph(self.temp_real, pid_output)
# except ValueError:
#     pass

# Handle PID values
#         if self.pid.output > 0:
#             self.heater = 'ON'
#             self.fan = 'OFF'
#         elif self.pid.output < 0:
#             self.heater = 'OFF'
#             self.fan = 'ON'
#         else:
#             self.heater = 'OFF'
#             self.fan = 'OFF'
#
#         self.writing_thread.set_heat_and_fan(self.heater, self.fan)

#self.write_event = threading.Event()
#self.writing_thread = WriteThread(self.write_event, self.my_serial, TIME_INTERVAL)
#self.writing_thread.setDaemon(True)

# def start_writing_thread(self):
#     self.my_serial.write_buffer = []
#     self.my_serial.can_write = True
#     self.my_serial.ack_id = 0
#     if not self.write_event.is_set:
#         self.writing_thread.start()
#     else:
#         self.write_event.clear()
#         self.writing_thread = WriteThread(self.write_event, self.my_serial, TIME_INTERVAL)
#         self.writing_thread.setDaemon(True)
#         self.writing_thread.start()

# def stop_writing_thread(self):
#     self.write_event.set()
#     self.writing_thread.join(5)

# if not self.write_event.is_set:
#     self.write_event.set()
#     self.writing_thread.join(5)

class FSM:
    def __init__(self, serial_interface):

        self.fsm_states = {
            "Init": self.fsm_init,
            "Idle": self.fsm_idle,
            "StartUp": self.fsm_start_up,
            "PreHeat": self.fsm_pre_heat,
            "Pid": self.fsm_pid,
            "Stop": self.fsm_stop,
            "Error": self.fsm_error
        }

        # Interfaces
        self.serial_interface = serial_interface
        self.timer = FsmTimer(5)

        # Variables
        self.uart_state = False
        self.door_open_state = False  # State of the door
        self.heater_state = False
        self.fan_state = False
        self.pic_initialized = False
        self.graph_set = False
        self.should_start = False
        self.should_stop = False
        self.first_write = True
        self.sensor_value = 0.0

        # PID values
        self.pid = PID()
        self.pid.configure_pid()
        self.cnt = 0
        self.temp_real = 0.0
        self.temp_target = []

        # FSM
        self.fsm_current_state = "Init"
        self.fsm_next_state = "Init"
        self.do_fsm_tick()

    """
    FSM FUNCTIONS
    """
    def check_inputs(self):
        # Do some stuff
        self.fsm_current_state = self.fsm_next_state

    def do_fsm_tick(self):
        self.check_inputs()
        self.fsm_states[self.fsm_current_state]()
        self.timer.tick()

    """
    FSM STATE METHODS
    """
    def fsm_init(self):
        # Do initialize
        if self.serial_interface.is_ready:
            self.uart_state = True
            self.serial_interface.serial_write(pCOMMAND["Initialize"], "")

        # Next state?
        self.fsm_next_state = "Idle"

    def fsm_idle(self):
        # Next state?
        if self.should_start:
            if self.uart_state and self.graph_set and self.pic_initialized and not self.door_open_state:
                self.fsm_next_state = "StartUp"

    def fsm_start_up(self):
        self.timer.clear_timer()

        # Next state
        self.fsm_next_state = "PreHeat"

    def fsm_pre_heat(self):
        self.heater_state = True
        # Write to serial

        # Next state

    def fsm_pid(self):
        pass

    def fsm_stop(self):
        pass

    def fsm_error(self):
        pass