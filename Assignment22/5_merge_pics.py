import cv2 as cv
import numpy as np

my_img = cv.imread('img/me.jpg', 0)
eliot_img = cv.imread('img/eliot.jpg', 0)

height, width = my_img.shape
eliot_img = cv.resize(eliot_img, (height, width))

merge1 = my_img//2 + eliot_img//4
merge2 = my_img//4 + eliot_img//2

result = np.zeros((height, width*4), dtype='uint8')

result[0:height, 0:width]=my_img
result[0:height, width:width*2]=merge1
result[0:height, width*2:width*3]=merge2
result[0:height, width*3:width*4]=eliot_img

cv.imwrite('result_5.jpg', result)