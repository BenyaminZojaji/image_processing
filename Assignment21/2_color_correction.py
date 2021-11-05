import cv2

img1 = cv2.imread('img/1.jpg')
img2 = cv2.imread('img/2.jpg')

inverted_img1 = cv2.bitwise_not(img1)
inverted_img2 = cv2.bitwise_not(img2)

cv2.imwrite('result_2_1.png', inverted_img1)
cv2.imwrite('result_2_2.png', inverted_img2)