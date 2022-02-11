import argparse
import socket
from utils import *

def client(host, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    print('Client has the socket:',sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock,16)
    print('The server said', repr(reply))
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client socket program')
    parser.add_argument('host', help='interface the server is listeng at')
    parser.add_argument('-p', metavar='PORT', type= int, default= 8555, help= 'TCP port (default 8555)')
    args = parser.parse_args()

    client(args.host,args.p)