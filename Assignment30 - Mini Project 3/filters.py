import cv2
import numpy as np

def normal(img):
    return img

def cartoon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def blur(img):
    blur = cv2.blur(img,(5,5))
    return blur

def justRED(img):
    r,g,b=cv2.split(img)
    g=np.ones_like(g)
    b=np.ones_like(b)
    result = cv2.merge((b,g,r))
    result=cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result

def Countours(image):
    contoured_image = image
    gray = cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(gray, 200, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    cv2.drawContours(contoured_image, contours, contourIdx=-1, color=6, thickness=1)

    return contoured_image
def ColourQuantization(image, K=9):
    Z = image.reshape((-1, 3)) 
    Z = np.float32(Z) 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    compactness, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))

    return res2

def cartoonT1(img):
    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    coloured = ColourQuantization(img)
    contoured = Countours(coloured)
    final_image = contoured
    return final_image

def noHue(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h,s,v=cv2.split(img)
    h=np.zeros_like(h)
    result = cv2.merge((h,s,v))
    return result

def noGreen(img):
    r,g,b=cv2.split(img)
    g=np.zeros_like(g)
    result = cv2.merge((b,g,r))
    return result

def noBlue(img):
    r,g,b=cv2.split(img)
    b=np.zeros_like(b)
    result = cv2.merge((b,g,r))
    return result

def noRed(img):
    r,g,b=cv2.split(img)
    r=np.zeros_like(r)
    result = cv2.merge((b,g,r))
    return result
