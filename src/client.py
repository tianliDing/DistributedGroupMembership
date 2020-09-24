"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""

import socket


class Client:
    def __init__(self):
        self.serverAddressPort = ("vpnpool-10-250-8-86.near.illinois.edu", 8080)

    def run(self):
        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        print(1)
        bufferSize = 1024
        print(2)
        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        print(3)
        UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        print(4)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)


if __name__ == '__main__':
    s = Client()
    s.run()
