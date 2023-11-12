from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QSlider, QSpinBox, QHBoxLayout


class Sliders(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../static/sliders.ui', self)
