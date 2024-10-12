# all hardware interfaces
from picozero import pico_temp_sensor, Pot
import machine
from pid import PID_Controller

class TempSensor:
    def __init__(self):
        self.sensor = pico_temp_sensor

    def celsius(self):
        return self.sensor.temp

    def fahrenheit(self):
        return self.sensor.temp * 9/5 + 32 # type: ignore

class Servo:
    def __init__(self):
        self.speed = machine.PWM(machine.Pin(17, machine.Pin.OUT))
        self.pin1 = machine.Pin(15, machine.Pin.OUT)
        self.pin2 = machine.Pin(16, machine.Pin.OUT)
        self.read_potentiometer = Pot(0)
        self.current_pos = self.read_potentiometer.value
        self.pid = PID_Controller(0.1, 0, 0, 216)
        self.target_pos = 216
        self.MAX_DUTY = 65536
        self.speed.freq(1000)

    def update(self):
        self.current_pos = int(self.read_potentiometer.value * 216)
        output = self.pid.update(self.current_pos)
        self.speed.duty_u16(abs(int(output * self.MAX_DUTY)))
        print(f"Output: {output}    Current Pos: {self.current_pos}    Target Pos: {self.target_pos}    Duty: {abs(int(output * self.MAX_DUTY))}")
        if output > 0:
            self.pin1.high()
            self.pin2.low()
        else:
            self.pin1.low()
            self.pin2.high()

    def set_target(self, target):
        self.target_pos = target
        self.pid.set_setpoint(target)
