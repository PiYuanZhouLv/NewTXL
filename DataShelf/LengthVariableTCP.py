import math

class LengthVariableTCP:
    def __init__(self, sock) -> None:
        self.sock = sock
    def send(self, data):
        length = len(data)
        # print('send data length:', length)
        if not length:
            return
        white_length = math.ceil(length.bit_length()/8) - 1
        ba = bytearray()
        ba.extend([0]*white_length)
        ba.extend(reversed([length%(256**(i+1))//(256**i) for i in range(white_length+1)]))
        ba.extend(data)
        self.sock.sendall(ba)
    def recv(self, _):
        head_left = 0
        while True:
            b = self.sock.recv(1)[0]
            if b:
                break
            else:
                head_left += 1
        data_length = b
        for i in range(head_left):
            data_length <<= 8
            data_length += self.sock.recv(1)[0]
        # print('receive data length:', data_length)
        data = bytearray()
        while len(data) < data_length:
            data.extend(self.sock.recv(min(1024, data_length-len(data))))
        return bytes(data)
