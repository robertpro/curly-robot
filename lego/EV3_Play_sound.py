#!/usr/bin/env python3

import ev3
import time

my_ev3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_ev3.verbosity = 1

ops = b''.join([
    ev3.opSound,
    ev3.REPEAT,
    ev3.LCX(100),                  # VOLUME
    ev3.LCS('./ui/DownloadSucces') # NAME
])
my_ev3.send_direct_cmd(ops)
time.sleep(2)
ops = b''.join([
    ev3.opSound,
    ev3.BREAK
])
my_ev3.send_direct_cmd(ops)