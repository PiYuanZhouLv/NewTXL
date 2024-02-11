import socket
import json
try:
    from LengthVariableTCP import LengthVariableTCP as LVTCP
except ModuleNotFoundError:
    from .LengthVariableTCP import LengthVariableTCP as LVTCP

class Client:
    def __init__(self,address):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect(address)
        self.lvtcp = LVTCP(self.sock)
        self.closed = False
    def new(self):
        self.lvtcp.send(json.dumps(['NEW']).encode())
        return int(self.lvtcp.recv(1024))
    def get(self,page):
        self.lvtcp.send(json.dumps(["get",page]).encode())
        return json.loads(self.lvtcp.recv(1024).decode())
    def set(cls,name):
        class Inner:
            def __init__(self, cmd=[]) -> None:
                self.cmd = cmd
            def __getitem__(self, item):
                return type(self)(self.cmd+[item])
            def __setitem__(self, item, value):
                cls.lvtcp.send(json.dumps(["set", name, self.cmd+[item], json.dumps(value)]).encode())
                cls.lvtcp.recv(1024)
        return Inner()

    def search(self,page):
        self.lvtcp.send(json.dumps(["search",page]).encode())   
        return json.loads(self.lvtcp.recv(1024).decode())

    def close(self):
        if not self.closed:
            self.lvtcp.send(b'["close"]')
            self.sock.close()
            self.closed = True

    def __del__(self):
        self.close()

    def check_invite_code(self, iv_code):
        self.lvtcp.send(json.dumps(["check", iv_code]).encode())
        return self.lvtcp.recv().decode() == 'Valid'
