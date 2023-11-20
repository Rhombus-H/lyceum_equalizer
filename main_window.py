import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('static/main_window.ui', self)


    def create_preset(self):
        pass