#!/usr/bin/env python3

import curses
import ev3, ev3_vehicle

def react(c):
    global speed, turn, vehicle
    if c in [ord('q'), 27, ord('p')]:
        vehicle.stop()
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
    vehicle.move(speed, turn)
    stdscr.addstr(5, 0, 'speed: {}, turn: {}      '.format(speed, turn))
    stdscr.addstr(6, 0, 'x: {}, y: {}, o: {}      '.format(vehicle.pos_x, vehicle.pos_y, vehicle.orientation))

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
                   curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            react(c)

speed = 0
turn  = 0   
vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.015835, tread=0.1689, protocol=ev3.WIFI, host='00:16:53:5E:89:BD')
stdscr = None

curses.wrapper(main)