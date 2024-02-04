import socket
import json
import time
import queue
import threading
from rapidfuzz import process
import os
import traceback

class DataShelf:
    def __init__(self, file, addr, log=False) -> None:
        if not os.path.exists(file):
            with open(file, 'a'):
                pass
        self.fp = open(file, 'r+', encoding='utf-8')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        if log:
            print('DataShelf has bound to', addr)
            print('Press Ctrl-C to input command.')
        self.save_count = 1000
        self.shutdown = False
        self.load()
        self.sock.listen(16)
        self.sock.settimeout(10)
        self.queue = queue.Queue()
        self.threads = []
        self.log = log
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
        return str(nid)
    # def delete(self, tid):
    #     self.shelf['shelf'].pop(str(tid))
    #     self.save()
    def set(self, command):
        i = self.shelf['shelf'][str(command[0])]
        for n in command[1][:-1]:
            if n not in i:
                i[n] = {}
            i = i[n]
        i[command[1][-1]] = command[2]
        self.save()
        return 'OK'
    def get(self, command):
        return json.dumps(self.shelf['shelf'][str(command[0])])
    def search(self, command):
        titles = {k: v['title'] for k, v in self.shelf['shelf'].items()}
        return json.dumps(process.extract(command[0], titles, limit=10))
    def accept(self):
        def deal(sock: socket.socket, server: DataShelf):
            q = queue.Queue()
            sock.setblocking(True)
            sock.settimeout(10)
            while not server.shutdown:
                try:
                    cmd = json.loads(sock.recv(1024).decode())
                except socket.timeout:
                    continue
                except json.JSONDecodeError:
                    try:
                        sock.send(b'CommandSyntexError')
                    except OSError:
                        return
                    else:
                        continue
                if cmd[0] == "close":
                    if server.log:
                        print('A Client has disconnected.')
                    return
                else:
                    server.queue.put((cmd, q))
                    result = q.get()
                    sock.send(result.encode())
        while not self.shutdown:
            try:
                client_socket, client_address = self.sock.accept()
            except socket.timeout:
                continue
            thread = threading.Thread(target=deal, args=(client_socket, self))
            self.threads.append(thread)
            thread.start()
            if self.log:
                print('A Client', client_address, 'has connected to the sever.')
        for thread in self.threads:
            thread.join()
    def process(self):
        while not self.shutdown:
            try:
                cmd, back = self.queue.get(timeout=10)
                if self.log:
                    print('Get command', cmd, 'from', hex(id(back)))
            except queue.Empty:
                continue
            try:
                match cmd[0].lower():
                    case "get":
                        r = self.get(cmd[1:])
                    case "set":
                        r = self.set(cmd[1:])
                    case "search for name":
                        r = self.search(cmd[1:])
                    case "new":
                        r = self.new()
            except Exception as err:
                r = type(err).__name__+': '+str(err)
                traceback.print_exception(err)
            back.put(r)
    def do_shutdown(self):
        self.shutdown = True
        self.save_at_once()

def start(file, addr):
    db = DataShelf(file, addr, True)
    acc = threading.Thread(target=db.accept)
    acc.start()
    pro = threading.Thread(target=db.process)
    pro.start()
    log = True
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            db.log = False
            cmd = input('DataShelf> ')
            match cmd:
                case "save":
                    db.save_at_once()
                    print('The data is saved.')
                case "log on":
                    log = True
                    print('OK, the log is on now.')
                case "log off":
                    log = False
                    print('OK, the log is off now')
                case "shutdown":
                    db.do_shutdown()
                    print('Shuting down, please do NOT close this window.')
                    print('This can take about 10 seconds......')
                    acc.join()
                    pro.join()
                    break
                case _:
                    print('Unknown command.')
            db.log = log

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--ip', default='127.0.0.1')
    parser.add_argument('--port', default='12345')
    args = parser.parse_args()
    # Try to start this server by using `python server.py --file test.db.json`
    start(args.path, (args.ip, int(args.port)))