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
            return "Connection success"
        except socket.error as e:
            return "Caught exception socket.error : %s" % e

    def send(self, msg):
        try:
            self.sock.send(msg)
            return True
        except:
            return False
