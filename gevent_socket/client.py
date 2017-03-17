#!/usr/bin/env python
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 16000))
clientsocket.send(b'hello')

