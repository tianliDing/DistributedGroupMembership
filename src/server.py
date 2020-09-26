
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

        # Create a socket, parameter: Internet, UDP
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        s.bind((self.localIP, self.localPort))
        print("UDP server up and listening")

        list_of_clients = []
        introducer = None

        while True:
            message, address = s.recvfrom(self.bufferSize)
            self.printMsg(message, address)
            list_of_clients.append(address)

            msgFromServer = "Hello UDP Client, your address is {}".format(address)
            bytesToSend = str.encode(msgFromServer)
            s.sendto(bytesToSend, address)

            # add introducer
            if len(list_of_clients) == 1:
                introducer = address[0]
                s.sendto(str.encode("I am introducer"), address)

            # send address to introducer
            if len(list_of_clients) > 1:
                msg = "New member join: ip: " + str(address[0]) + " port: " + str(address[1])
                bytes = str.encode(msg)
                s.sendto(bytes, list_of_clients[0])


            print("CLIENT LIST", list_of_clients)

    def printMsg(self, msg, IP):
        msg = "MESSAGE: {}".format(msg.decode('utf8'))
        IP = "FROM: {}".format(IP)
        print("==================================================================")
        print(msg)
        print(IP)
        print("==================================================================")


if __name__ == '__main__':
    s = Server()
    s.run()
