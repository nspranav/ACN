#!/usr/bin/env python3
import argparse
import pickle
import socket
from time import sleep
from random import random
from utils import *

def router(interface,port,serv_port):
    '''

    '''
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Router Listening at', sock.getsockname())
    sc_server = None
    while True:
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        sc.settimeout(2)
        # Message is from the client
        socket_open = True
        while socket_open:
            message = recvall(sc)
            print('length of message',len(message))
            if message:
                segments = pickle.loads(message)
                print(' Number of segments received =', len(segments))
                
                # store packets after random dropping
                new_segemts = [segment for segment in segments if random()>0.4] 

                print('Number of packets left =',len(new_segemts),'of',len(segments))

                # only create new connection to server if doesn't exist
                if not sc_server:
                    # Forward packet to server
                    sc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sc_server.settimeout(2)
                    sc_server.connect((interface,serv_port))
                    print('Router client has been assigned socket name', sc_server.getsockname())
                if len(new_segemts) > 0:
                    sc_server.sendall(pickle.dumps(new_segemts))


            while True:
                # wait for server reply
                reply = recvall(sc_server)
                if reply:
                    print('len of reply',len(reply))
                    nacks = pickle.loads(reply)
                    if isinstance(nacks,FIN):
                        print('sending FIN to client')
                        sc_server.close()
                        sc.sendall(reply)
                        sleep(3)
                        sc.close()
                        socket_open = False
                        sc_server= None
                        break

                    #print(' Number of segments received =', len(message))
                    
                    # store packets after random dropping
                    new_nacks = [nack for nack in nacks if random()>0.4]
                    print('NACK forwarding to client')
                    if len(new_nacks) > 0:
                        sc.sendall(pickle.dumps(new_nacks))
                    break

        




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('router', help = 'The ip address of the router')
    parser.add_argument('-r', metavar='router port', type= int, default= 8343, help= 'The port number for the router.')
    parser.add_argument('-s', metavar='server port', type=int, help= 'The port of the server program ')

    args = parser.parse_args()

    router(args.router, args.r, args.s)


    
