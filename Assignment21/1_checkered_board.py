import cv2
import numpy as np

img_arr = np.arange(0, 640000, 1, np.uint8)
img_arr = np.reshape(img_arr, (800, 800))
height, width = img_arr.shape

for i in range(height):
    for j in range(width):   
        if ((i//(width/8))%2+(j//(width/8))%2)%2==0:
            img_arr[i][j]=255
        else:
            img_arr[i][j]=0

cv2.imwrite('result_1.png', img_arr)