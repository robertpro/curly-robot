#!/usr/bin/env python3

import ev3, ev3_vehicle

my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_vehicle.verbosity = 1
my_vehicle._pos_x = pos_x_init = 0.075
my_vehicle._pos_y = pos_y_init = 0.11
speed = 70
speed_claw = 20
my_vehicle.sync_mode = ev3.SYNC

object_1 = [0.50,0.50]
object_2 = [1.0,0.40]
object_3 = [1.2,0.70]

store_1 = [0.0,0.40]
store_2 = [0.0,0.60]
store_3 = [0.0,0.80]

# Pick up 1
my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_to(speed, object_1[0],object_1[1])
my_vehicle.claw(speed_claw, open=False)
my_vehicle.drive_to(speed, store_1[0],store_1[1])
my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_straight(-speed,0.10)

# Pick up 2
#my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_to(speed, object_2[0],object_2[1])
my_vehicle.claw(speed_claw, open=False)
my_vehicle.drive_to(speed, store_2[0],store_2[1])
my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_straight(-speed,0.10)

# Pick up 1
#my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_to(speed, object_3[0],object_3[1])
my_vehicle.claw(speed_claw, open=False)
my_vehicle.drive_to(speed, store_3[0],store_3[1])
my_vehicle.claw(speed_claw, open=True)
my_vehicle.drive_straight(-speed,0.10)

# Go to initial point
my_vehicle.drive_to(speed,pos_x_init,pos_y_init)
my_vehicle.rotate_to(speed,0)
my_vehicle.claw(speed_claw, open=False)