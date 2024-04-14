from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class Description(QMainWindow):
    def __init__(self, text):
        super().__init__()
        uic.loadUi('description.ui', self)
        self.setWindowTitle("Описание")
        self.text = text
        self.initUI()

    def initUI(self):
        self.textEdit.setPlainText(self.text)
