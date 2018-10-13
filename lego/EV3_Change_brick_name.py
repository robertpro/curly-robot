#!/usr/bin/env python3

import ev3

my_ev3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
my_ev3.verbosity = 1

ops = b''.join([
    ev3.opCom_Set,
    ev3.SET_BRICKNAME,
    ev3.LCS("EV3_SD")
])
my_ev3.send_direct_cmd(ops)