#!/usr/bin/env python3

# Echo client program
import socket

HOST = '192.168.43.148'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('1')
s.close()
