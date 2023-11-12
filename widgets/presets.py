from PyQt5 import uic

from PyQt5.QtWidgets import QWidget


class PresetsTable(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../static/presets.ui', self)
        
