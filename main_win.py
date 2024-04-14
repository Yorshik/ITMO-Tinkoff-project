import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from account import Account

from habr_parse import HabrParser
from hh_parse import HHParser

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
        self.initUI()

    def initUI(self):
        self.search_button.clicked.connect(self.search)
        self.to_profile_button.clicked.connect(self.account)
        self.init_news()

    def init_news(self):
        self.parameters = ["Разработка", "Маркетинг"]
        self.habr_parser = HabrParser()
        self.news_text_edit.setReadOnly(True)
        text = self.habr_parser.parse(self.parameters[-1])
        string = ""
        for vacancy in text:
            string += vacancy["title"] + "\n" + vacancy["salary"] + "\n" + vacancy["place"] + "\n" + vacancy["company"] + "\n\n"
        self.news_text_edit.setPlainText(string)

    def init_vacancies(self):
        self.hh_parser = HHParser()

    def set_filters(self):
        self.hh_parser.set_filters()  # TODO get filters

    def search(self):
        text_for_pars = self.search_line_edit.text()
        if len(text_for_pars) < 2:
            return
        else:
            """Парсим по запросу и выводим в таблицу"""
            pass

    def account(self):
        self.acc_win = Account(self.login)
        self.acc_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow("nikitka1")
    plan.show()
    sys.exit(app.exec_())
