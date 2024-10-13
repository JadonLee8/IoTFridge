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
        self.power = 40


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

# TODO: give user opyion to change to celcius
# TODO: also give user option to type in power. make sure to include input validation
    def webpage(self, temperature, power):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>IoT Fridge</title>
            <style>
                body {{
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <h1 style="font-family: Arial, sans-serif; color: #2c3e50; text-align: center; background-color: #ecf0f1; padding: 20px 0; margin: 0;">IoT Fridge</h1>

            <!-- Form that submits via GET -->
            <div style="text-align: center;">
                <form action="/setpower" method="GET" style="font-family: Arial, sans-serif; color: #34495e; display: inline-block; text-align: center;">
                    <label for="powerRange" style="font-family: Arial, sans-serif; color: #34495e;">Set Temp:</label>
                    <input type="range" id="powerRange" name="value" min="30" max="55" step="0.1" value="{power}" oninput="updatePowerValue(this.value)" style="margin: 10px 0;">
                    <span id="powerValue" style="font-family: Arial, sans-serif; color: #34495e;">{power}</span>
                    <br>
                    <button type="submit" style="background-color: #3498db; color: white; border: none; padding: 10px 20px; cursor: pointer;">Set Power</button>
                </form>

                <script>
                    function updatePowerValue(value) {{
                        document.getElementById('powerValue').textContent = value;
                    }}
                </script>

                <p style="font-family: Arial, sans-serif; color: #34495e;">Temperature is {temperature} f</p>
                <p style="font-family: Arial, sans-serif; color: #34495e;">Setting is {power} f</p>
                <div style="text-align: center; margin-top: 100px"></div>
                    <p style="font-family: Arial, sans-serif; color: #34495e;">Made by Jadon Lee</p>
                    <p style="font-family: Arial, sans-serif; color: #34495e;">Github: <a href="https://github.com/JadonLee8" style="color: #3498db;">https://github.com/JadonLee8</a></p>
                </div>
            </div>

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

