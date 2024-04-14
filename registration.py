import sys
import sqlite3
import hashlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox
from PyQt5 import QtCore, QtWidgets
from main_win import MainWindow


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.setWindowTitle("Регистрация")
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.reg_btn.clicked.connect(self.reg)

        self.list_of_checkboxes = [self.dev, self.testing, self.administration, self.management,
                               self.design, self.analytics, self.marketing]


        style_for_edit = """
QLineEdit {
    font: 12pt "Rockwell Condensend";
    border-radius: 15px;
    border: 2px solid rgb(55, 55, 55);
    padding-left: 10px;
    padding-right: 10px;
}
"""
        style_for_btn = """background-color: rgb(255, 255, 255);\n
border-radius: 10px;\n
\n
}\n
QPushButton:hover{    \n
    background-color: rgb(255,204,0);\n
    effect = QtWidgets.QGraphicsDropShadowEffect(QPushButton)\n
    effect.setOffset(0, 0)\n
    effect.setBlurRadius(20)\n
    effect.setColor(QColor(57, 219, 255))\n
    QPushButton.setGraphicsEffect(effect)
    border-radius: 48px;        /* круглый */
border: 2px solid #35544C;
"""
        self.setStyleSheet('.QWidget {background-image: url(backgrounds/regbg.png);}')
        self.nameEdit.setStyleSheet(style_for_edit)
        self.passwordEdit.setStyleSheet(style_for_edit)
        self.reg_btn.setStyleSheet(style_for_btn)


    def reg(self):
        if self.nameEdit.text() and self.passwordEdit.text():
            logins = self.cur.execute(f"""SELECT id FROM logins WHERE login = ?""", (self.nameEdit.text(),)).fetchall()
            if logins:
                self.errorLabel.setText("Такой логин уже существует")
                return
            
            hashed_password = hashlib.sha1(f"{self.passwordEdit.text()}".encode())
            prior = " ".join([elem.text() for elem in self.list_of_checkboxes if elem.isChecked()])
            params = (self.nameEdit.text(), hashed_password.hexdigest(), prior)
            self.cur.execute(f"""INSERT INTO logins ('login', 'password', 'priorities')
                                          VALUES (?, ?, ?)""", params).fetchall()
            self.con.commit()
            self.main_win = MainWindow(self.nameEdit.text())
            self.main_win.show()
            self.close()
        else:
            self.errorLabel.setText("Вы не ввели логин или пароль")
            return
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Registration()
    plan.show()
    sys.exit(app.exec_())