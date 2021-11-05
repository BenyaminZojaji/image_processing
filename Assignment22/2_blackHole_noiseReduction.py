import cv2 as cv
import numpy as np

images = []
for folder in range(1, 5):
    img_sq = np.zeros((1000, 1000), dtype='uint8')
    for img in range(1, 6):
        image = cv.imread(f'img/black hole/{folder}/{img}.jpg', 0)
        img_sq += image//5
    images.append(img_sq)

complete_img = np.zeros((2000, 2000), dtype='uint8')
complete_img[0:1000, 0:1000] = images[0]
complete_img[0:1000, 1000:2000] = images[1]
complete_img[1000:2000, 0:1000] = images[2]
complete_img[1000:2000, 1000:2000] = images[3]

cv.imwrite('result_2.jpg', complete_img)