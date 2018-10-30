import cv2
import numpy as np


template = cv2.imread('../images/figuras/pinzas.png', 1)
image = cv2.imread("../images/figuras/base2.png")

w, h, _ = template.shape[::-1]

res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imshow('res.png', image)
cv2.waitKey(0)
