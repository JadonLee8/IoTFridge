from LAN_Server import Server
from Hardware import TempSensor, Servo
import machine
import uasyncio as asyncio

# TODO: this is a hardware todo. Make button to hard reset pico by shorting run and ground pins

# Create a server object
server = None
try:
    server = Server('TAMU_IoT')
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    machine.reset()

temp_sensor = TempSensor()
fridge_power = Servo()

temperature = 0
power = 4
last_power = 4

# Async function to handle the server
async def handle_server():
    global power
    while True:
        power = server.serve(temp_sensor.fahrenheit()) # type: ignore
        await asyncio.sleep(0.1)  # Add a small delay to yield control

# Async function to update fridge power
async def update_fridge_power():
    global last_power
    while True:
        print(f"Current Pos: {fridge_power.current_pos}")
        if power != last_power:
            fridge_power.set_target(((power - 1) / 4) * 216)  # Map power to servo position
        last_power = power
        fridge_power.update()
        await asyncio.sleep(0.01)  # Small delay to prevent maxing out CPU

# Main entry point
async def main():
    # Start both tasks concurrently
    await asyncio.gather(handle_server(), update_fridge_power()) # type: ignore

# Run the event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    if server:
        server.close_socket()  # type: ignore
    machine.reset()
