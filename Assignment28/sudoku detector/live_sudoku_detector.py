import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils.perspective import four_point_transform 

parser = argparse.ArgumentParser(description='Benyamin Zojaji Live Sudoku Detector - 25 Dec 2021')
parser.add_argument('--input', type=str, help='device number', default=0)
parser.add_argument('--output', type=str, help='path of your output image', default='sudoku.jpg')
parser.add_argument('--kernel_size', type=int, help='blur kernel size', default=7)
parser.add_argument('--color', type=tuple, help='sudoku detector color ', default=(0, 255, 0))
args = parser.parse_args()

cap = cv2.VideoCapture(args.input)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_blurred = cv2.GaussianBlur(frame_gray, (args.kernel_size, args.kernel_size), 3)

    thresh = cv2.adaptiveThreshold(frame_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sudoku_contour = None

    for contour in contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            sudoku_contour = approx
            break
    
    if sudoku_contour is None:
        pass
    else:
        cv2.drawContours(frame, [sudoku_contour], -1, args.color, 20)

        # I found 2 ways to transform an image.
        # 1:
        warped = four_point_transform(frame, approx.reshape(4,2))
        warped = cv2.resize(warped, (500, 500))

        # 2:
        # src_pts = np.array([sudoku_contour[1], sudoku_contour[0], sudoku_contour[3], sudoku_contour[2]], dtype=np.float32)
        # dst_pts = np.array([[0, 0],   [500, 0],  [500, 500], [0, 500]], dtype=np.float32)
        # M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        # warped = cv2.warpPerspective(frame, M, (500, 500))

        cv2.imshow('cam', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(args.output, warped)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()