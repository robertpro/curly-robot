#!/usr/bin/env python3

# 2 Azul
# 3 Verde
# 4 Amarillo
# 5 Rojo

import ev3, ev3_vehicle

my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_vehicle.verbosity = 1
my_vehicle._pos_x = pos_x_init = 0.14
my_vehicle._pos_y = pos_y_init = 0.11
my_vehicle._sync_mode = ev3.SYNC

speed = 40
speed_claw = 20

pieces = [
    [0.40,0.30],
    [0.70,0.50],
    [1.10,0.20]
]

stores = {
    2: [0.1,0.15],
    3: [0.1,0.30],
    4: [0.1,0.45],
    5: [0.1,0.60]
}

# Pick up ALL
for piece in pieces:
    my_vehicle.define_front(claw=False)
    my_vehicle.drive_to(speed, piece[0],piece[1],stop_at=0.23)
    optimal_o = my_vehicle.poll_area(speed, 90)
    my_vehicle.rotate_to(int(speed/2),optimal_o[0])
    my_vehicle.drive_straight(speed,0.15)
    color = my_vehicle.read_color()
    my_vehicle.grab_object(speed, speed_claw)
    my_vehicle.define_front(claw=True)
    my_vehicle.drive_to(speed, stores[color][0],stores[color][1])
    my_vehicle.leave_object(speed, speed_claw)

# Go to initial point
my_vehicle.drive_to(speed,pos_x_init,pos_y_init)
my_vehicle.rotate_to(speed,0)
my_vehicle.claw(speed_claw, open=False)