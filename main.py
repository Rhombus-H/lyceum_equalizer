from PyQt5 import uic
import sys

class PyLizer(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.PlayButton.clicked.connect(lambda: print("a"))
        self.StopButton.clicked.connect(lambda: print("s"))
        self.ClearButton.clicked.connect(lambda: print("a"))
        self.SaveButton.clicked.connect(lambda: print("a"))
        self.AcceptButton.clicked.connect(lambda: print("a"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyLizer()
    ex.show()
    sys.exit(app.exec_())
