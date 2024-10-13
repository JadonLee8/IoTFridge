# all hardware interfaces
from picozero import pico_temp_sensor, Pot
import machine

class TempSensor:
    def __init__(self):
        self.sensor = pico_temp_sensor

    def celsius(self):
        return self.sensor.temp

    def fahrenheit(self):
        return self.sensor.temp * 9/5 + 32 # type: ignore

class Servo:
    def __init__(self):
        # self.servo = machine.PWM(machine.Pin(16, machine.Pin.OUT))
        self.servo = machine.PWM(16, freq=50)
        self.MAX_DUTY = 65536

    def set_target(self, target):
        self.servo.duty_u16(int((target) * self.MAX_DUTY))
