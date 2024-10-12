
class PID_Controller:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0

    def update(self, current_value):
        error = current_value - self.setpoint
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        return max(min(output, 1), -1)

    def set_setpoint(self, setpoint, reset_integral=True):
        self.setpoint = setpoint
        self.integral = 0 if reset_integral else self.integral
        self.prev_error = 0