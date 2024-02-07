import socket
import json

class client:
    def __init__(self,address):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect(address)
    def new():
        self.sock.send(json.dumps(['NEW']).encode())
        
    def get():
        ...
    def set():
        ...
    def serch():
        ...    



