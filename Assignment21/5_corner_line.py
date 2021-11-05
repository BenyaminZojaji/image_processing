import cv2

img = cv2.imread('img/polar_bear.jpg', 1)

height, width, _ = img.shape

for j in range(400): #height
    for k in range(85): #width
        if not 300-j+k<0:
            img[j][300-j+k]= 0

cv2.imwrite('result_5.png', img)