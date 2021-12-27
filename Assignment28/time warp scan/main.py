import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def time_warp_scan(rows, cols):
    alternate_frame = np.zeros((rows,cols,3))
    
    for i in range(rows):
        ret, frame = cap.read()
        if not ret:
            break

        alternate_frame[i, :] = frame[i, :]
        for j in range(i):
            frame[j, :] = alternate_frame[j, :]                 
        
        cv2.line(frame, (0, i-1), (cols, i-1), (212, 184, 0), 2)

        cv2.imshow('cam', frame)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break
    cv2.imshow('cam', frame)
    cv2.waitKey()
    return alternate_frame # in case we want to save or process the final img later, return it to main

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break    

        cv2.imshow('cam', frame)
                
        if cv2.waitKey(1) & 0xFF == ord('s'):
            rows, cols, _ = frame.shape
            time_warp_scan(rows, cols)
        
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

if __name__=='__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()