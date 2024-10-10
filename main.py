from LAN_Server import Server

# Create a server object
server = Server('TAMU IoT')

# Run the server
while True:
    server.serve(tempurature=0)