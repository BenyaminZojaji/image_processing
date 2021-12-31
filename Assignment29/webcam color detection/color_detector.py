import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break    
        
        width, height, _ = frame.shape

        b, g, r = cv2.split(frame)

        target = frame[(width//8)*3:(width//8)*5, (height//8)*3:(height//8)*5]

        b_tar, g_tar, r_tar = cv2.split(target)

        alpha = 3 # Contrast control (1.0-3.0)
        beta = 0 # Brightness control (0-100)
        r_tar = cv2.convertScaleAbs(r_tar, alpha=alpha, beta=beta)
        g_tar = cv2.convertScaleAbs(g_tar, alpha=alpha, beta=beta)
        b_tar = cv2.convertScaleAbs(b_tar, alpha=alpha, beta=beta)

        r_avg = round(np.average(r_tar))
        g_avg = round(np.average(g_tar))
        b_avg = round(np.average(b_tar))

        target = cv2.merge((b_tar,g_tar,r_tar))

        kernel = np.ones((45, 45), np.float32)/2025
        b = cv2.filter2D(b, -1, kernel, borderType=cv2.BORDER_CONSTANT)
        g = cv2.filter2D(g, -1, kernel, borderType=cv2.BORDER_CONSTANT)
        r = cv2.filter2D(r, -1, kernel, borderType=cv2.BORDER_CONSTANT)

        frame = cv2.merge((b, g, r))

        frame[(width//8)*3:(width//8)*5, (height//8)*3:(height//8)*5] = target
        cv2.rectangle(frame, (height//8*3, width//8*3), ((height//8*5), (width//8*5)), (0, 255, 0), 4)

        # detect color and put text ... r_avg , b_avg ...
        if r_avg>220 and g_avg>220 and b_avg>220:
            cv2.putText(frame, 'White', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif r_avg<60 and g_avg<60 and b_avg<60:
            cv2.putText(frame, 'Black', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif 170>r_avg>70 and 170>g_avg>70 and 170>b_avg>70:
            cv2.putText(frame, 'Gray', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

        elif r_avg>200 and g_avg<40 and b_avg<40:
            cv2.putText(frame, 'Red', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif r_avg<40 and g_avg>200 and b_avg<40:
            cv2.putText(frame, 'Green', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif r_avg<40 and g_avg<40 and b_avg>200:
            cv2.putText(frame, 'Blue', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

        elif r_avg>200 and g_avg>200 and b_avg<40:
            cv2.putText(frame, 'Yellow', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif r_avg<40 and g_avg>200 and b_avg>200:
            cv2.putText(frame, 'Cyan', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        elif r_avg>200 and g_avg<40 and b_avg>200:
            cv2.putText(frame, 'Magenta', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

        cv2.imshow('cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()