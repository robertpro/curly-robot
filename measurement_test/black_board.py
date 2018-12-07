#!/usr/bin/env python

# Black Board measures 222.4 cm X 80.35 cm

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import contours
from imutils import perspective
import numpy as np
import argparse
import cv2
import imutils
import socket
import sys
import click

def find_color(image, color):
    # Resize the image
    image = cv2.resize(image, (800, 600))
    image_height, image_width, _ = image.shape
    colors = {'red'   : ([56, 91, 235], [116, 151, 255]),
              'blue'  : ([198, 116, 39], [255, 176, 99]),
              'green' : ([116, 192, 19], [186, 252, 79])}
    # find the shapes with the color in the image
    lower, upper = colors[color]
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    shapeMask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=shapeMask)
    
    # find the contours in the mask
    (_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key = cv2.contourArea)
    
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
    
    print("Red object location in pixels")
    print(cX, cY)
    print("Black board origin coordinates in cms")
    print(cX * cm_pixel_heigth_coefficient, cY * cm_pixel_heigth_coefficient)
    
    cv2.imshow("Image", image)
    cv2.waitKey(0)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
image = cv2.resize(image, (800, 600))
image_height, image_width, _ = image.shape

# find all the 'black' shapes in the image
#lower = np.array([0, 0, 0])
lower = np.array([45, 45, 45])
upper = np.array([65, 65, 65])
#upper = np.array([130, 130, 130])
shapeMask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=shapeMask)

# find the contours in the mask
(_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key = cv2.contourArea)

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
print("Black board origin coordinates in pixels")
xO, yO = xB, image_height - yB
print(xO, yO)
print("Black board origin coordinates in cms")
print(xO * cm_pixel_heigth_coefficient, yO * cm_pixel_heigth_coefficient)


for ((x, y), color) in zip(rect, colors):
	cv2.circle(image, (int(x), int(y)), 5, color, -1)
cv2.imshow("Image", image)
cv2.waitKey(0)

image = cv2.imread(args["image"])

find_color(image, 'red')
find_color(image, 'blue')
find_color(image, 'green')

