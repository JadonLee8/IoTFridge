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
        self.power = 2.5


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

    def webpage(self, temperature, power):
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>IoT Fridge</title>
            </head>
            <body>
                <h1>IoT Fridge</h1>

                <!-- Form that submits via GET -->
                <form action="/setpower" method="GET">
                    <label for="powerRange">Set Power:</label>
                    <input type="range" id="powerRange" name="value" min="1" max="5" step="0.1" value="{power}" oninput="updatePowerValue(this.value)">
                    <span id="powerValue">{power}</span>
                    <br>
                    <button type="submit">Set Power</button>
                </form>

                <script>
                    function updatePowerValue(value) {{
                        document.getElementById('powerValue').textContent = value;
                    }}
                </script>

                <p>Temperature is {temperature}</p>
                <p>Power is {power}</p>
            </body>
            </html>
            """
        return str(html)

    def serve(self, tempurature):
        client = self.connection.accept()[0]
        request = client.recv(1024)
        request = request.decode()
        print(request)
        try:
            request = request.split()[1]
            print(request)
        except IndexError:
            print('IndexError')
            pass
        if '/setpower?' in request:
            self.power = float(request.split('=')[1])
            print(self.power)
        html = self.webpage(tempurature, self.power)
        client.send(html)
        client.close()
        return self.power

    # def close_socket(self):
    #     self.connection.close()

