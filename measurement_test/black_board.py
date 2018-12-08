#!/usr/bin/env python

# Black Board measures 222.4 cm X 80.35 cm

# import the necessary packages
from imutils import perspective
import requests
import numpy as np
import cv2
import imutils
import sys


url = "http://10.42.0.190:8080/shot.jpg"


RED = 5
BLUE = 2
GREEN = 3


COLORS = {
    RED: ([90, 90, 235], [150, 150, 255]),
    #BLUE: ([198, 116, 39], [255, 176, 99]),
    #GREEN: ([116, 192, 19], [186, 252, 79])
}


def find_obj(image, color, board_coefficient):
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

    cv2.imshow("Board", image)
    cv2.waitKey(0)

    #print("Red object location in pixels")
    #print(cX, cY)
    #print("Black board origin coordinates in cms")
    #print(cX * cm_pixel_heigth_coefficient, cY * cm_pixel_heigth_coefficient)
    x = cX * board_coefficient
    y = cY * board_coefficient
    return x, y


def find_board(image):
    image_height, image_width, _ = image.shape

    # find all the 'black' shapes in the image
    # lower = np.array([0, 0, 0])
    lower = np.array([20, 20, 20])
    upper = np.array([60, 60, 60])
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
    board_width_in_cm = 122.4
    board_heigth_in_pixels = yU - yL
    board_heigth_in_cm = 80.35
    board_coefficient = board_width_in_cm / board_width_in_pixels
    #board_coefficient = board_heigth_in_cm / board_heigth_in_pixels
    cv2.imshow("Board", image)
    cv2.waitKey(0)
    #print("Black board origin coordinates in pixels")
    xO, yO = xB, image_height - yB
    #print(xO, yO)
    #print("Black board origin coordinates in cms")
    #print(xO * heigth_coefficient, yO * heigth_coefficient)

    return board_coefficient


def take_pic():
    try:
        img_resp = requests.get(url)
        img_array = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        img = cv2.resize(img, (800, 600))

        #cv2.imshow("Android Cam", img)
        #cv2.waitKey(0)

    except:
        print("Unable to get image from " + url)
        sys.exit(-1)

    return img


def get_img(img_name):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (800, 600))
    return img

