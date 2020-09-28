
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


class Server:
    def __init__(self):
        self.localIP = socket.gethostname()
        print(self.localIP)
        self.localPort = 8080
        self.bufferSize = 2000
        self.list_of_clients = []

    def run(self):
        """
        start server, deal with messages
        """
        # Create a socket, parameter: Internet, UDP
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        s.bind((self.localIP, self.localPort))
        print("UDP server up and listening")

        t = threading.Thread(target=self.main_func, args=(s,))
        w = threading.Thread(target=self.switchMode, args=(s, ))
        t.start()
        w.start()

    def main_func(self, s):
        """
        for server to receive message from clients and process
        :param s: socket
        """
        while True:
            message, address = s.recvfrom(self.bufferSize)
            self.printMsg(message, address)
            self.list_of_clients.append(address)

            #send reply to connected client
            msgFromServer = "Hello UDP Client, your address is {} and {}".format(address[0], address[1])
            bytesToSend = str.encode(msgFromServer)
            s.sendto(bytesToSend, address)

            # add introducer
            if len(self.list_of_clients) == 1:
                s.sendto(str.encode("I am introducer"), address)

            # send address to introducer
            if len(self.list_of_clients) > 1:
                msg = "New member join: ip: " + str(address[0]) + " port: " + str(address[1])
                bytes = str.encode(msg)
                s.sendto(bytes, self.list_of_clients[0])
            print("CLIENT LIST", self.list_of_clients)

    def switchMode(self, s):
        """
        switch mode between alltoall and gossip
        :param s: socket
        """
        while True:
            inp = input()
            if inp == "all":
                print('--------Alltoall Mode Start--------')
                for client in self.list_of_clients:
                    s.sendto(str.encode("all"), client)
            elif inp == "gossip":
                print('--------Gossip Mode Start---------')
                for client in self.list_of_clients:
                    s.sendto(str.encode("gossip"), client)

    def printMsg(self, msg, IP):
        """
        format output
        :param msg: main text of the message
        :param IP: address of the message
        """
        msg = "MESSAGE: {}".format(msg.decode('utf8'))
        IP = "FROM: {}".format(IP)
        print("==================================================================")
        print(msg)
        print(IP)
        print("==================================================================")


if __name__ == '__main__':
    s = Server()
    s.run()
