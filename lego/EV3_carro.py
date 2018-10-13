#!/usr/bin/env python3

import curses
import ev3

def move(speed: int, turn: int, claw: str) -> None:
    global myEV3, stdscr
    stdscr.addstr(5, 0, 'speed: {}, turn: {}, claw: {}      '.format(speed, turn, claw))
    if turn > 0:
        speed_right = speed
        speed_left  = round(speed * (1 - turn / 100))
    else:
        speed_right = round(speed * (1 + turn / 100))
        speed_left  = speed
    if claw == 'open':
        speed_claw = 50
    elif claw == 'stop':
        speed_claw = 0
    else:
        speed_claw = -50
    ops = b''.join([
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_C),              # NOS
        ev3.LCX(speed_right),             # SPEED
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_B),              # NOS
        ev3.LCX(speed_left),              # SPEED
        ev3.opOutput_Speed,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_A),              # NOS
        ev3.LCX(speed_claw),              # SPEED
        ev3.opOutput_Start,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_C + ev3.PORT_B + ev3.PORT_A)  # NOS
    ])
    myEV3.send_direct_cmd(ops)

def stop() -> None:
    global myEV3, stdscr
    stdscr.addstr(5, 0, 'vehicle stopped                         ')
    ops = b''.join([
        ev3.opOutput_Stop,
        ev3.LCX(0),                       # LAYER
        ev3.LCX(ev3.PORT_C + ev3.PORT_B), # NOS
        ev3.LCX(0)                        # BRAKE
    ])
    myEV3.send_direct_cmd(ops)

def react(c):
    global speed, turn, claw
    if c in [ord('q'), 27, ord('p')]:
        stop()
        return
    elif c == curses.KEY_LEFT:
        turn += 5
        turn = min(turn, 200)
    elif c == curses.KEY_RIGHT:
        turn -= 5
        turn = max(turn, -200)
    elif c == curses.KEY_UP:
        speed += 5
        speed = min(speed, 100)
    elif c == curses.KEY_DOWN:
        speed -= 5
        speed = max(speed, -100)
    elif c == curses.KEY_F1:
        if claw == 'open':
            claw = 'stop'
        else:
            claw = 'open'
    elif c == curses.KEY_F2:
        if claw == 'close':
            claw = 'stop'
        else:
            claw = 'close'
    move(speed, turn, claw)

def main(window) -> None:
    global stdscr
    stdscr = window
    stdscr.clear()      # print introduction
    stdscr.refresh()
    stdscr.addstr(0, 0, 'Use Arrows to navigate your EV3-vehicle')
    stdscr.addstr(1, 0, 'Pause your vehicle with key <p>')
    stdscr.addstr(2, 0, 'Terminate with key <q>')

    while True:
        c = stdscr.getch()
        if c in [ord('q'), 27]:
            react(c)
            break
        elif c in [ord('p'),
                   curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN, curses.KEY_ENTER, curses.KEY_BACKSPACE]:
            react(c)

speed = 0
turn  = 0   
claw  = 'stop'
myEV3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
stdscr = None

# ops = opOutput_Polarity + b'\x00' + LCX(PORT_A + PORT_D) + LCX(-1)
# myEV3.send_direct_cmd(ops)

curses.wrapper(main)