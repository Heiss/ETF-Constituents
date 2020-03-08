import sys

from ui.main import Ui_MainWindow
from ui.settingsDialog import Ui_Dialog
from ui.etfWidget import Ui_Form
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PySide2.QtCore import SIGNAL
import logging
import threading
from qt.LoaderThread import LoaderThread, ProgressBarUpdate
from qt.QTableWidgetNumberItem import QTableWidgetNumberItem


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.communicator = ProgressBarUpdate(self.progressBar)
        self.loadingThread = LoaderThread(
            self, self.progressBar.maximum(), self.communicator)

        self.actionReload.triggered.connect(lambda: self.loadingThread.start())
        self.actionSettings.triggered.connect(self.showDialog)
        self.actionExit.triggered.connect(sys.exit)

        self.communicator.value.connect(self.set_progressbar)
        self.communicator.format.connect(self.set_progressbar_format)

        self.tableWidget.itemSelectionChanged.connect(self.setStatusLabel)

        self.show()
        self.loadingThread.start()

    def setStatusLabel(self):
        items = self.tableWidget.selectedItems()

        sum = 0
        for item in items:
            if isinstance(item, QTableWidgetNumberItem):
                sum += float(item.text())

        self.label.setText("Selected value of weight: {}".format(sum))

    def set_progressbar(self, val):
        try:
            val = int(val)
            self.progressBar.setValue(val if val < 100 else 100)
        except:
            pass

    def set_progressbar_format(self, val):
        self.progressBar.setFormat(val)

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

        # add here an additional tab to Dialog per institution
        self.tabs = []
        self.createTabs(self.tabWidget)

        self.buttonBox.accepted.connect(self.saveConfig)

        logger.debug("open settingsDialog")
        self.exec()

    def createTabs(self, tabWidget):
        selectedList = []
        with open("config.txt", newline="") as file:
            selectedList = [line.strip() for line in file.readlines()]

        from institutions.msci import MSCI

        etf = etfWidget()
        msci = MSCI(autoLoad=False)

        msci.addIndexFondsToWidget(etf.listWidget, selectIndeces=selectedList)

        tabWidget.addTab(etf, "MSCI")

    def saveConfig(self):
        # save the selected items in config here
        logger.debug("Start saveConfig")
        for index in range(1, self.tabWidget.count()):
            tabName = self.tabWidget.tabText(index)
            widget = self.tabWidget.widget(index)

            items = widget.listWidget.selectedItems()

            selectedFonds = ["{} {}\n".format(
                tabName, item.text()) for item in items]
            logger.debug(selectedFonds)

            with open("config.txt", "w") as file:
                file.writelines(selectedFonds)
                logger.debug("Write lines in config.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
