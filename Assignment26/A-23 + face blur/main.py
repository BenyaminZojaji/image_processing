from itertools import compress
import cv2 as cv
import numpy as np
from win10toast import ToastNotifier


def key_managing(key):
    global keys
    keys = list(map(lambda x: False if True else False, keys))
    keys[key] = True


def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    bg_img = background_img.copy()

    if overlay_size is not None:
        img_to_overlay_t = cv.resize(img_to_overlay_t.copy(), overlay_size)

    # Extract the alpha mask of the RGBA image, convert to RGB
    b, g, r, a = cv.split(img_to_overlay_t)
    overlay_color = cv.merge((b, g, r))

    # Apply some simple filtering to remove edge noise
    mask = cv.medianBlur(a, 5)

    h, w, _ = overlay_color.shape
    roi = bg_img[y:y + h, x:x + w]

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv.bitwise_and(roi.copy(), roi.copy(), mask=cv.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv.bitwise_and(overlay_color, overlay_color, mask=mask)

    # Update the original image with new ROI
    bg_img[y:y + h, x:x + w] = cv.add(img1_bg, img2_fg)

    return bg_img


face_detector = cv.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eye_detector = cv.CascadeClassifier('data/haarcascade_eye.xml')
smile_detector = cv.CascadeClassifier('data/haarcascade_smile.xml')

eye_sticker = cv.imread('img/eye.png', -1)
lip_sticker = cv.imread('img/joker_lips.png', -1)
sunglasses_sticker = cv.imread('img/sunglasses.png', -1)

cap = cv.VideoCapture(0)

keys = [False for i in range(5)]

toast = ToastNotifier()
while True:
    ret, frame = cap.read()
    key = cv.waitKey(1)

    if ret:
        if key == 27:  # Esc
            break
        elif key == 49:  # 1
            key_managing(0)
            toast.show_toast('program', 'You choose sunglasses emoji.', duration=2, threaded=True)
        elif key == 50:  # 2
            key_managing(1)
            toast.show_toast('program', 'You choose emoji on lips and eyes.', duration=2, threaded=True)
        elif key == 51:  # 3
            key_managing(2)
            toast.show_toast('program', 'You choose censored face.', duration=2, threaded=True)
        elif key == 52:  # 4
            key_managing(3)
            toast.show_toast('program', 'You choose flip horizontal effect.', duration=2, threaded=True)
        elif key== 53: # 5
            key_managing(4)
            toast.show_toast('program', 'You choose Blur face effect.', duration=2, threaded=True)

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(frame_gray, 1.3, 10)

        for (fa_x, fa_y, fa_w, fa_h) in faces:
            # cv.rectangle(frame_gray, (fa_x, fa_y), (fa_x+fa_w, fa_y+fa_h), (0, 255, 0), 4)
            face_sec = np.zeros((fa_h, fa_w), dtype='uint8')
            face_sec = frame_gray[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w]

            key_pushed = list(compress(range(len(keys)), keys))

            if key_pushed:
                if key_pushed[0] == 0:  # emoji on face
                    frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w] = overlay_transparent(
                        frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w], sunglasses_sticker, 0, 0, (fa_w, fa_h))

                elif key_pushed[0] == 1:  # lip and eyes
                    smiles = smile_detector.detectMultiScale(face_sec, 1.9, 10)
                    eyes = eye_detector.detectMultiScale(face_sec, 1.2, 10)

                    for (eye_x, eye_y, eye_w, eye_h) in eyes:
                        frame[fa_y + eye_y:fa_y + eye_y + fa_h + eye_h,
                        fa_x + eye_x:fa_x + eye_x + fa_w + eye_w] = overlay_transparent(
                            frame[fa_y + eye_y:fa_y + eye_y + fa_h + eye_h, fa_x + eye_x:fa_x + eye_x + fa_w + eye_w],
                            eye_sticker, 0, 0, (eye_w, eye_h))

                    for (sm_x, sm_y, sm_w, sm_h) in smiles:
                        frame[fa_y + sm_y:fa_y + sm_y + fa_h + sm_h,
                        fa_x + sm_x:fa_x + sm_x + fa_w + sm_w] = overlay_transparent(
                            frame[fa_y + sm_y:fa_y + sm_y + fa_h + sm_h, fa_x + sm_x:fa_x + sm_x + fa_w + sm_w],
                            lip_sticker, 0, 0, (sm_w, sm_h))

                elif key_pushed[0] == 2:  # censored face
                    low_quality_img = cv.resize(frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w], (0, 0), fx=0.1, fy=0.1)
                    frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w] = cv.resize(low_quality_img, (fa_w, fa_h),
                                                                          interpolation=cv.INTER_NEAREST)

                    # Note: solution2: nested loop that put the color of first cell into 10x10 ... 

                elif key_pushed[0] == 3: # flip-horizontal effect
                    height, width, _ = frame.shape
                    flipped_img = cv.flip(frame[:, width // 2:width], 1)
                    frame[:, 0:width // 2] = flipped_img
                
                elif key_pushed[0] == 4: # Blur face effect
                    face = frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w]

                    ksize = (30, 30)
                    face = cv.blur(face, ksize, cv.BORDER_DEFAULT)

                    frame[fa_y:fa_y + fa_h, fa_x:fa_x + fa_w] = face

        cv.imshow('cam-0', frame)

cap.release()
cv.destroyWindow('cam-0')