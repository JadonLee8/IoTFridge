from picozero import pico_temp_sensor, pico_led
from utime import sleep
import network
import socket

# NOTE: This server is designed to work on the TAMU IoT network which uses mac address authorization, thus no key is required.

class Server:
    def __init__(self, ssid):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid)
        while self.wlan.isconnected() == False:
            print(f"Connecting to {ssid}")
            sleep(1)
        self.ip = self.wlan.ifconfig()[0]
        print(f'Connected on {self.ip}')
        self.connection = self.open_socket()
        pico_led.off()
        self.state = 'OFF'


    def open_socket(self):
        # open a socket to server html over
        address = (self.ip, 80)
        connection = socket.socket()
        connection.bind(address)
        # try:
        #     connection.bind(address)
        # except Exception as e:
        #     print(e)
        #     connection.close()
        connection.listen(1)
        return connection

    def webpage(self, temperature):
        html = f"""
                <!DOCTYPE html>
                <html>
                <p>Temperature is {temperature}</p>
                </body>
                </html>
                """
        return str(html)

    def serve(self, tempurature):
        client = self.connection.accept()[0]
        print(client)
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            print('IndexError')
            pass
        if request == '/lighton?':
            pico_led.on()
            self.state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            self.state = 'OFF'
        # TODO: return the request so that fridge power can take in fridge power request as param
        html = self.webpage(tempurature)
        client.send(html)
        client.close()

    # def close_socket(self):
    #     self.connection.close()

