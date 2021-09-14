from PySide2.QtWidgets import QTableWidgetItem


class QTableWidgetNumberItem(QTableWidgetItem):
    def __init__(self, number, name):
        super(QTableWidgetNumberItem, self).__init__(str(number))
        self.__number = number
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __lt__(self, other):
        return self.__number < other.__number
