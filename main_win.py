import sys
import os
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHeaderView, QFrame, QButtonGroup
from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PIL import Image

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class MainWindow(QMainWindow):
    def __init__(self, login):
        super().__init__()
        uic.loadUi('main_win.ui', self)
        self.setWindowTitle("Поиск вакансий")

        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
        self.login = login



if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow()
    plan.show()
    sys.exit(app.exec_())