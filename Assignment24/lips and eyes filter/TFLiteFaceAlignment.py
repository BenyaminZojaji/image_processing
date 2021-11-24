#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import sys
import numpy as np
import cv2
import tensorflow as tf
from functools import partial
from TFLiteFaceDetector import UltraLightFaceDetecion


class CoordinateAlignmentModel():
    def __init__(self, filepath, marker_nums=106, input_size=(192, 192)):
        self._marker_nums = marker_nums
        self._input_shape = input_size
        self._trans_distance = self._input_shape[-1] / 2.0

        self.eye_bound = ([35, 41, 40, 42, 39, 37, 33, 36],
                          [89, 95, 94, 96, 93, 91, 87, 90])

        # tflite model init
        self._interpreter = tf.lite.Interpreter(model_path=filepath)
        self._interpreter.allocate_tensors()

        # model details
        input_details = self._interpreter.get_input_details()
        output_details = self._interpreter.get_output_details()

        # inference helper
        self._set_input_tensor = partial(self._interpreter.set_tensor,
                                         input_details[0]["index"])
        self._get_output_tensor = partial(self._interpreter.get_tensor,
                                          output_details[0]["index"])

        self.pre_landmarks = None

    def _calibrate(self, pred, thd, skip=6):
        if self.pre_landmarks is not None:
            for i in range(pred.shape[0]):
                if abs(self.pre_landmarks[i, 0] - pred[i, 0]) > skip:
                    self.pre_landmarks[i, 0] = pred[i, 0]
                elif abs(self.pre_landmarks[i, 0] - pred[i, 0]) > thd:
                    self.pre_landmarks[i, 0] += pred[i, 0]
                    self.pre_landmarks[i, 0] /= 2

                if abs(self.pre_landmarks[i, 1] - pred[i, 1]) > skip:
                    self.pre_landmarks[i, 1] = pred[i, 1]
                elif abs(self.pre_landmarks[i, 1] - pred[i, 1]) > thd:
                    self.pre_landmarks[i, 1] += pred[i, 1]  
                    self.pre_landmarks[i, 1] /= 2
        else:
            self.pre_landmarks = pred

    def _preprocessing(self, img, bbox, factor=3.0):
        """Pre-processing of the BGR image. Adopting warp affine for face corp.

        Arguments
        ----------
        img {numpy.array} : the raw BGR image.
        bbox {numpy.array} : bounding box with format: {x1, y1, x2, y2, score}.

        Keyword Arguments
        ----------
        factor : max edge scale factor for bounding box cropping.

        Returns
        ----------
        inp : input tensor with NHWC format.
        M : warp affine matrix.
        """

        maximum_edge = max(bbox[2:4] - bbox[:2]) * factor
        scale = self._trans_distance * 4.0 / maximum_edge
        center = (bbox[2:4] + bbox[:2]) / 2.0
        cx, cy = self._trans_distance - scale * center

        M = np.array([[scale, 0, cx], [0, scale, cy]])

        cropped = cv2.warpAffine(img, M, self._input_shape, borderValue=0.0)
        inp = cropped[..., ::-1].astype(np.float32)

        return inp[None, ...], M

    def _inference(self, input_tensor):
        self._set_input_tensor(input_tensor)
        self._interpreter.invoke()

        return self._get_output_tensor()[0]

    def _postprocessing(self, out, M):
        iM = cv2.invertAffineTransform(M)
        col = np.ones((self._marker_nums, 1))

        out = out.reshape((self._marker_nums, 2))

        out += 1
        out *= self._trans_distance

        out = np.concatenate((out, col), axis=1)

        return out @ iM.T  # dot product

    def get_landmarks(self, image, detected_faces=None):
        """Predict the landmarks for each face present in the image.

        This function predicts a set of 68 2D or 3D images, one for each image present.
        If detect_faces is None the method will also run a face detector.

        Arguments
        ----------
        image {numpy.array} : The input image.

        Keyword Arguments
        ----------
        detected_faces {list of numpy.array} : list of bounding boxes, one for each
        face found in the image (default: {None}, format: {x1, y1, x2, y2, score})
        """

        for box in detected_faces:
            inp, M = self._preprocessing(image, box)
            out = self._inference(inp)
            pred = self._postprocessing(out, M)

            # self._calibrate(pred, 1, skip=6)
            # yield self.pre_landmarks

            yield pred


# left eye: 35 36 33 37 39 42 40 41
# right eye: 89 90 87 91 93 96 94 95
# lip: 52 55 56 53 59 58 69 68 67 71 63 64

def zoom_effect(frame, landmarks):
    x, y, w, h = cv2.boundingRect(landmarks)

    rows, cols, _ = frame.shape
    mask = np.zeros((rows, cols, 3), dtype="uint8")

    cv2.drawContours(mask, [landmarks], -1, (255, 255, 255), -1)

    frame_2x = cv2.resize(frame, None, fx=2, fy=2)
    mask_2x = cv2.resize(mask, None, fx=2, fy=2)

    frame_2x = frame_2x / 255
    mask_2x = mask_2x / 255

    frame_target = frame[int(y-(h*0.5)):int(y+h+(h*0.5)), int(x-(w*0.5)):int(x+w+(w*0.5))]
    frame_target = frame_target / 255

    foreground = cv2.multiply(mask_2x, frame_2x)
    background = cv2.multiply(frame_target, 1 - mask_2x[y*2:(y+h)*2, x*2:(x+w)*2])
    res = cv2.add(background, foreground[y*2:(y+h)*2, x*2:(x+w)*2])
    frame[int(y-(0.5*h)):int(y+h+(0.5*h)), int(x-(0.5*w)):int(x+w+(0.5*w))] = res *255
    return frame


if __name__ == '__main__':
    fd = UltraLightFaceDetecion("weights/RFB-320.tflite", conf_threshold=0.88)
    fa = CoordinateAlignmentModel("weights/coor_2d106.tflite")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rows, cols, _ = frame.shape

        boxes, scores = fd.inference(frame)

        for pred in fa.get_landmarks(frame, boxes):
            pred_int = np.round(pred).astype(np.int)
            
            landmarks_left_eye = []
            for i in [35, 36, 33, 37, 39, 42, 40, 41]:
                landmarks_left_eye.append(tuple(pred_int[i]))

            landmarks_right_eye = []
            for i in [89, 90, 87, 91, 93, 96, 94, 95]:
                landmarks_right_eye.append(tuple(pred_int[i]))

            landmarks_lips = []
            for i in [52, 55, 56, 53, 59, 58, 69, 68, 67, 71, 63, 64]:
                landmarks_lips.append(tuple(pred_int[i]))

            landmarks_left_eye = np.array(landmarks_left_eye)
            landmarks_right_eye = np.array(landmarks_right_eye)
            landmarks_lips = np.array(landmarks_lips)
            
            
            # cv2.drawContours(mask, [landmarks_left_eye], -1, (255, 255, 255), -1)
            # cv2.drawContours(mask, [landmarks_right_eye], -1, (255, 255, 255), -1)
            # cv2.drawContours(mask, [landmarks_lips], -1, (255, 255, 255), -1)

            # for index, p in enumerate(np.round(pred).astype(np.int)):
            #     # print(p, index)
            #     cv2.circle(image, tuple(p), 1, (125, 255, 125), 1, cv2.LINE_AA)
            #     cv2.putText(image, str(index), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            frame = zoom_effect(frame, landmarks_lips)
            frame = zoom_effect(frame, landmarks_left_eye)
            frame = zoom_effect(frame, landmarks_right_eye)


        #cv2.imwrite("output/result.jpg", frame)
        cv2.imshow("cam-0", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



# if __name__ == '__main__':

#     from TFLiteFaceDetector import UltraLightFaceDetecion
#     import sys

#     fd = UltraLightFaceDetecion(
#         "weights/RFB-320.tflite",
#         conf_threshold=0.88)
#     fa = CoordinateAlignmentModel(
#         "weights/coor_2d106.tflite")

#     cap = cv2.VideoCapture(sys.argv[1])
#     color = (125, 255, 125)

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             break

#         start_time = time.perf_counter()

#         boxes, scores = fd.inference(frame)

#         for pred in fa.get_landmarks(frame, boxes):
#             for p in np.round(pred).astype(np.int):
#                 cv2.circle(frame, tuple(p), 1, color, 1, cv2.LINE_AA)

#         print(time.perf_counter() - start_time)

#         cv2.imshow("result", frame)
#         if cv2.waitKey(0) == ord('q'):
#             break
