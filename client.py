import os
from socket import *
import argparse
import threading

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.connect(('127.0.0.1', 10001))


def receive(client_socket, i):
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("Disconnected")
            break
        data = data.decode()
        print(data)


def send(client_socket, i):
    while 1:
        data = input()
        client_socket.sendall(data.encode())
        if data == "/q":
            break
    server_socket.close()


receive_thread = threading.Thread(target=receive, args=(server_socket, ""))
receive_thread.start()
send_thread = threading.Thread(target=send, args=(server_socket, ""))
send_thread.start()
