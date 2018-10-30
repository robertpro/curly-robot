#!/usr/bin/env python3

import ev3, ev3_vehicle

my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_vehicle.verbosity = 1
speed = 30
speed_claw = 20
my_vehicle.sync_mode = ev3.SYNC
# my_vehicle.drive_straight(speed, 0.15)
# my_vehicle.rotate_to(speed, 45.0)
# my_vehicle.drive_straight(speed, 0.30)
# my_vehicle.rotate_to(speed,0.0)
# my_vehicle.drive_straight(speed, 0.30)
# my_vehicle.drive_to(speed, 0.0, 0.0)
# my_vehicle.rotate_to(speed, 0.0)

my_vehicle.claw(speed_claw, open=True)
my_vehicle.claw(speed_claw, open=False)
my_vehicle.claw(speed_claw, open=True)
my_vehicle.claw(speed_claw, open=False)
my_vehicle.claw(speed_claw, open=True)
my_vehicle.claw(speed_claw, open=False)