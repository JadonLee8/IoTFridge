from servo import Servo
import utime

my_servo = Servo(16)

try:
    while True:
        for i in range(181):
            my_servo.write(i)
            utime.sleep(.03)
        
        for i in reversed(range(181)):
            my_servo.write(i)
            utime.sleep(.03)
except KeyboardInterrupt:
    my_servo.off()
        


