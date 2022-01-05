import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break    

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)###
        HSV_mask = cv2.inRange(frame_hsv, (0, 20, 0), (15,150,255)) 
        HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
        HSV_result = cv2.bitwise_not(HSV_mask)

        img_YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
        YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
        YCrCb_result = cv2.bitwise_not(YCrCb_mask)

        global_mask=cv2.bitwise_and(HSV_result, YCrCb_result)
        global_mask=cv2.medianBlur(global_mask,3)
        global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4,4), np.uint8))
        global_result=cv2.bitwise_not(global_mask)

        skin = cv2.bitwise_and(frame, frame, mask = global_result)
        cv2.imshow('cam', skin)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()