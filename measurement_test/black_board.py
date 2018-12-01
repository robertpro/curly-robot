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

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
image_height, image_width, _ = image.shape

# find all the 'black' shapes in the image
lower = np.array([0, 0, 0])
upper = np.array([130, 130, 130])
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
xB, yB = rect.astype("int")[3]
xL, yL = rect.astype("int")[0] 
xU, _ = rect.astype("int")[1] 
_, yU = rect.astype("int")[2] 
board_width_in_pixels = xU - xL
board_width_in_cm = 222.4
board_heigth_in_pixels = yU - yL
board_heigth_in_cm = 80.35
cm_pixel_width_coefficient = board_width_in_cm / board_width_in_pixels
cm_pixel_heigth_coefficient = board_heigth_in_cm / board_heigth_in_pixels
cm_pixel_coefficient = (cm_pixel_width_coefficient + cm_pixel_heigth_coefficient) / 2
print("Black board origin coordinates in pixels")
xO, yO = xB, image_height - yB
print(xO, yO)
print("Black board origin coordinates in cms")
print(xB * cm_pixel_heigth_coefficient, (image_height - yB) * cm_pixel_heigth_coefficient)
#print(image_width, image_height)
#print("Black board all coordinates")
#print(rect.astype("int"))
for ((x, y), color) in zip(rect, colors):
	cv2.circle(image, (int(x), int(y)), 5, color, -1)
cv2.imshow("Image", image)
cv2.waitKey(0)

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 90, 150)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, _) = contours.sort_contours(cnts)
i = 1 
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
    	continue
    
    # compute the rotated bounding box of the contour, then
    # draw the contours
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # check to see if the new method should be used for
    # ordering the coordinates
    rect = perspective.order_points(box)
    
    # set limits for the size of the objects
    x1, y1 = rect.astype("int")[0] 
    x2, y2 = rect.astype("int")[1] 
    x3, y3 = rect.astype("int")[2] 
    x4, y4 = rect.astype("int")[3] 
    if x2 - x1 > 50 or x2 - x1 < 25:
        #print("x")
        #print(x2 - x1)
        pass
    elif y3 - y2 > 90 or y3 - y2 < 30:
        #print("y")
        #print(y3 - y2)
        pass
    else:
        #print("Object all coordinates")
        #print(rect.astype("int"))
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

        for ((x, y), color) in zip(rect, colors):
        	cv2.circle(image, (int(x), int(y)), 5, color, -1)
        
        # draw the object num at the top-left corner
        cv2.putText(image, "Object #{}".format(i + 1),
        	(int(rect[0][0] - 15), int(rect[0][1] - 15)),
        	cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print("Object {} coordinates in pixels".format(i))
        print(cX, (image_height - cY) - yO)
        print("Object {} coordinates in cms".format(i))
        print(cX * cm_pixel_heigth_coefficient , ((image_height - cY) - yO)* cm_pixel_heigth_coefficient)
        i += 1
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        # draw the contour and center of the shape on the image
        
        # show the image
        cv2.imshow("Image", image)
        cv2.waitKey(0)


