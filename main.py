#!/usr/bin/env python

import argparse
from lego.EV3_Send import send_to_lego
from measurement_test.black_board import find_obj, find_board, take_pic, get_img
from measurement_test import black_board

HOST = '192.168.43.191'  # The remote host
PORT = 50009  # The same port as used by the server


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="path to the image file")
    ap.add_argument("-H", "--host", help="host to connect", default=HOST)
    ap.add_argument("-p", "--port", help="port to connect", default=PORT)

    args = vars(ap.parse_args())
    host = args.get('host')
    port = args.get('port')
    image_name = args.get('image')
    if image_name:
        image = get_img(image_name)
    else:
        image = take_pic()

    heigth_coefficient, width_coefficient = find_board(image=image)
    for color in black_board.COLORS.keys():
        print(f"Finding color: {color}")
        x, y = find_obj(image, color, heigth_coefficient, width_coefficient)
        print(f"Color found: {color} | X:{x}, Y:{y}")

        print(f"Sending lego to {x}, {y} for color {color}")
        try:
            response = send_to_lego(host=host, port=port, color=color, x=x, y=y)
            print(f"Lego response: {response}")
        except ConnectionRefusedError:
            print(f"Can not connect to {host}:{port}")
        print("*" * 100)


if __name__ == "__main__":
    main()
