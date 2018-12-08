#!/usr/bin/env python26

# Message format
# "Action,param1,param2"

# 1:Claw      1:Open/2:Close
# 2:Drive To  0-120:x coordinate   0-80:y coordinate

import socket


def send_to_lego(host, port, color, x, y):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(f'{color},{x:.2f},{y:.2f}')
    data = s.recv(64)
    s.close()
    return repr(data)
