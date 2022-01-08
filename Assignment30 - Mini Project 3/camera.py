import cv2
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Camera(QWindow):
    def __init__(self, fullname):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/camera.ui', None)
        self.ui.show()
        
        self.fullname = fullname

        self.ui.camera_btn.clicked.connect(self.take_pic)

        detector = cv2.CascadeClassifier("packages/haarcascade_frontalface_default.xml")
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, self.frame = self.cap.read()
            if not ret:
                break

            self.frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame_rgb = cv2.resize(self.frame_rgb, (700,400))
            
            img = QImage(self.frame_rgb, self.frame_rgb.shape[1], self.frame_rgb.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.ui.camera_label.setPixmap(pixmap)

            faces = detector.detectMultiScale(self.frame, 1.3, 10)
            for x,y,w,h in faces:
                self.face = self.frame[y:y+h, x:x+w]
            cv2.waitKey(1)

    def take_pic(self):
        cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.face)
        self.ui.close()