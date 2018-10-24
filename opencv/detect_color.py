# import the necessary packages
import numpy as np
import cv2

# load the image
image = cv2.imread("../images/figuras/red.png")
image = cv2.imread("../images/figuras/blue.png")
image = cv2.imread("../images/figuras/green.png")
image = cv2.imread("../images/figuras/yellow.png")
image = cv2.imread("../images/figuras/base2.png")


# define the list of boundaries


def boundary(x: list) -> np.array:
    return np.array(x, dtype="uint8")


boundaries = {
    'red': {
        'lower': boundary([15, 15, 110]),
        'upper': boundary([90, 90, 255]),
    },
    'blue': {
        'lower': boundary([86, 31, 4]),
        'upper': boundary([220, 96, 50]),
    },
    'yellow': {
        'lower': boundary([25, 116, 160]),
        'upper': boundary([110, 194, 250]),
    },
    'green': {
        'lower': boundary([45, 70, 10]),
        'upper': boundary([100, 250, 90]),
    },
}

masks = []

# loop over the boundaries
for color in boundaries.keys():
    lower = boundaries[color].get('lower')
    upper = boundaries[color].get('upper')

    masks.append(cv2.inRange(image, lower, upper))

mask = sum(masks)

output = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)
