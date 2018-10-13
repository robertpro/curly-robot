#!/usr/bin/env python3

import curses
import ev3

myEV3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')

myEV3.send_direct_cmd(ops)