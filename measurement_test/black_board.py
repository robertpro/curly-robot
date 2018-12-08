#!/usr/bin/env python

# Black Board measures 222.4 cm X 80.35 cm

# import the necessary packages
from imutils import perspective
import numpy as np
import cv2
import imutils


RED = 'red'
BLUE = 'blue'
GREEN = 'green'


COLORS = {
    RED: ([56, 91, 235], [116, 151, 255]),
    BLUE: ([198, 116, 39], [255, 176, 99]),
    GREEN: ([116, 192, 19], [186, 252, 79])
}


def find_color(image_name, color, cm_pixel_heigth_coefficient, cm_pixel_width_coefficient):
    # Resize the image
    image = cv2.imread(image_name)
    image = cv2.resize(image, (800, 600))
    image_height, image_width, _ = image.shape
    # find the shapes with the color in the image
    lower, upper = COLORS[color]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    shapeMask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=shapeMask)

    # find the contours in the mask
    (_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)

    # compute the rotated bounding box of the contour, then
    # draw the contours
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

    # show box coordinates
    colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
    rect = perspective.order_points(box)
    M = cv2.moments(rect)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cY = image_height - int(M["m01"] / M["m00"])

    # print("Red object location in pixels")
    # print(cX, cY)
    # print("Black board origin coordinates in cms")
    # print(cX * cm_pixel_heigth_coefficient, cY * cm_pixel_heigth_coefficient)
    x = cX * cm_pixel_width_coefficient
    y = cY * cm_pixel_heigth_coefficient
    return x, y


def find_board(image_name):
    # load the image
    image = cv2.imread(image_name)
    image = cv2.resize(image, (800, 600))
    image_height, image_width, _ = image.shape

    # find all the 'black' shapes in the image
    # lower = np.array([0, 0, 0])
    lower = np.array([45, 45, 45])
    upper = np.array([65, 65, 65])
    # upper = np.array([130, 130, 130])
    shapeMask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=shapeMask)

    # find the contours in the mask
    (_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)

    # compute the rotated bounding box of the contour, then
    # draw the contours
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

    # show box coordinates
    colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
    rect = perspective.order_points(box)

    xL, yL = rect.astype("int")[0]
    xU, _ = rect.astype("int")[1]
    _, yU = rect.astype("int")[2]
    xB, yB = rect.astype("int")[3]
    board_width_in_pixels = xU - xL
    board_width_in_cm = 222.4
    board_heigth_in_pixels = yU - yL
    board_heigth_in_cm = 80.35
    cm_pixel_width_coefficient = board_width_in_cm / board_width_in_pixels
    cm_pixel_heigth_coefficient = board_heigth_in_cm / board_heigth_in_pixels
    # print("Black board origin coordinates in pixels")
    xO, yO = xB, image_height - yB
    # print(xO, yO)
    # print("Black board origin coordinates in cms")
    # print(xO * cm_pixel_heigth_coefficient, yO * cm_pixel_heigth_coefficient)

    return cm_pixel_heigth_coefficient, cm_pixel_width_coefficient
