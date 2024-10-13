from servo import Servo
from picozero import Pot
import utime

my_servo = Servo(16)
my_pot = Pot(0)

try:
    while True:
        for i in range(181):
            my_servo.write(i)
            utime.sleep(.03)
            print(my_pot.value)
        
        for i in reversed(range(181)):
            my_servo.write(i)
            utime.sleep(.03)
            print(my_pot.value)
except KeyboardInterrupt:
    my_servo.off()
        


