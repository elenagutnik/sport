import socket

class TCPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect(self.host, self.port)

    def diconnectSocket(self):
        self.socket.close()
        self.socket = None

    def send(self, msg):
        self.socket.send(msg)
