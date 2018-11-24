import cv2


def get_orientation():
    # read image as grey scale
    img = cv2.imread('../images/figuras/pinzas.png')
    # get image height, width
    (h, w) = img.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)

    scale = 1

    orientation = {}

    for angle in range(1, 360 + 1):
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(img, M, (h, w))

        orientation[angle] = rotated

    return orientation
