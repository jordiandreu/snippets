import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
#clientsocket.connect(('84.89.227.57', 5000))
clientsocket.send('hello')
#clientsocket.send('hello')
#clientsocket.send('hello')
#clientsocket.send('hello')
