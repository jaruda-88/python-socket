import socket
from _thread import *

# 서버에 접속한 클라이언트
client_sockets = []

def threaded(client_socket, addr):
    print('** Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data:
                print('** Disconnected by ' + addr[0], ':', addr[1])
                break

            print('Received from ' + addr[0], ':', addr[1], data.decode())

            # 서버에 접속한 클라이언트들에게 채팅 보내기
            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            for client in client_sockets :
                if client != client_socket :
                    client.send(data)

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets :
        client_sockets.remove(client_socket)
        print('remove client list : ',len(client_sockets))

    client_socket.close()

HOST = '127.0.0.1'
PORT = 9999

print('** Seerver Start')
# 소켓 레벨과 데이터 형태(IP4 인터넷을 사용, 데이터를 바이너리 byte stream 사용)
# SOCK_STREAM 연결지향성 SOCK_DGRAM 비연결 지향성(UDP), SOCK_RAW은 SOCKET의 HEADER 정보까지 취득
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 소켓 레블은 SOL_SOCKET, IPPROTO_TCP, IPPROTO_UDP
# SOL_SOCKET 레벨 옵션을 프로토콜에서 설정 레퍼런스 참조
# 별일 없으면 AF_INET/SOCK_STREAM [ SOL_SOCKET/SO_REUSEADDR or IPPROTO_TCP/TCP_NODELAY] 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

try:
    while True:
        print ('wait')
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수", len(client_sockets))
except Exception as e:
    print(e.args[0])
finally:
    server_socket.close()
        