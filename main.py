from LAN_Server import Server
from Hardware import TempSensor, FridgePower
import machine

# Create a server object
server = None
try:
    server = Server('TAMU_IoT')
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    machine.reset()

temp_sensor = TempSensor()
fridge_power = FridgePower()

tempurature = 0

# Run the server
try:
    while True:
        tempurature = temp_sensor.fahrenheit()
        server.serve(tempurature)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    if server:
        server.close_socket() # type: ignore
    machine.reset()