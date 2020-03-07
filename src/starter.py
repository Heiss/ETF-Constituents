import sys

from ui.main import Ui_MainWindow
from ui.settingsDialog import Ui_Dialog
from ui.etfWidget import Ui_Form
from util.loader import load_institution
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PySide2.QtCore import Slot


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.actionSettings.triggered.connect(self.showDialog)
        self.actionExit.triggered.connect(sys.exit)
        self.show()

    @Slot()
    def loader(self):
        indices = open("config.txt", newline="").readlines()
        for inst in load_institution(indices):
            print(inst)

    def showDialog(self):
        settingsDialog()

class etfWidget(QWidget, Ui_Form):
    def __init__(self):
        super(etfWidget, self).__init__()
        self.setupUi(self)
        

class settingsDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(settingsDialog, self).__init__()
        self.setupUi(self)

        # TODO add here an additional tab to Dialog per institution
        """with open("src/institutions/data/msci_id.full.data", newline="\n") as file:
            for indices in file.readlines():
                item = QListWidgetItem(str(indices).strip())
                self.listWidget.addItem(item)"""
        from institutions.msci import MSCI
        
        etf = etfWidget()
        msci = MSCI(autoLoad=False)
        msci.addIndexFondsToWidget(etf.listWidget)

        self.tabWidget.addTab(etf, "MSCI")
        self.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
