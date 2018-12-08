#!/usr/bin/env python

import requests
import cv2
import numpy as np

url = "http://192.168.8.4:8080/shot.jpg"

img_resp = requests.get(url)
img_array = np.array(bytearray(img_resp.content), dtype = np.uint8)
img = cv2.imdecode(img_array, -1)
img = cv2.resize(img, (800, 600))

cv2.imshow("Android Cam", img)

cv2.waitKey(0)



