# all hardware interfaces
from picozero import pico_temp_sensor
from servo import Servo # type: ignore
# NOTE: the type: ignore exists since I didn't fully set up my vs code for rpi pico development
# I will fix this in the future

class TempSensor:
    def __init__(self):
        self.sensor = pico_temp_sensor

    def celsius(self):
        return self.sensor.temp

    def fahrenheit(self):
        return self.sensor.temp * 9/5 + 32 # type: ignore

class FridgePower:
    def __init__(self):
        self.servo = Servo(16)

    def min(self):
        self.servo.write(0)

    def max(self):
        self.servo.write(180)

    # power expressed as a percentage. 1 to 5 inclusive
    def set_power(self, power):
        self.servo.write(int((power-1) * (180/4)))