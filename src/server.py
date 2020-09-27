
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
from datetime import datetime

class Server:
    def __init__(self):
        self.localIP = socket.gethostname()
        print(self.localIP)
        self.localPort = 8080
        self.bufferSize = 1024
        self.list_of_clients = []
        # self.memberList = [{'address': ('10.180.128.255', 2), 'timestamp': "123456"}]

    def main_func(self, s):
        while True:
            message, address = s.recvfrom(self.bufferSize)
            self.printMsg(message, address)
            msgList = message.decode('utf8').split()
            print(msgList[0])

            if msgList[0] == "Alive": #listen for client leave
                for client in self.list_of_clients:
                    if client['address'] == address:
                        client['timestamp'] = self.getCurrentTimestamp()
                        break

            else: #normal listen for connection
                self.list_of_clients.append({'address': address, 'timestamp': self.getCurrentTimestamp()})
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
                    s.sendto(bytes, self.list_of_clients[0]['address'])
                print("CLIENT LIST", self.list_of_clients)

            for cur in self.list_of_clients:
                if int(self.getCurrentTimestamp()) - int(cur['timestamp']) > 10:
                    print('-------------------leaveIP: --------------------')
                    print(cur['address'])
                    self.list_of_clients.remove(cur)
                    #send message to all client to remove curAddress

    def getCurrentTimestamp(self):
        now = datetime.now()
        current_time = now.strftime("%H%M%S")       # "%H%M%S%f"
        return current_time

    def check_leave(self, s):
        while True:
            for client in self.list_of_clients:
                s.sendto(str.encode("Check whether you disconnect"), client['address'])
            time.sleep(5)

    def run(self):
        # Create a socket, parameter: Internet, UDP
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        s.bind((self.localIP, self.localPort))
        print("UDP server up and listening")
        introducer = None

        t = threading.Thread(target=self.main_func, args=(s,))
        w = threading.Thread(target=self.check_leave, args=(s,))
        t.start()
        w.start()


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
