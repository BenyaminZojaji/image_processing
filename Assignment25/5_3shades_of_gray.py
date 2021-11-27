import cv2
import numpy as np

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter('result_5.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 5.0, (640, 480))
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    width, height = frame_gray.shape
    
    target = frame_gray[width//4:(width//4)*3, height//4:(height//4)*3]

    kernel = np.ones((45, 45), np.float32)/2025
    frame_gray = cv2.filter2D(frame_gray, -1, kernel, borderType=cv2.BORDER_CONSTANT)

    frame_gray[width//4:(width//4)*3, height//4:(height//4)*3] = target
    cv2.rectangle(frame_gray, (height//4, width//4), ((height//4*3), (width//4*3)), (0, 0, 0), 4)

    target_color = np.average(target)
    if target_color<85:
        cv2.putText(frame_gray, "Black", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    elif target_color<170:
        cv2.putText(frame_gray, "Gray", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    else:
        cv2.putText(frame_gray, "White", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

    out.write(frame)
    cv2.imshow("cam-0", frame_gray)
    if cv2.waitKey(1) == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()