import socket
import json

class client:
    def __init__(self,address):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect(address)
    def new(self):
        self.sock.send(json.dumps(['NEW']).encode())
        return int(self.sock.recv(1024))
    def get(self,page):
        self.sock.send(json.dumps(["get",page]).encode())
        return json.loads(self.sock.recv(1024).decode())
    def set(cls,name):
        class Inner:
            def __init__(self, cmd=[]) -> None:
                self.cmd = cmd
            def __getitem__(self, item):
                return type(self)(self.cmd+[item])
            def __setitem__(self, item, value):
                cls.sock.send(json.dumps(["set", name, self.cmd+[item], json.dumps(value)]).encode())
                cls.sock.recv(1024)
        return Inner()

    def search(self,page):
        self.sock.send(json.dumps(["search",page]).encode())   
        return json.loads(self.sock.recv(1024).decode())

    def close(self):
        self.sock.send(b'["close"]')
        self.sock.close()

