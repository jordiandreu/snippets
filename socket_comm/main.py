#!/usr/bin/env python

'''https://realpython.com/python-sockets/'''

import socket


HOST = '127.0.0.1'
PORT = 65432


class Server(object):
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print('Waiting for connections...')
            conn, addr = s.accept()
            # conn is a new socket object for communication!!
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if data == b'Who are you?':
                        # echo back to client
                        conn.sendall(b'I am your servant')



class EchoClient(object):
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'Who are you?')
            data = s.recv(1024)
        print('Received', repr(data))


if __name__ == "__main__":

   import sys
   if sys.argv[1] == "server":
       s = Server()
   elif sys.argv[1] == "client":
       s = EchoClient()


