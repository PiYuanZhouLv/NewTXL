import socket
import random
import json
import time

class DataShelf:
    def __init__(self, file, addr, port=None) -> None:
        self.fp = open(file, 'r+', encoding='utf-8')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if port == None:
            while True:
                try:
                    self.sock.bind((addr, random.randint(1024, 65536)))
                except:
                    continue
                else:
                    break
        else:
            self.sock.bind((addr, port))
        self.save_count = 1000
        self.load()
        self.sock.setblocking(False)
    def load(self):
        self.fp.seek(0, 2)
        if self.fp.tell() == 0:
            self.shelf = {
                'info':{
                    'newid': 0,
                    'savetime': time.strftime('%Y-%m-%d %H:%M:%S')
                },
                'shelf':{}
            }
        else:
            self.fp.seek(0, 0)
            self.shelf = json.load(self.fp)
    def save(self):
        self.save_count -= 1
        if self.save_count <= 0:
            self.save_at_once()
    def save_at_once(self):
        self.fp.seek(0, 0)
        self.shelf['info']['savetime'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(self.shelf, self.fp)
        self.fp.truncate()
        self.fp.flush()
        self.save_count = 1000
    def new(self):
        nid = self.shelf['info']['newid']
        self.shelf['info']['newid'] += 1
        self.shelf['shelf'][str(nid)] = {}
        self.save()
    def delete(self, tid):
        self.shelf['shelf'].pop(str(tid))
        self.save()
    def set(self, command):
        i = self.shelf['shelf'][str(command[0])]
        for n in command[1][:-1]:
            i = i[n]
        i[command[1][-1]] = command[2]
        self.save()
    def deal(self, loop=False):
        ...

def start():
    ...

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--ip', default='127.0.0.1')
    parser.add_argument('--port', default='12345')
    args = parser.parse_args()
    start(args.path, (args.ip, args.port))