#%%
import socket

class NACK:
    '''
    A segment representing a negative acknowledgement

    Attributes:
        seq (int): Represents 
    '''
    def __init__(self,seq):
        self.SEQ = seq
    
    def __repr__(self) -> str:
        return f'seq:{self.SEQ}'

class FIN:
    '''
    '''
    def __init__(self):
        self.fin = 1

class Segment:
    '''
    A Segment representing data unit transferred between the transport layers

    Attributes:
        seq (int):
        data (object): 
        len (int):
    '''
    def __init__(self,seq,data,len):
        self.SEQ = seq
        self.data = data
        self.FIN = 0
        self.len = len
    
    def __repr__(self) -> str:
        return f'SEQ : {self.SEQ}, data : {self.data}'

def recvall(sock: socket.socket):
    '''
    Function to recieve data from a socket

    Parameters:
        sock (Socket): The socket from which the data is being received
        length (int): The minimum length of data before recvieve returns

    Returns;
        Bytes: The data received in bytes
    '''
    data = b''
    packet = None
    while True:
        try:
            packet = sock.recv(1024)
        except socket.timeout as e:
            pass
        except ConnectionResetError as e:
            return 

        if not packet:
            break

        data += packet
        packet = None

    return data


def prepare_data(num:int):
    '''
    Function to generate segments

    Parameters:
        num (int): The number of segments to generate 

    Returns:
        list: A list of 'num' number of segments   
    '''

    segments = [Segment(i,i,num) for i in range(1,num+1)]
    segments[-1].FIN = 1

    return segments

# %%
