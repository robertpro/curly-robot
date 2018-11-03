#!/usr/bin/env python26

# Message format
# "Action,param1,param2"

# 1:Claw      1:Open/2:Close
# 2:Drive To  0-120:x coordinate   0-80:y coordinate

import socket

HOST = '192.168.43.191'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('2,0.2,0.2')
data = s.recv(64)
s.close()
print('Received', repr(data))
