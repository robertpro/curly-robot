#!/usr/bin/env python3

import curses
import ev3

myEV3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')

# Program to calculate the tread
ops = b''.join([
        ev3.opOutput_Step_Sync,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A + ev3.PORT_D), # NOS
        ev3.LCX(20),                      # SPEED
        ev3.LCX(200),                       # TURN
        ev3.LCX(18000),                    # STEP
        ev3.LCX(1),                       # BR
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A + ev3.PORT_D)  # NOS
    ])

myEV3.send_direct_cmd(ops)

# 9.375 turns
# tread = radius_wheel * 100 / N
# tread = 0.015835 * 100 / 9.375 = 0.1689

