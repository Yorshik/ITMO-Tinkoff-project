import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Account(QMainWindow):
    def __init__(self, login):
        super().__init__()
        uic.loadUi('account.ui', self)
        self.setWindowTitle("Профиль")

        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
        self.login = login

        self.hello_label.setText(f"Привет, {login}")
        #self.favourite_edit
        #self.history_edit




if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Account()
    plan.show()
    sys.exit(app.exec_())