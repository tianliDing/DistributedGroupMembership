
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
        introducer = None

        while True:
            message, address = s.recvfrom(self.bufferSize)
            clientMsg = "Message from Client: {}".format(message.decode('utf8'))
            clientIP = "Client IP Address: {}".format(address)
            print(clientMsg)
            print(clientIP)

            list_of_clients.append(address)

            # add introducer
            if len(list_of_clients) == 1:
                introducer = address[0]
                s.sendto(str.encode("I am introducer"), address)

            # send address to introducer
            if len(list_of_clients) > 1:
                msg = "New member join: ip: " + str(address[0]) + " port: " + str(address[1])
                bytes = str.encode(msg)
                s.sendto(bytes, list_of_clients[0])
                s.sendto(bytesToSend, address)

            print(list_of_clients)


if __name__ == '__main__':
    s = Server()
    s.run()
