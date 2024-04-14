import bleach
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

        self.priorities = self.cur.execute(f"""SELECT priorities FROM logins WHERE login = '{self.login}'""").fetchall()[0][0].split()
        
        self.initUI()

    def initUI(self):
        self.search_button.clicked.connect(self.search)
        self.to_profile_button.clicked.connect(self.account)
        self.init_news()
        self.init_vacancies()

    def init_news(self):
        self.habr_parser = HabrParser()
        self.news_text_edit.setReadOnly(True)
        text = self.habr_parser.parse(self.priorities[-1])
        string = ""
        for vacancy in text:
            string += vacancy["title"] + "\n" + vacancy["salary"] + "\n" + vacancy["place"] + "\n" + vacancy[
                "company"] + "\n\n"
        self.news_text_edit.setPlainText(string)

    def init_vacancies(self):
        self.hh_parser = HHParser()

    def set_filters(self):
        self.hh_parser.set_filters()  # TODO get filters

    def search(self):
        text_for_pars = self.search_line_edit.text()
        if len(text_for_pars) < 2:
            return
        """Парсим по запросу и выводим в таблицу"""
        args = {}
        if self.city_box.currentText() != 'Не выбрано':
            args['city'] = self.city_box.currentText()
        if self.typework_box.currentText() != 'Не выбрано':
            args['schedule'] = self.typework_box.currentText()
        if self.salary_box.currentText() != 'Не выбрано':
            args['salary'] = self.salary_box.currentText()
        self.hh_parser.set_filters(**args)
        vacancies = self.hh_parser.parse_vacancies()
        self.vacancy_table.setRowCount(len(vacancies))
        for i, row in enumerate(vacancies):
            self.vacancy_table.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{row['employer_name']}"))
            self.vacancy_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{row['vacancy_name']}"))
            self.vacancy_table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{row['salary']}"))
            self.vacancy_table.setItem(i, 3, QtWidgets.QTableWidgetItem(
                bleach.clean(row['description'], tags=[], strip=True)))
            self.vacancy_table.setItem(i, 4, QtWidgets.QTableWidgetItem(row['link']))

    def account(self):
        self.acc_win = Account(self.login)
        self.acc_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow("nikitka1")
    plan.show()
    sys.exit(app.exec_())
