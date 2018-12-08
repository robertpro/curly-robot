import cv2
import argparse

from measurement_test.black_board import find_color, find_board
from measurement_test import black_board


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i",
        "--image",
        help="path to the image file",
        required=True
    )
    args = vars(ap.parse_args())
    image_name = args.get('image')

    cm_pixel_heigth_coefficient = find_board(image_name=image_name)

    for color in black_board.COLORS.keys():
        x, y = find_color(image_name, color, cm_pixel_heigth_coefficient)
        print(f"Color: {color} | X:{x}, Y:{y}")


if __name__ == "__main__":
    main()
