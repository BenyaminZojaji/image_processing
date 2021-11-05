import cv2
import numpy as np

img_arr = np.arange(0, 65025, 1, np.uint8)
img = np.reshape(img_arr, (255, 255))
height, width = img.shape

for i in range(height):
    img[i, :]=height-i

cv2.imwrite('result_6.png', img)