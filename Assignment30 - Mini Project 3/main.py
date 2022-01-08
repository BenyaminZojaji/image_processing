from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import cv2
from numpy.core.numeric import full
import database
import hash
import camera
import filters

class Login(QWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/login.ui', None)
        self.ui.show()

        self.ui.check_btn.clicked.connect(self.check)
    
    def check(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        if database.checkPassword(username, hash.encode(password)):
            self.ui = MainWindow()
        else:
            self.msgBox('wrong Password')

    def msgBox(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()


class Add_employee(QWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/add_employee.ui', None)
        self.ui.show()
        self.id = database.countEmployee()
        
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.add_btn.clicked.connect(self.add)
        self.ui.takepicture.clicked.connect(self.picture)

        self.ui.year.clear()
        for i in range(1900, 2023, 1):
            self.ui.year.addItem(str(i))

    def picture(self):
        firstname = self.ui.firstname.text()
        lastname = self.ui.lastname.text()
        self.ui = camera.Camera(firstname+lastname)

    def add(self):
        firstname = self.ui.firstname.text()
        lastname = self.ui.lastname.text()
        nationalcode = self.ui.nationalcode.text()
        day = self.ui.day.currentText()
        month = self.ui.month.currentText()
        year = self.ui.year.currentText()
        birthday = day + '-' + month + '-' + year
        id = self.id + 1
        database.add_employee(id, firstname, lastname, birthday, nationalcode, imagePath=f'{firstname+lastname}.jpg')
        self.ui = MainWindow()

    def cancel(self):
        self.ui = MainWindow()


class Effect(QWindow):
    def __init__(self, img, fullname):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/filter.ui', None)
        self.ui.show()

        self.fullname = fullname
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(img, (200,200))

        self.cartoon = filters.cartoon(self.img)
        self.image = QImage(self.cartoon, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_2.setIcon(QIcon(self.pix1))
        self.ui.img_2.setIconSize(QSize(150, 150))

        self.justRED = filters.justRED(self.img)
        self.image = QImage(self.justRED, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_1.setIcon(QIcon(self.pix1))
        self.ui.img_1.setIconSize(QSize(150, 150))

        self.blur = filters.blur(self.img)
        self.image = QImage(self.blur, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_3.setIcon(QIcon(self.pix1))
        self.ui.img_3.setIconSize(QSize(150, 150))

        self.cartoonT1 = filters.cartoonT1(self.img)
        self.image = QImage(self.cartoonT1, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_4.setIcon(QIcon(self.pix1))
        self.ui.img_4.setIconSize(QSize(150, 150))

        self.normal = filters.normal(self.img)
        self.image = QImage(self.normal, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_5.setIcon(QIcon(self.pix1))
        self.ui.img_5.setIconSize(QSize(150, 150))

        self.noHue = filters.noHue(self.img)
        self.image = QImage(self.noHue, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_6.setIcon(QIcon(self.pix1))
        self.ui.img_6.setIconSize(QSize(150, 150))

        self.noGreen = filters.noGreen(self.img)
        self.image = QImage(self.noGreen, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_7.setIcon(QIcon(self.pix1))
        self.ui.img_7.setIconSize(QSize(150, 150))

        self.noBlue = filters.noBlue(self.img)
        self.image = QImage(self.noBlue, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_8.setIcon(QIcon(self.pix1))
        self.ui.img_8.setIconSize(QSize(150, 150))

        self.noRed = filters.noRed(self.img)
        self.image = QImage(self.noRed, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix1 = QPixmap.fromImage(self.image)
        self.ui.img_9.setIcon(QIcon(self.pix1))
        self.ui.img_9.setIconSize(QSize(150, 150))


        self.ui.img_1.clicked.connect(self.select)
        self.ui.img_2.clicked.connect(self.select)
        self.ui.img_3.clicked.connect(self.select)
        self.ui.img_4.clicked.connect(self.select)
        self.ui.img_5.clicked.connect(self.select)
        self.ui.img_6.clicked.connect(self.select)
        self.ui.img_7.clicked.connect(self.select)
        self.ui.img_8.clicked.connect(self.select)
        self.ui.img_9.clicked.connect(self.select)

    def select(self):
        mode = int(self.sender().objectName().split('_')[-1])
        if mode==1:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.justRED)
        elif mode==2:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.cartoon)
        elif mode==3:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.blur)
        elif mode==4:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.cartoonT1)
        elif mode==5:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.normal)
        elif mode==6:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.noHue)
        elif mode==7:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.noGreen)
        elif mode==8:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.noBlue)
        elif mode==9:
            cv2.imwrite(f'img/user_images/{self.fullname}.jpg', self.noRed)
        self.ui = MainWindow()

class Edit_employee(QWindow):
    def __init__(self, id):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/edit_employee.ui', None)
        self.ui.show()
        self.id = id
        self.employee = database.get_employee_detail(self.id)[0]

        self.ui.year.clear()
        for i in range(1900, 2023, 1):
            self.ui.year.addItem(str(i))
        
        self.ui.firstname.setText(self.employee[1])
        self.ui.lastname.setText(self.employee[2])
        self.ui.nationalcode.setText(str(self.employee[4]))
        birthday=list(self.employee[3].split('-'))
        self.ui.year.setCurrentText(birthday[2])
        self.ui.month.setCurrentText(birthday[1])
        self.ui.day.setCurrentText(birthday[0])

        self.ui.image_effect_btn.clicked.connect(self.effect)
        self.ui.done_btn.clicked.connect(self.done)
        self.ui.cancel_btn.clicked.connect(self.cancel)

    def effect(self):
        img=cv2.imread(f'img/user_images/{self.employee[1]+self.employee[2]}.jpg')
        self.ui = Effect(img, self.employee[1]+self.employee[2])

    def done(self):
        firstname = self.ui.firstname.text()
        lastname = self.ui.lastname.text()
        nationalcode = self.ui.nationalcode.text()
        day = self.ui.day.currentText()
        month = self.ui.month.currentText()
        year = self.ui.year.currentText()
        birthday = day + '-' + month + '-' + year
        database.edit_employee(self.id, firstname, lastname, birthday, nationalcode, imagePath=f'{firstname+lastname}.jpg')
        self.ui = MainWindow()

    def cancel(self):
        self.ui = MainWindow()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('Ui/main.ui', None)
        self.ui.show()

        self.ui.addEmployee_btn.clicked.connect(self.add_employee)

        self.readFromDataBase()


    def add_employee(self):
        self.ui = Add_employee()

    def readFromDataBase(self):
        result = database.get_all_employee() # (1, 'benyamin', 'zojaji', '12-3-1950', 321555, 'benyaminzojaji.jpg')
        for i in range(len(result)):
            id_label = QLabel() # id
            id_label.setText(str(result[i][0]))

            fullName_label = QLabel() # Full Name
            fullName_label.setText(result[i][1]+' '+result[i][2])

            edit_btn = QPushButton() # edit
            edit_btn.setStyleSheet('border:0px;')
            edit_btn.setObjectName(f'edit_btn_{result[i][0]}')
            edit_btn.setIcon(QIcon('img/icon/edit_black.png'))
            edit_btn.clicked.connect(self.edit)

            delete_btn = QPushButton() # delete
            delete_btn.setStyleSheet('border:0px;')
            delete_btn.setObjectName(f'delete_btn_{result[i][0]}')
            delete_btn.setIcon(QIcon('img/icon/delete.png'))
            delete_btn.clicked.connect(self.delete)

            avatar_btn = QPushButton() # avatar image
            avatar_btn.setStyleSheet('max-width: 75px; min-height: 75px; border: 0px; border-radius: 30px;')
            avatar_btn.setIcon(QIcon(f'img/user_images/{result[i][5]}'))
            avatar_btn.setIconSize(QSize(75, 75))

            # tasks layout
            self.ui.grid_emp_list.addWidget(id_label, i, 0)
            self.ui.grid_emp_list.addWidget(avatar_btn, i, 1)
            self.ui.grid_emp_list.addWidget(fullName_label, i, 2)
            self.ui.grid_emp_list.addWidget(edit_btn, i, 3)
            self.ui.grid_emp_list.addWidget(delete_btn, i, 4)

    def edit(self):
        id = self.sender().objectName().split('_')[-1]
        self.ui = Edit_employee(id)

    def delete(self):
        id = self.sender().objectName().split('_')[-1]
        database.delete_employee(id)
        self.clearUI_employee()
        self.readFromDataBase()

    def clearUI_employee(self):
        for i in reversed(range(self.ui.grid_emp_list.count())): 
            self.ui.grid_emp_list.itemAt(i).widget().deleteLater()



if __name__=='__main__':
    app = QApplication([])
    window = Login()
    app.exec()