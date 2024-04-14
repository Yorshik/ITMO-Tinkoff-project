import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from account import Account


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

        self.priorities = self.cur.execute(f"""SELECT priorities FROM logins WHERE login = '{self.login}'""").fetchall()[0][0].split()
        
        print(self.priorities)

        self.search_button.clicked.connect(self.search)
        self.to_profile_button.clicked.connect(self.account)

    def search(self):
        text_for_pars = self.search_line_edit.text()
        if len(text_for_pars) < 5:
            return
        else:
            """Парсим по запросу и выводим в таблицу"""
            pass

    def account(self):
        self.acc_win = Account(self.login)
        self.acc_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow()
    plan.show()
    sys.exit(app.exec_())