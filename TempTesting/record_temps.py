from picozero import pico_temp_sensor
from servo import Servo
import utime
import machine

data = open("temperature.csv","a") # open file for appending

rtc = machine.RTC()
power_servo = Servo(16) # servo on pin 16
minute = 1
total_runtime = 3 * 60 # 3 hours to minutes

while minute < total_runtime:
    power_servo.write(minute)
    temp = pico_temp_sensor.temp
    row = str(temp) + "," + str(minute) + ","
    
    timestamp = rtc.datetime()

    for item in timestamp:
        row += str(item) + ","
    
    data.write(row + "\n")
    data.flush()
    
    utime.sleep(60) # log every minute for testing
    minute += 1
    
    
data.close()
power_servo.off()
