from LAN_Server import Server
from Hardware import TempSensor, Servo
import machine

# Create a server object
server = None
try:
    server = Server('TAMU_IoT')
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    machine.reset()

temp_sensor = TempSensor()
fridge_power = Servo()

tempurature = 0
power = 40
last_power = 40

# Run the server
try:
    while True:
        tempurature = temp_sensor.fahrenheit()
        power = server.serve(tempurature)
        power = min(53, max(32, power))
        fridge_power.set_target(((power - 30) / (55-30)))
        print(f"{((power - 29.9) / (55-29.8)):.3f}")


except KeyboardInterrupt:
    print("KeyboardInterrupt")
    if server:
        server.close_socket() # type: ignore
    machine.reset()