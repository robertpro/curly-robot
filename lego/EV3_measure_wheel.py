#!/usr/bin/env python3

import curses
import ev3

myEV3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')

# Program to calculate radious of the wheel 
ops = b''.join([
        ev3.opOutput_Step_Sync,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A + ev3.PORT_D), # NOS
        ev3.LCX(20),                      # SPEED
        ev3.LCX(0),                       # TURN
        ev3.LCX(3600),                    # STEP
        ev3.LCX(1),                       # BR
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A + ev3.PORT_D)  # NOS
    ])

myEV3.send_direct_cmd(ops)

# It moved 99 - 99.5 cm 
# radius_wheel = distance / (20 * pi) = 0.015835

