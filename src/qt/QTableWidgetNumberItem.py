from PySide2.QtWidgets import QTableWidgetItem


class QTableWidgetNumberItem(QTableWidgetItem):
    def __init__(self, number):
        super(QTableWidgetNumberItem, self).__init__(str(number))
        self.__number = number

    def __lt__(self, other):
        return self.__number < other.__number
