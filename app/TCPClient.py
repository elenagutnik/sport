import socket
from config import Config

class DataSender:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        try:
            self.sock.connect((Config.SCOREBOARD_HOST, Config.SCOREBOARD_PORT))
            return True
        except socket.error:
            return False

    def send(self, msg):
        self.sock.send(msg)

    def close(self):
        self.sock.close()
