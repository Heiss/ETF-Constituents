import sys

from ui.main import Ui_MainWindow
from ui.settingsDialog import Ui_Dialog
from ui.etfWidget import Ui_Form
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QTableWidgetItem
from qt.QTableWidgetNumberItem import QTableWidgetNumberItem
import logging
import threading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def threadLoading(mainWindow):
    # fork the loading function to not block the mainWindow
    thread = threading.Thread(target=loader, args=(mainWindow,))
    logger.debug("Start loading thread")
    thread.start()


def loader(mainWindow):
    institutions = []
    from util.loader import load_institution

    # progressbar for loading
    mainWindow.progressBar.setValue(0)
    with open("config.txt", newline="\n") as file:
        indices = [line.strip() for line in file.readlines()]
        for inst in load_institution(indices, progressBar=mainWindow.progressBar):
            logger.debug("loaded institution: {}".format(inst))

            institutions.append(inst)

    shares = {}
    for institution in institutions:
        for fond in institution.indexFonds:
            for constituent in fond.constituents:
                try:
                    shares[constituent.name] += constituent.weight
                except:
                    shares[constituent.name] = constituent.weight

    # TODO: add shares to tables with column 0: Name and column 1: Weight
    table = mainWindow.tableWidget
    logger.debug("clear table")

    table.clearContents()
    table.setRowCount(0)
    index = 0

    for name, weight in shares.items():
        logger.debug("add item {} with weight {} to table".format(name, weight))
        numRows = index

        itemName = QTableWidgetItem(name)
        itemWeight = QTableWidgetNumberItem(weight)

        table.insertRow(numRows)
        table.setItem(numRows, 0, itemName)
        table.setItem(numRows, 1, itemWeight)
        
        index += 1


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.actionReload.triggered.connect(lambda: threadLoading(self))
        self.actionSettings.triggered.connect(self.showDialog)
        self.actionExit.triggered.connect(sys.exit)

        threadLoading(self)

        self.show()

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
