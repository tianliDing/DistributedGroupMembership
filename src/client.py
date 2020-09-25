"""
for each client:
- own membership list recording nodes that receives heartbeat from
- gossip: send to 4 nodes [upto 3 failures]
- all-to-all: send to all except itself
"""

import socket


class Client:
    def __init__(self):
        self.host = "vpnpool-10-251-40-13.near.illinois.edu"
        self.serverAddressPort = (self.host, 8080)
        self.memberList = []

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
        while True:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            msg = "Message from Server {}".format(msgFromServer[0])
            print(msg)
            msgList = msg.split()
            print(msgList)
            if (msgList[3] == "New"):
                print(msgList[-3])
                print(int(msgList[-1]))

                msgToClient = "heartbeat"

                newMemAddr = (msgList[-3], int(msgList[-1]))
                self.memberList.append(newMemAddr)
                print('membership list:')
                print(self.memberList)

                UDPClientSocket.sendto(str.encode(msgToClient), newMemAddr)



if __name__ == '__main__':
    s = Client()
    s.run()
