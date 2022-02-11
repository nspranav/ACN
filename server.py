#!/usr/bin/env python3
import argparse
import socket
from utils import recvall

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Server listening at', sock.getsockname())

    while True:
        sc, sockname = sock.accept()

        print('Connection accepted from ', sockname)
        print(' Socket name:',sc.getsockname())
        print(' Socket peer:',sc.getpeername())
        message = recvall(sc,16)
        print(' Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print(' Reply sent, socket closed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive over TCP')
    parser.add_argument('host', help ='interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=8555, help='TCP port (default 8555)')
    args = parser.parse_args()

    server(args.host,args.p)

