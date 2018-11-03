#!/usr/bin/env python26

# Echo client program
import socket

HOST = '192.168.43.191'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('2,0.2,0.2')
data = s.recv(1024)
s.close()
print 'Received', repr(data)