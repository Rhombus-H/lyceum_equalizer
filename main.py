from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from widgets import sliders, presets


class PyLizer(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyLizer()
    ex.show()
    sys.exit(app.exec_())
