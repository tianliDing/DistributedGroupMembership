"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""

import socket
import random


class Client:
    def __init__(self):
        self.host = "vpnpool-10-251-40-13.near.illinois.edu"
        self.serverAddressPort = (self.host, 8080)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.memberList = {}

    """
    choose four members to gossip
    """
    def gossipTo(self):
        if len(self.memberList) <= 4:
            for member in self.memberList:
                self.socket.sendto(str.encode("heyhey"), member)
        else:
            tempList = random.choice(self.memberList, 4)
            for member in tempList:
                self.socket.sendto(str.encode("heyhey"), member)

    """
    initialize membership list, include
    address, heartbeat count, (timestamp?)
    """
    def initializeMembership(self, newMemAddr):
        self.memberList['address'] = newMemAddr
        print('membership list:')
        print(self.memberList)
        msgToClient = "heartbeat"
        self.socket.sendto(str.encode(msgToClient), newMemAddr)

    def run(self):
        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        bufferSize = 1024
        self.socket.sendto(bytesToSend, self.serverAddressPort)

        while True:
            msgFromServer = self.socket.recvfrom(bufferSize)
            msg = "Message from Server {}".format(msgFromServer[0])
            print(msg)
            msgList = msg.split()
            print(msgList)
            if msgList[3] == "New":
                print(msgList[-3])
                print(int(msgList[-1]))
                newMemAddr = (msgList[-3], int(msgList[-1]))
                self.initializeMembership(newMemAddr)


if __name__ == '__main__':
    s = Client()
    s.run()
