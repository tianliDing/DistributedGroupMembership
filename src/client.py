"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""
import threading
import time
import socket
import random
import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class Client:
    def __init__(self):
        self.host = "vpnpool-10-251-36-157.near.illinois.edu"
        self.serverAddressPort = (self.host, 8080)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # self.memberList = [{'address': ('10.180.128.255', 2), 'timestamp': "123456"}]       # for testing
        self.memberList = []
        self.ip = None
        self.port = None
        self.address = None
        self.lastTime = None

    def jsonToStr(self):
        strML = "LIST: "
        # for member in self.memberList:
        strML += json.dumps(self.memberList)
        return strML

    """
    choose four members to gossip
    """
    def gossipTo(self):
        self.lastTime = self.getCurrentTimestamp()
        strML = self.jsonToStr()
        tempList = self.memberList
        if len(self.memberList) > 4:
            tempList = random.sample(self.memberList, 4)
        for member in tempList:
            if self.address is not None and tuple(member['address']) != self.address:
                self.socket.sendto(str.encode(strML), tuple(member['address']))

        for cur in self.memberList:
            if int(self.getCurrentTimestamp()) - int(cur['timestamp']) >= 4:
                self.memberList.remove(cur)
        self.printML()

    def getCurrentTimestamp(self):
        now = datetime.now()
        current_time = now.strftime("%H%M%S")       # "%H%M%S%f"
        return current_time

    # send heartbeat every 5 seconds
    def sendHb(self):
        sched = BlockingScheduler()
        sched.add_job(self.gossipTo, 'cron', second='0-59/1')
        sched.start()

    """
    add new join to introducer's membership list, include address, timestamp
    """
    def addMember(self, newMemAddr):
        newMember = {'address': newMemAddr, 'timestamp': self.getCurrentTimestamp()}
        self.memberList.append(newMember)

    def main_func(self, bufferSize):
        while True:
            message, address = self.socket.recvfrom(bufferSize)
            msg = "MESSAGE: {}".format(message.decode('utf8'))
            IP = "FROM: {}".format(address)
            msgList = msg.split()

            # set own address
            if len(msgList) >= 9 and msgList[5] == "address":
                self.printMsg(msg, IP)
                self.ip = msgList[7]
                self.port = int(msgList[9])
                self.address = (self.ip, self.port)
                # self.memberList.append({'address': self.address, 'timestamp': self.getCurrentTimestamp()})

            # if introducer get new node
            if msgList[1] == "New":
                self.printMsg(msg, IP)
                newMemAddr = (msgList[-3], int(msgList[-1]))
                self.addMember(newMemAddr)

            # msg from other nodes
            elif msgList[1] == "LIST:":
                if msgList[2] != "[]":
                    newMsg = msg[15:]
                    jsonML = json.loads(newMsg)

                    # append the sender to its member list
                    jsonML.append({'address': address, 'timestamp': self.getCurrentTimestamp()})
                    for new in jsonML:
                        flag = 0
                        for cur in self.memberList:
                            if tuple(new['address']) == tuple(cur['address']):
                                flag = 1
                                if int(new['timestamp']) > int(cur['timestamp']):
                                    cur['timestamp'] = new['timestamp']
                        if flag == 0 and int(self.getCurrentTimestamp()) - int(new['timestamp']) < 4:
                            newMember = {'address': tuple(new['address']), 'timestamp': new['timestamp']}
                            self.memberList.append(newMember)

    def run(self):
        bytesToSend = str.encode("Hello UDP Server")
        self.socket.sendto(bytesToSend, self.serverAddressPort)

        bufferSize = 1024
        t = threading.Thread(target=self.main_func, args=(bufferSize,))
        w = threading.Thread(target=self.sendHb)
        t.start()
        w.start()

    def printML(self):
        print("ADDRESS                              TIMESTAMP                    ")
        for member in self.memberList:
            print(member['address'], "               ", member['timestamp'])
        print("==================================================================")

    def printMsg(self, msg, IP):
        print(msg)
        print(IP)
        print("==================================================================")


if __name__ == '__main__':
    s = Client()
    s.run()
