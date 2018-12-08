#!/usr/bin/env python

# import the necessary packages
import numpy as np
import argparse
import cv2
import imutils
from scipy.spatial import distance as dist
from imutils import contours
from imutils import perspective

def order_points(pts):
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
 
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
 
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
 
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
 
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl], dtype="float32")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

# find all the 'black' shapes in the image
lower = np.array([0, 0, 0])
upper = np.array([130, 130, 130])
shapeMask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=shapeMask)

# find the contours in the mask
(_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print("I found %d black shapes" % (len(cnts)))
cv2.imshow("Mask", shapeMask)

# loop over the contours
for c in cnts:
	# draw the contour and show it
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)

c = max(cnts, key = cv2.contourArea)
cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
cv2.imshow("Image", image)
#x,y,w,h = cv2.boundingRect(c)
## draw the book contour (in green)
#cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
cv2.waitKey(0)

# compute the rotated bounding box of the contour, then
# draw the contours
box = cv2.minAreaRect(c)
box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
box = np.array(box, dtype="int")

cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

# show the original coordinates
print("Black board coordinates")
print(box)
colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
rect = order_points(box)
print(rect.astype("int"))
for ((x, y), color) in zip(rect, colors):
	cv2.circle(image, (int(x), int(y)), 5, color, -1)
cv2.imshow("Image", image)
cv2.waitKey(0)

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 190, 250)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
cv2.imshow("edged", edged)
cv2.waitKey(0)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, _) = contours.sort_contours(cnts)
for (i, c) in enumerate(cnts):
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
    	continue
    
    # compute the rotated bounding box of the contour, then
    # draw the contours
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # show the original coordinates
    #print("Object #{}:".format(i + 1))
    #print(box)
    
    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    
    # check to see if the new method should be used for
    # ordering the coordinates
    rect = perspective.order_points(box)
    
    # show the re-ordered coordinates
    print("")
    
    # loop over the original points and draw them

    x1, y1 = rect.astype("int")[0] 
    x2, y2 = rect.astype("int")[1] 
    x3, y3 = rect.astype("int")[2] 
    x4, y4 = rect.astype("int")[3] 
    if x2 - x1 > 170 or x2 - x1 < 135:
        print("x")
        print(x2 - x1)
        pass
    elif y3 - y2 > 210 or y3 - y2 < 180:
        print("y")
        print(y3 - y2)
        pass
    else:
        print("Lego robot")
        print(rect.astype("int"))
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
        print(cX, cY)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        # draw the contour and center of the shape on the image
        
        # show the image
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
cv2.imshow("edged", edged)
cv2.waitKey(0)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, _) = contours.sort_contours(cnts)
for (i, c) in enumerate(cnts):
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
    	continue
    
    # compute the rotated bounding box of the contour, then
    # draw the contours
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # show the original coordinates
    #print("Object #{}:".format(i + 1))
    #print(box)
    
    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    
    # check to see if the new method should be used for
    # ordering the coordinates
    rect = perspective.order_points(box)
    
    # show the re-ordered coordinates
    print("")
    
    # loop over the original points and draw them

    x1, y1 = rect.astype("int")[0] 
    x2, y2 = rect.astype("int")[1] 
    x3, y3 = rect.astype("int")[2] 
    x4, y4 = rect.astype("int")[3] 
    if x2 - x1 > 50 or x2 - x1 < 25:
        print("x")
        print(x2 - x1)
        pass
    elif y3 - y2 > 90 or y3 - y2 < 30:
        print("y")
        print(y3 - y2)
        pass
    else:
        print("Lego robot")
        print(rect.astype("int"))
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
        print(cX, cY)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        # draw the contour and center of the shape on the image
        
        # show the image
        cv2.imshow("Image", image)
        cv2.waitKey(0)


