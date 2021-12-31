from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('form.ui', None)
        self.ui.show()

        self.ui.r_slider.valueChanged.connect(self.color)
        self.ui.g_slider.valueChanged.connect(self.color)
        self.ui.b_slider.valueChanged.connect(self.color)
        
    def color(self):
        r = self.ui.r_slider.value()
        g = self.ui.g_slider.value()
        b = self.ui.b_slider.value()
        
        self.ui.r_label.setText(str(r))
        self.ui.g_label.setText(str(g))
        self.ui.b_label.setText(str(b))

        self.ui.graphicsView.setStyleSheet(f'background-color: rgb({r}, {g}, {b});')

if __name__=='__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()