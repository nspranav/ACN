#!/usr/bin/env python3
import argparse
import socket
from utils import *
import pickle
from matplotlib import pyplot as plt
import time

def client(host, port,length):
    num_trials = 0
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host,port))
    print('Client has the socket:',sock.getsockname())

    segments = prepare_data(length)
    dump = pickle.dumps(segments)
    print(len(dump))

    sock.sendall(dump)
    num_trials += 1
    
    while True:

        reply = recvall(sock)
        if reply:
            
            print('Replying to NACK')
            nacks = pickle.loads(reply)
            if isinstance(nacks,FIN):
                print('Data sent successfully')
                sock.close()
                break
            print('Got nack for',nacks)
            sock.sendall(pickle.dumps([segments[nack.SEQ - 1] for nack in nacks]))
            num_trials += 1
    
    return num_trials


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client socket program')
    parser.add_argument('host', help='interface the server is listeng at')
    parser.add_argument('-p', metavar='PORT', type= int, default= 8555, help= 'TCP port (default 8555)')
    args = parser.parse_args()
    
    num_packets = [150, 250, 450, 650, 850, 1000]

    num_trials = []
    total_times = []
    total_time = 0 

    for l in num_packets:
        start = time.time()
        num_trials.append(client(args.host,args.p,l))
        end = time.time()
        total_time = end - start
        total_times.append(total_time)

    #num_trials = [client(args.host,args.p,len) for len in num_packets]

    plt.plot(num_packets,num_trials,'-')
    plt.xticks(num_packets)
    plt.yticks(num_trials)
    plt.xlabel('Number of packets')
    plt.ylabel('Number of trials')
    plt.savefig('plot.png')

    print(total_times)