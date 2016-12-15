from settings.Settings import read_settings, PID_SETTINGS


class PID:
    def __init__(self, p=20, i=0.005, d=0.01):
        self.Kp = p
        self.Ki = i
        self.Kd = d

        self.set_point = 0.0     # Desired value
        self.error = 0.0        # Error between desired and measured value
        self.prev_error = 0.0   # Previous error
        self.dt = 1.0     # Time interval in which every cycle happens

        self.integrator = 0.0
        self.Wu = 1000      # To counter large oscillations

        self.output = 0.0

    def configure_pid(self):
        pid_settings = read_settings(PID_SETTINGS)
        self.Kp = pid_settings['Kp']
        self.Ki = pid_settings['Ki']
        self.Kd = pid_settings['Kd']
        self.Wu = pid_settings['Wu']
        self.dt = pid_settings['dt']

    # Integrator part
    def integrate(self, error):
        i = self.integrator + error*self.dt
        if abs(i) > self.Wu:
            return 0
        else:
            self.integrator += (error*self.dt)
            return self.integrator

    # Differential part
    def differentiate(self, error):
        return (self.error - self.prev_error) / self.dt

    # Proportional part
    def proportional(self, error):
        return error

    # Do the actual calculation
    def do_work(self, measured_value):
        # Calculate the error
        self.error = self.set_point - measured_value

        # Calculate P I and D values
        P = self.Kp * self.proportional(self.error)
        I = self.Ki * self.integrate(self.error)
        D = self.Kd * self.differentiate(self.error)

        # Calculate the output
        self.output = P + I + D

        # Set values for next iteration
        self.prev_error = self.error

        return self.output


