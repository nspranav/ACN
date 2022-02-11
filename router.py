import argparse
import socket
from utils import recvall, Segment


def router(interface,port,serv_port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Router Listening at', sock.getsockname())

    while True:
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())

        # Message is from the client
        message = recvall(sc, 16)
        print(' Incoming sixteen-octet message:', repr(message))
        
        # Forward packet to server
        sc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc_server.connect((interface,serv_port))
        print('Router client has been assigned socket name', sc_server.getsockname())
        sc_server.sendall(message)

        #wait for server reply
        reply = recvall(sc_server,16)
        print('The server said', repr(reply))
        sc_server.close()

        #



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('router', help = 'The ip address of the router')
    parser.add_argument('-r', metavar='router port', type= int, default= 8343, help= 'The port number for the router.')
    parser.add_argument('-s', metavar='server port', type=int, help= 'The port of the server program ')

    args = parser.parse_args()

    router(args.router, args.r, args.s)


    
