#!/usr/bin/env python3
import argparse
from operator import eq
import socket
from utils import *
from time import sleep
import pickle

def order_messages(final_segments:list,segments:list):
    '''
    '''
    seq = []
    for segment in segments:
        final_segments[segment.SEQ - 1] = segment
        seq.append(segment.SEQ)
   
    missing_segments = list(set(range(1,len(final_segments)+1)) - set(seq))
    return missing_segments

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Server listening at', sock.getsockname())

    while True:
        sc, sockname = sock.accept()
        sc.settimeout(2)

        print('Connection accepted from ', sockname)
        print(' Socket name:',sc.getsockname())
        print(' Socket peer:',sc.getpeername())
        final_segments = []
        missing_segments = None

        while True:
            message = recvall(sc)
            if message:
                segments = pickle.loads(message)
                print(f'Server received {len(segments)} segemtns')
                
                # setting the final window size of total data
                if len(final_segments) != segments[0].len:
                    final_segments = [None] *  segments[0].len

                print('length of final seg=',len(final_segments))

                #need initail missing segments, later only one missing segment will arrive
                if not missing_segments:
                    print('In here')
                    missing_segments = order_messages(final_segments, segments)
                else:
                    received_seq = []
                    # Nack has been sent and the reply arrived
                    print('segments recieved is',segments)
                    for segment in segments:
                        final_segments[segment.SEQ - 1] = segment
                        received_seq.append(segment.SEQ)
                    missing_segments = list(set(missing_segments) - set(received_seq))

                print('packets missing', missing_segments)
            
            if len(missing_segments) == 0:
                fin = FIN()
                sc.sendall(pickle.dumps(fin))
                sc.close()
                print('All packets received, socket closed')
                break
            elif missing_segments:
                
                nacks = [NACK(seq=i) for i in missing_segments]
                print('sending NACK for missing segments',nacks)
                dump = pickle.dumps(nacks)
                print('len of nacks',len(dump))
                sc.sendall(dump)
            else:
                nack = NACK(seq=0)
                sc.sendall(pickle.dumps(nack))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive over TCP')
    parser.add_argument('host', help ='interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=8555, help='TCP port (default 8555)')
    args = parser.parse_args()

    server(args.host,args.p)

