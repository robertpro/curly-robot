import cv2
import numpy as np


def get_pinzas_direction():
    # read image as grey scale
    img = cv2.imread('../images/figuras/pinzas.png')
    # get image height, width
    (h, w) = img.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)

    scale = 1

    pinzas_dir = {}

    for angle in range(1, 360 + 1):
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(img, M, (h, w))

        pinzas_dir[angle] = rotated

    return pinzas_dir


image1 = cv2.imread("../images/figuras/base2.png")
image2 = cv2.imread("../images/base/base1.jpeg")
image3 = cv2.imread("../images/base/base2.jpeg")
image4 = cv2.imread("../images/base/base3.jpeg")

images = (image1, image2, image3, image4)
images = (image1,)

pinzas_direction = get_pinzas_direction()

for i in range(len(images)):
    print(i)
    for angle in pinzas_direction.keys():
        image = images[i]
        template = pinzas_direction[angle]
        w, h, _ = template.shape[::-1]
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)

        a, b = loc[:2]
        if a.any() or b.any():
            print(angle, w, h)
            print(loc[0], loc[1])
            for pt in zip(*loc[::-1]):
                print(pt, (pt[0] + w, pt[1] + h))
                # cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255))
                cv2.circle(image, pt, pt, (0, 0, 255))
                cv2.imshow('res.png', image)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
