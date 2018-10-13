#!/usr/bin/env python3

import ev3, time

my_ev3 = ev3.EV3(
    protocol=ev3.WIFI,
    host='00:16:53:5E:89:BD'
)
my_ev3.verbosity = 1

ops = b''.join([
    ev3.opUI_Draw,
    ev3.TOPLINE,
    ev3.LCX(0),                                      # ENABLE
    ev3.opUI_Draw,
    ev3.BMPFILE,
    ev3.LCX(1),                                      # COLOR
    ev3.LCX(0),                                      # X0
    ev3.LCX(0),                                      # Y0
    ev3.LCS("../apps/Motor Control/MotorCtlAD.rgf"), # NAME
    ev3.opUI_Draw,
    ev3.UPDATE
])
my_ev3.send_direct_cmd(ops)
time.sleep(5)
ops = b''.join([
    ev3.opUI_Draw,
    ev3.TOPLINE,
    ev3.LCX(1),     # ENABLE
    ev3.opUI_Draw,
    ev3.FILLWINDOW,
    ev3.LCX(0),     # COLOR
    ev3.LCX(0),     # Y0
    ev3.LCX(0),     # Y1
    ev3.opUI_Draw,
    ev3.UPDATE
])
my_ev3.send_direct_cmd(ops)