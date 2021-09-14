from PySide2.QtCore import QThread, SIGNAL
from PySide2.QtWidgets import QTableWidgetItem
from qt.QTableWidgetNumberItem import QTableWidgetNumberItem
from PySide2.QtCore import QObject, Signal

import logging

logger = logging.getLogger()


class ProgressBarUpdate(QObject):
    value = Signal(float)
    format = Signal(str)

    def __init__(self, progressBar):
        super(ProgressBarUpdate, self).__init__()

        self.progressBar = progressBar

        self.value.connect(self.updateValue)
        self.format.connect(self.updateFormat)

    def updateValue(self, value):
        self.progressBar.setValue(value if value < 100 else 100)

    def updateFormat(self, format):
        self.progressBar.setFormat(format)


class LoaderThread(QThread):
    def __init__(self, mainWindow, maximum, communicator):
        QThread.__init__(self)
        self.mainWindow = mainWindow
        self.maximum = maximum
        self.communicator = communicator

    def __del__(self):
        self.wait()

    def run(self):
        self.loader()

    def loader(self):
        mainWindow = self.mainWindow

        institutions = []
        from util.loader import load_institution

        logger.debug("Start downloading")

        val = 0
        self.communicator.format.emit("Downloading: %p%")
        self.communicator.value.emit(val)

        with open("config.txt", newline="\n") as file:
            indices = [line.strip() for line in file.readlines()]
            logger.debug(indices)

            valPerRun = self.maximum / len(indices)
            for inst in load_institution(indices):
                logger.debug("loaded institution: {}".format(inst))

                institutions.append(inst)
                val += valPerRun
    
                self.communicator.value.emit(val)


        shares = {}
        sharesCount = 0

        logger.debug("Start calculating")

        val = 0
        self.communicator.format.emit("Calculating: %p%")
        self.communicator.value.emit(val)

        valPerRun = self.maximum / len(institutions)

        index = 0

        for institution in institutions:
            for fond in institution.indexFonds:
                for constituent in fond.constituents:
                    try:
                        shares[constituent.name] += constituent.weight
                    except:
                        shares[constituent.name] = constituent.weight
                    sharesCount += constituent.weight
            index += 1

            val += valPerRun
            self.communicator.value.emit(val)

        # add shares to tables with column 0: Name and column 1: Weight
        table = mainWindow.tableWidget
        logger.debug("clear table")

        table.clearContents()
        table.setRowCount(0)
        index = 0

        logger.debug("Start adding")

        val = 0
        self.communicator.format.emit("Adding to table: %p%")
        self.communicator.value.emit(val)

        valPerRun = self.maximum / len(shares.items())

        for name, weight in shares.items():
            numRows = index

            itemName = QTableWidgetItem(name)
            itemWeight = QTableWidgetNumberItem(weight / sharesCount * 100, "weight")
            itemShares = QTableWidgetNumberItem(weight, "share")

            table.insertRow(numRows)
            table.setItem(numRows, 0, itemName)
            table.setItem(numRows, 1, itemWeight)
            table.setItem(numRows, 2, itemShares)

            index += 1

            val += valPerRun
            self.communicator.value.emit(val)

        logger.debug("Done")

        self.communicator.value.emit(100)
        self.communicator.format.emit("Done")
