from collections import namedtuple
    

Segment = namedtuple('Segment',['SEQ','data','FIN'])
NACK = namedtuple('NACK',['seq'])


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))

        if not more:
            raise EOFError('was expecting %d bytes but only recieved'
                        ' %d bytes before the socket closed'
                        % (length, len(data)))

        data += more

    return data


def prepare_data(num:int):
    '''
    Function to generate segments

    Parameters:
        num (int): The number of segments to generate 

    Returns:
        list: A list of 'num' number of segments   
    '''

    segments = [Segment(i,i*100,0) for i in range(1,10)]
    segments[-1].FIN = 1

    return segments