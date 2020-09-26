"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""

import socket
import random
import json
from datetime import datetime


class Client:
    def __init__(self):
        self.host = "Tianlis-MacBook-Pro.local"
        self.serverAddressPort = (self.host, 8080)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.memberList = [{'address': (1,2), 'timestamp': "123456"}]       # for testing

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
    add new join to introducer's membership list, include
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
            msg, IP = self.socket.recvfrom(bufferSize)
            msg = "MESSAGE: {}".format(msg.decode('utf8'))
            IP = "FROM: {}".format(IP)
            self.printMsg(msg, IP)
            msgList = msg.split()

            # only introducer will get msg "MESSAGE: New member join: ip: xxxxx port: xxxxx"
            if msgList[1] == "New":
                newMemAddr = (msgList[-3], int(msgList[-1]))
                # introducer send own membership to new comer, then add new node into own list
                mlStr = json.dumps(self.memberList[0])
                self.socket.sendto(str.encode(mlStr), newMemAddr)
                self.addMember(newMemAddr)

    def printML(self):
        print("==================================================================")
        print("ADDRESS                              TIMESTAMP                    ")
        for member in self.memberList:
            print(member['address'], "               ", member['timestamp'])
        print("==================================================================")

    def printMsg(self, msg, IP):

        print("==================================================================")
        print(msg)
        print(IP)
        print("==================================================================")


if __name__ == '__main__':
    s = Client()
    s.run()
