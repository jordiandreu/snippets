#!/usr/bin/env python

import selectors
import socket
import types

HOST = "127.0.0.1"
PORT = 65432

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from, addr')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

class Server(object):
    def __init__(self):

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((HOST, PORT))
        lsock.listen()
        print('listening on', (HOST, PORT))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        # Event loop
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)


if __name__ == "__main__":

   import sys
   if sys.argv[1] == "server":
       s = Server()
   elif sys.argv[1] == "client":
       s = EchoClient()

