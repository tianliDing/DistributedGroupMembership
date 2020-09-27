
"""
global membership list
id count
log to record join, leave, fail
type var: gossip / membership list

VM:
fa20-cs425-g48-XX.cs.illinois.edu

"""

import socket
import threading
import time

class Server:
    def __init__(self):
        self.localIP = socket.gethostname()
        print(self.localIP)
        self.localPort = 8080
        self.bufferSize = 1024
        self.list_of_clients = []

    def main_func(self, s):
        while True:
            message, address = s.recvfrom(self.bufferSize)
            self.printMsg(message, address)
            self.list_of_clients.append(address)

            msgFromServer = "Hello UDP Client, your address is {} and {}".format(address[0], address[1])
            bytesToSend = str.encode(msgFromServer)
            s.sendto(bytesToSend, address)

            # add introducer
            if len(self.list_of_clients) == 1:
                introducer = address[0]
                s.sendto(str.encode("I am introducer"), address)

            # send address to introducer
            if len(self.list_of_clients) > 1:
                msg = "New member join: ip: " + str(address[0]) + " port: " + str(address[1])
                bytes = str.encode(msg)
                s.sendto(bytes, self.list_of_clients[0])
            print("CLIENT LIST", self.list_of_clients)

    # # every 10 sec, send to all clients, let them start send heartbeat
    # def sendHb(self, s):
    #     while True:
    #         for client in self.list_of_clients:
    #             msgFromServer = "Start gossip!"
    #             bytesToSend = str.encode(msgFromServer)
    #             s.sendto(bytesToSend, client)
    #         print('sent start gossip')
    #         time.sleep(10)

    def run(self):
        # Create a socket, parameter: Internet, UDP
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        s.bind((self.localIP, self.localPort))
        print("UDP server up and listening")
        introducer = None
        self.main_func(s)
        # t = threading.Thread(target=self.main_func, args=(s,))
        # w = threading.Thread(target=self.sendHb, args=(s,))
        # t.start()
        # w.start()


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
