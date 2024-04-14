import webbrowser

import bleach
import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from yandexgptlite import YandexGPTLite
from account import Account
from descript_win import Description

from habr_parse import HabrParser
from hh_parse import HHParser

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

schedule_matches = {
    'Полный день': 'fullDay',
    'Сменный график': 'shift',
    'Гибкий график': 'flexible',
    'Удаленная работа': 'remote',
    'Вахтовый метод': 'flyInFlyOut'
}


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
        self.search_button.clicked.connect(self.search)

    def initUI(self):
        self.style_for_btn = """background-color: rgb(255, 255, 255);\n
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

        style_for_edit = """
        QLineEdit {
            font: 12pt "Rockwell Condensend";
            border-radius: 15px;
            border: 2px solid rgb(55, 55, 55);
            padding-left: 10px;
            padding-right: 10px;
        }
        """

        self.search_line_edit.setStyleSheet(style_for_edit)
        self.to_profile_button.setStyleSheet(self.style_for_btn)
        self.search_button.setStyleSheet(self.style_for_btn)
        self.search_button.clicked.connect(self.search)
        self.search_button.clicked.connect(self.GPT_request)
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
        args = {'text': text_for_pars}
        if self.city_box.currentText() != 'Не выбрано':
            args['city'] = self.city_box.currentText()
        if self.typework_box.currentText() != 'Не выбрано':
            args['schedule'] = schedule_matches[self.typework_box.currentText()]
        if self.salary_box.currentText() != 'Не выбрано':
            args['salary'] = format_salary(self.salary_box.currentText())
        self.hh_parser.set_filters(**args)
        vacancies = self.hh_parser.parse_vacancies()
        self.vacancy_table.setRowCount(len(vacancies))
        for i, row in enumerate(vacancies):
            self.vacancy_table.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{row['employer_name']}"))
            self.vacancy_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{row['vacancy_name']}"))
            self.vacancy_table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{row['salary']}"))
            btn = QtWidgets.QPushButton("Открыть")
            btn.setStyleSheet(self.style_for_btn)
            btn.clicked.connect(lambda: self.open_desc((bleach.clean(row['description'], tags=[], strip=True))))
            btn2 = QtWidgets.QPushButton('Ссылка')
            btn2.setStyleSheet(self.style_for_btn)
            btn2.clicked.connect(lambda: webbrowser.open(row['link']))
            self.vacancy_table.setCellWidget(i, 3, btn)
            self.vacancy_table.setCellWidget(i, 4, btn2)

    def open_desc(self, text):
        self.desc = Description(text)
        self.desc.show()

    def GPT_request(self):
        text_for_pars = self.search_line_edit.text()
        if len(text_for_pars) < 2:
            return
        account = YandexGPTLite('b1gkod9fr73tfg0e4mrl', 'y0_AgAAAAAy_SMVAATuwQAAAAEB6K5tAAAPCIKUDadLH5774KDpceA82ll8Tw')
        text = account.create_completion(
            f'Напиши короткую рекомендацию из трех пунктов как подготовиться к собеседованию на работу {text_for_pars}',
            '0.3')
        self.recommendations_text_edit.setText(text)

    def account(self):
        self.acc_win = Account(self.login)
        self.acc_win.show()


def format_salary(sal):
    return int(sal[3:].replace('.', ''))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow("nikitka1")
    plan.show()
    sys.exit(app.exec_())
