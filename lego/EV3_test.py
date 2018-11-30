#!/usr/bin/env python3

import ev3, ev3_vehicle
import time

my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_vehicle.verbosity = 1
#my_vehicle._pos_x = pos_x_init = 0.075
#my_vehicle._pos_y = pos_y_init = 0.11
speed = 50
speed_claw = 20

my_vehicle.poll_area(speed, 90)
