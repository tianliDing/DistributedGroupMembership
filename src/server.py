
"""
global membership list
id count
log to record join, leave, fail
type var: gossip / membership list

VM:
fa20-cs425-g48-XX.cs.illinois.edu

"""

import socket


class Server:
    def __init__(self):
        self.localIP = socket.gethostname()
        print(self.localIP)
        self.localPort = 8080
        self.bufferSize = 1024

    def run(self):
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)
        # Create a socket, parameter: Internet, UDP
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        s.bind((self.localIP, self.localPort))
        print("UDP server up and listening")

        list_of_clients = []
        while True:
            message, address = s.recvfrom(self.bufferSize)
            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)
            print(clientMsg)
            print(clientIP)
            list_of_clients.append(address)
            # Sending a reply to client
            s.sendto(bytesToSend, address)
            print(list_of_clients)


if __name__ == '__main__':
    s = Server()
    s.run()
