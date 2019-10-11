import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse the local socket in TIME_WAI state, without waiting expiration.
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
serversocket.bind(('localhost', 8100))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    print "Accepting..."
    connection, address = serversocket.accept()
    print "Accepted."
    while True:
        buf = connection.recv(64)
        if len(buf) > 0:
            print "buffer content is ", buf
        #break
