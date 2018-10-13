#!/usr/bin/env python3

import ev3

my_ev3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')

ops = b''.join([
    ev3.opUI_Write,
    ev3.LED,
    ev3.LED_RED,
    ev3.opSound,
    ev3.TONE,
    ev3.LCX(1),
    ev3.LCX(262),
    ev3.LCX(500),
    ev3.opSound_Ready,
    ev3.opUI_Write,
    ev3.LED,
    ev3.LED_GREEN,
    ev3.opSound,
    ev3.TONE,
    ev3.LCX(1),
    ev3.LCX(330),
    ev3.LCX(500),
    ev3.opSound_Ready,
    ev3.opUI_Write,
    ev3.LED,
    ev3.LED_RED,
    ev3.opSound,
    ev3.TONE,
    ev3.LCX(1),
    ev3.LCX(392),
    ev3.LCX(500),
    ev3.opSound_Ready,
    ev3.opUI_Write,
    ev3.LED,
    ev3.LED_RED_FLASH,
    ev3.opSound,
    ev3.TONE,
    ev3.LCX(2),
    ev3.LCX(523),
    ev3.LCX(2000),
    ev3.opSound_Ready,
    ev3.opUI_Write,
    ev3.LED,
    ev3.LED_GREEN
])
my_ev3.send_direct_cmd(ops)