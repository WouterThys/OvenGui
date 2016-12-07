class PID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.setPoint = 0.0     # Desired value
        self.error = 0.0        # Error between desired and measured value
        self.prev_error = 0.0   # Previous error
        self.dt = 1.0     # Time interval in which every cycle happens

        self.integrator = 0.0
        self.windup = 1000      # To counter large oscillations

        self.output = 0.0

    # Integrator part
    def integrate(self, error):
         i = self.integrator + error*self.dt
         if i > self.windup:
             return 0
         else:
             self.integrator += (error*self.dt)
             return self.integrator

    # Differential part
    def differentiate(self, error):
        return ((self.error - self.prev_error) / self.dt)

    # Proportional part
    def proportional(self, error):
        return error

    # Do the actual calculation
    def do_work(self, measured_value):
        # Calculate the error
        self.error = self.setPoint - measured_value

        # Calculate P I and D values
        P = self.Kp * self.proportional(self.error)
        I = self.Ki * self.integrate(self.error)
        D = self.Kd * self.differentiate(self.error)

        # Calculate the output
        self.output = P + I + D

        # Set values for next iteration
        self.prev_error = self.error

        return self.output


