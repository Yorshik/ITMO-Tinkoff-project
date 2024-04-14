import sys
import hashlib
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from registration import Registration
from main_win import MainWindow

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Avtorization(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('avtorization.ui', self)
        self.setWindowTitle("Авторизация")
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        self.sign_in_btn.clicked.connect(self.sign_in)
       
        self.reg_btn.clicked.connect(self.reg)
    
    def sign_in(self):
        hashed_password = hashlib.sha1(f"{self.passwordEdit.text()}".encode()).hexdigest()
        password = self.cur.execute(f"""SELECT password FROM logins WHERE login = ?""", (self.loginEdit.text(),)).fetchall()
        if password and password[0][0] == hashed_password:
            self.main_win = MainWindow(self.loginEdit.text())
            self.main_win.show()
            self.close()
        elif not password or (hashed_password not in password):
            self.errorLabel.setText("Неверный логин или пароль")

    def reg(self):
        self.reg_window = Registration()
        self.reg_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Avtorization()
    plan.show()
    sys.exit(app.exec_())