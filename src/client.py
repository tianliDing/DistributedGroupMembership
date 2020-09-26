"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""

import socket
import random
from datetime import datetime


class Client:
    def __init__(self):
        self.host = "Tianlis-MacBook-Pro.local"
        self.serverAddressPort = (self.host, 8080)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.memberList = []

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
    address, timestamp
    """
    def addMember(self, newMemAddr):
        # add address
        newMember = {'address': newMemAddr}
        msgToClient = "heartbeat"
        self.socket.sendto(str.encode(msgToClient), newMemAddr)
        # add timestamp
        newMember['timestamp'] = self.getCurrentTimestamp()
        self.memberList.append(newMember)
        print('membership list:')
        self.printML()

    def printML(self):
        print("==================================================================")
        print("ADDRESS                              TIMESTAMP                    ")
        for member in self.memberList:
            print(member['address'], "               ", member['timestamp'])
        print("==================================================================")

    def getCurrentTimestamp(self):
        now = datetime.now()
        current_time = now.strftime("%H%M%S%f")
        return current_time

    def run(self):
        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        bufferSize = 1024
        self.socket.sendto(bytesToSend, self.serverAddressPort)

        while True:
            msgFromServer = self.socket.recvfrom(bufferSize)
            msg = "Message from Server: {}".format(msgFromServer[0].decode('utf8'))
            print(msg)
            msgList = msg.split()
            print(msgList)
            if msgList[3] == "New":
                print(msgList[-3])
                print(int(msgList[-1]))
                newMemAddr = (msgList[-3], int(msgList[-1]))
                self.addMember(newMemAddr)


if __name__ == '__main__':
    s = Client()
    s.run()
