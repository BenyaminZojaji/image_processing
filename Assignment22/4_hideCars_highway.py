import cv2 as cv
import numpy as np

image = np.zeros((240, 320), dtype='uint8')
for i in range(15):
    img = cv.imread(f'img/highway/h{i}.jpg', 0)
    image += img//15

cv.imwrite('result_4.jpg', image)