from picozero import pico_temp_sensor, pico_led
from utime import sleep
import network
import socket

# NOTE: This server is designed to work on the TAMU IoT network which uses mac address authorization, thus no key is required.

class Server:
    def __init__(self, ssid):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        while not self.wlan.isconnected():
            print(f"Connecting to {ssid}")
            sleep(1)
        self.ip = self.wlan.ifconfig()[0]
        print(f'Connected on {self.ip}')
        self.connection = self.open_socket()


    def open_socket(self):
        # open a socket to server html over
        address = (self.ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        return connection

    def webpage(self, temperature, state):
        html = f"""
                <!DOCTYPE html>
                <html>
                <form action="./lighton">
                <input type="submit" value="Light on" />
                </form>
                <form action="./lightoff">
                <input type="submit" value="Light off" />
                </form>
                <p>LED is {state}</p>
                <p>Temperature is {temperature}</p>
                </body>
                </html>
                """
        return str(html)

    def serve(self, tempurature):
        client = self.connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            print('IndexError')
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        html = self.webpage(tempurature, state)
        client.send(html)
        client.close()

