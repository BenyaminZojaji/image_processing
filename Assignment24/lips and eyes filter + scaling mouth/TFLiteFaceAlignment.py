#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
import sys
import time
from functools import partial
from scipy.spatial import distance as dist
import numpy as np
import cv2
import tensorflow as tf
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

def scaling_zoom_effect(frame, landmarks, scale):
    x, y, w, h = cv2.boundingRect(landmarks)
    
    if scale==1: 
        size_diff = 0 # half of size difference
    elif scale==2:
        size_diff = 0.5 # 2-1=x x/2=1 ^^
    elif scale==4:
        size_diff = 1.5 # 4-1=3 3/2 = 1.5

    rows, cols, _ = frame.shape
    mask = np.zeros((rows, cols, 3), dtype="uint8")
    
    cv2.drawContours(mask, [landmarks], -1, (255, 255, 255), -1)
    
    frame_scale = cv2.resize(frame, None, fx=scale, fy=scale)
    mask_scale = cv2.resize(mask, None, fx=scale, fy=scale)
    
    frame_scale = frame_scale / 255
    mask_scale = mask_scale / 255

    frame_target = frame[int(y - (h * size_diff)) : int(y + h + (h * size_diff)), int(x - (w * size_diff)) : int(x + w + (w * size_diff))]
    frame_target = frame_target / 255
    
    foreground = cv2.multiply(mask_scale, frame_scale)
    try:
        background = cv2.multiply(frame_target, 1 - mask_scale[y * scale : (y + h) * scale, x * scale : (x + w) * scale])
        res = cv2.add(background, foreground[y * scale : (y + h) * scale, x * scale : (x + w) * scale])
        frame[int(y-(h*size_diff)) : int(y+h+(h*size_diff)), int(x-(w*size_diff)):int(x+w+(w*size_diff))] = res*255
    finally:
        return frame

def get_mouthAspectRatio(landmarks): #detect open-closed lips and return scale
    # compute the euclidean distance between the vertical
    vertical_dist = dist.euclidean(landmarks[9], landmarks[3]) # 71 53

	# compute the euclidean distance between the horizontal
    horizontal_dist = dist.euclidean(landmarks[0], landmarks[6]) # 52 69

	# compute the mouth aspect ratio
    mouth_aspect_ratio = vertical_dist / horizontal_dist

    if mouth_aspect_ratio < 0.45: # closed lips < 0.45
        return 1
    elif mouth_aspect_ratio < 0.8:
        return 2
    else:
        return 4

if __name__ == '__main__':
    fd = UltraLightFaceDetecion("weights/RFB-320.tflite", conf_threshold=0.88)
    fa = CoordinateAlignmentModel("weights/coor_2d106.tflite")

    cap = cv2.VideoCapture(0)
    # VideoWriter('filename.format', fourcc, fps, size)
    # fourcc: mp4 -> *X264 works as well as MP4V for mp4 format.
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 5.0, (640, 480))

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
            
            frame = scaling_zoom_effect(frame, landmarks_left_eye, 2)
            frame = scaling_zoom_effect(frame, landmarks_right_eye, 2)

            mouth_aspectRatio = get_mouthAspectRatio(landmarks_lips)
            frame = scaling_zoom_effect(frame, landmarks_lips, mouth_aspectRatio)


        out.write(frame)
        cv2.imshow("cam-0", frame)
        if cv2.waitKey(1) == ord('q'):
                break
    cap.release()
    out.release()
    cv2.destroyAllWindows()