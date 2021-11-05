import cv2
import numpy as np

img_arr = np.arange(0, 90000, 1, np.uint8)
img = np.reshape(img_arr, (300, 300))
height, width = img.shape

img[:,:]=255
img[50:250, 50:100]=0

img[50:90, 100:160]=0
img[210:250, 100:160]=0
img[130:170, 100:160]=0

img[70:140, 160:210]=0
img[160:230, 160:210]=0

cv2.imwrite('result_7.png', img)