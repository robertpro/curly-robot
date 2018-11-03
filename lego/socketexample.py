#!/usr/bin/env python3

# Echo server program
import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)
while 1:
    data = conn.recv(64)
    if not data: break
    conn.send(data)
conn.close() 

# # Echo client program
# import socket

# HOST = '192.168.43.148'    # The remote host
# PORT = 50007              # The same port as used by the server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# s.send('Hello, world')
# data = s.recv(1024)
# s.close()
# print 'Received', repr(data)