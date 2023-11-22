import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('static/main_window.ui', self)

    def get_slider_values(self):
        """
        Retrieves the values of all sliders in the class instance.

        Returns:
            dict: A dictionary containing the names of the sliders as keys and their corresponding values as values.
        """
        slider_values = {}

        for slider_name in dir(self):
            if slider_name.startswith('slider_'):
                slider = getattr(self, slider_name)
                slider_value = slider.value()
                slider_values[slider_name] = slider_value

        return slider_values


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
