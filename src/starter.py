import sys

from ui.main import Ui_MainWindow
from util.loader import load_institution
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Slot


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()

    @Slot()
    def loader(self):
        indices = open("config.txt", newline="").readlines()
        for inst in load_institution(indices):
            print(inst)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
