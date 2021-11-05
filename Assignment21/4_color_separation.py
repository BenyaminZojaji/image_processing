import cv2

img = cv2.imread('img/4.jpg', 0)
height, width = img.shape

for i in range(height):
    for j in range(width):
        if img[i][j]<110:
            img[i][j] = 0

cv2.imwrite('result_4.png', img)