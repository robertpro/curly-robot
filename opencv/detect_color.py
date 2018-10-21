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
boundaries = [
    # ([15, 15, 110], [90, 90, 255]),  # Red
    ([86, 31, 4], [220, 96, 50]),  # Blue
    # ([25, 116, 160], [110, 194, 250]),  # Yellow
    # ([45, 70, 10], [100, 250, 90]),  # Green
]

masks = []

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    # output = cv2.bitwise_and(image, image, mask=mask)

    # show the images
    # cv2.imshow("images", np.hstack([image, output]))
    # cv2.waitKey(0)

    masks.append(mask)

if len(masks) > 2:
    new_mask = None
    for i in range(len(masks) - 1):
        lower = np.array(boundaries[0][0], dtype="uint8")
        upper = np.array(boundaries[0][1], dtype="uint8")
        if new_mask is None:
            new_mask = cv2.inRange(image, lower, upper)
            continue
        new_mask = cv2.bitwise_or(new_mask, masks[i + 1])

elif len(masks) == 2:
    new_mask = cv2.bitwise_or(*masks)
else:
    new_mask = cv2.inRange(image, lower, upper)

output = cv2.bitwise_and(image, image, mask=new_mask)

cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)
