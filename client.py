import socket
from _thread import *

HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client):
    '''서버로부터 메세지를 받는 함수'''

    while True:
        data = client.recv(1024)

        print("recive: {}".format(data.decode()))

start_new_thread(recv_data, (client_socket,)) 
print("** connect server")

while True:
    message = input("")
    if message == 'quit':
        close_data = message
        break
    
    client_socket.send(message.encode())

client_socket.close()