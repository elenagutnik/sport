import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 7001)
sock.bind(server_address)

sock.listen(1)


connection, client_address = sock.accept()
while True:
    data = connection.recv(1024)
    if not data:break
    print(data)



