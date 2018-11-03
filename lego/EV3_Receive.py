#!/usr/bin/env python26

# Message format
# "Action,param1,param2"

# 1:Claw      1:Open/2:Close
# 2:Drive To  0-120:x coordinate   0-80:y coordinate

import socket
import ev3, ev3_vehicle
import numbers

my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_vehicle.verbosity = 1
my_vehicle._pos_x = pos_x_init = 0.075
my_vehicle._pos_y = pos_y_init = 0.11
speed = 30
speed_claw = 20
my_vehicle.sync_mode = ev3.SYNC

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Listening on port: %s' % PORT)
while 1:
    conn, addr = s.accept()
    print('Connected')
    while 1:
        data = conn.recv(64)
        datastr = data.decode("utf-8") 
        if not data: break
        dataparams = datastr.split(',')
        if dataparams[0] == '1':
            if dataparams[1] == '1':
                my_vehicle.claw(speed_claw, open=True)
                conn.send(data)
            elif dataparams[1] == '2':
                my_vehicle.claw(speed_claw, open=False)
                conn.send(data)
            else:
                conn.send('Message error')
        elif dataparams[0] == '2':
            try:
                my_vehicle.drive_to(speed, float(dataparams[1]),float(dataparams[2]))
                conn.send(data)
            except: 
                print('Message error')
        else:
            print('Message error')
    conn.close() 