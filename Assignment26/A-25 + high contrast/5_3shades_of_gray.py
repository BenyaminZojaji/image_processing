import cv2
import numpy as np
# I found 3 ways for contrast adjustment

# 1:
# def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
#     if brightness != 0:
#         if brightness > 0:
#             shadow = brightness
#             highlight = 255
#         else:
#             shadow = 0
#             highlight = 255 + brightness
#         alpha_b = (highlight - shadow)/255
#         gamma_b = shadow
        
#         buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
#     else:
#         buf = input_img.copy()
    
#     if contrast != 0:
#         f = 131*(contrast + 127)/(127*(131-contrast))
#         alpha_c = f
#         gamma_c = 127*(1-f)
        
#         buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

#     return buf


cap = cv2.VideoCapture(0)
out = cv2.VideoWriter('result2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10.0, (640, 480))
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    width, height = frame_gray.shape
    
    target = frame_gray[(width//8)*3:(width//8)*5, (height//8)*3:(height//8)*5]

    kernel = np.ones((45, 45), np.float32)/2025
    frame_gray = cv2.filter2D(frame_gray, -1, kernel, borderType=cv2.BORDER_CONSTANT)

    # 2:
    #enhanced_target = cv2.equalizeHist(target)
    # clahe = cv2.createCLAHE(clipLimit=4)
    # enhanced_target = clahe.apply(enhanced_target)

    # 3:
    alpha = 3 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    enhanced_target = cv2.convertScaleAbs(target, alpha=alpha, beta=beta)

    frame_gray[(width//8)*3:(width//8)*5, (height//8)*3:(height//8)*5] = enhanced_target
    cv2.rectangle(frame_gray, (height//8*3, width//8*3), ((height//8*5), (width//8*5)), (0, 0, 0), 4)


    target_color = np.average(enhanced_target)
    if target_color<85:
        cv2.putText(frame_gray, "Black", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    elif target_color<170:
        cv2.putText(frame_gray, "Gray", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    else:
        cv2.putText(frame_gray, "White", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

    out.write(frame_gray)
    cv2.imshow("cam-0", frame_gray)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()