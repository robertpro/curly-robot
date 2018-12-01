#!/usr/bin/env python3

# Echo server program
import socket

dictionary = {
    "1": "Hello World",
    "2": "Sistemas Distribuidos",
    "3": "Practica de RMI"
}

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)
while 1:
    data = conn.recv(64)
    if not data: 
        break
    if data in dictionary:
        print (dictionary[data])
    else:
        print ("Error")
conn.close() 

