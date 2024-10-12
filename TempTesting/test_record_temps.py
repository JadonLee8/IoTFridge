from picozero import pico_temp_sensor
from servo import Servo
import utime
import machine

# NOTE: THIS FILE IS FOR TEST TESTING ONLY. DO NOT RUN FOR THE ACTUAL TEST

data = open("temperature.csv","a") # open file for appending

rtc = machine.RTC()
power_servo = Servo(16) # servo on pin 16
second = 0
total_runtime = 60 # 60 seconds

while second < total_runtime:
    power_servo.write(second)
    temp = pico_temp_sensor.temp
    row = str(temp) + "," + str(second) + ","
    
    timestamp = rtc.datetime()

    for item in timestamp:
        row += str(item) + ","
    
    data.write(row + "\n")
    data.flush()
    
    utime.sleep(1) # log every minute for testing
    second += 1
    
    
data.close()
power_servo.off()

