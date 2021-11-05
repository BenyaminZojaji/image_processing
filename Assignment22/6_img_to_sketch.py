import cv2 as cv

img = cv.imread('img/Mona_Lisa.jpg', 0)

inverted = 255 - img
blurred = cv.GaussianBlur(inverted, (21, 21), 0)
inverted_blurred = 255 - blurred

sketch = img / inverted_blurred
sketch = sketch * 255

cv.imwrite('result_6.jpg', sketch)