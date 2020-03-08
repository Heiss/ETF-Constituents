from abc import ABC, abstractmethod
import logging

logger = logging.getLogger()


class Constituent(ABC):
    def __init__(self, name, weight):
        super().__init__()

        self.name = name
        self.weight = weight

    def __eq__(self, obj):
        if isinstance(obj, self.__class__) and obj.name == self.name:
            return True

        return False

    def __repr__(self):
        return f"Constituent: {self.name} ({self.weight})"

    def __str__(self):
        return self.name


class IndexFond(ABC):
    def __init__(self, name, id=None, autoLoad=True):
        """
        Set id, if you need something to identifier this fond against the index provider.
        """
        super().__init__()

        if id is not None:
            self.identifier = id

        self.name = name
        self.constituents = self.load_constituents(autoLoad=autoLoad)

    @abstractmethod
    def load_constituents(self, autoLoad=True):
        pass

    def getConstituents(self):
        return self.constituents

    def addConstituents(self, constituent: Constituent):
        self.constituents.append(constituent)

    def __repr__(self):
        res = f"---- Fond: {self.name} ----\n"

        for con in self.constituents:
            res += f"{con.name} ({con.weight})\n"

        return res

    def __str__(self):
        return self.name


class Institution(ABC):
    def __init__(self, listOfSearchedIndex=None, autoLoad=True):
        super().__init__()

        # if listOfSearchedIndex is empty, it should load all indexFonds
        if listOfSearchedIndex is None:
            listOfSearchedIndex = []

        # for easier usage
        if isinstance(listOfSearchedIndex, str):
            listOfSearchedIndex = [listOfSearchedIndex]

        if not isinstance(listOfSearchedIndex, list):
            raise ValueError("No list given.")

        self.indexFonds = self.load_indexfonds(
            listOfSearchedIndex, autoLoad=autoLoad)

    @abstractmethod
    def load_indexfonds(self, listOfSearchedIndex: list, autoLoad=True):
        """
        The given list will be searched for constituents.
        It has to return a list with IndexFond as Objects. 
        """
        raise NotImplemented()

    def addIndexFondsToWidget(self, qListWidget, selectIndeces: list = None):
        """
        The indexFonds of this institution will be transformed into a QListWidgetItem and added to the given QListWidget.
        Through the given selectIndeces list, you can specify, whic QListWidgetItem should be selected.

        The given list has to be this struct:
        [str, str, str]
        """
        from PySide2.QtWidgets import QListWidgetItem

        if selectIndeces is None:
            selectIndeces = []

        for fond in self.indexFonds:
            item = QListWidgetItem(fond.name)

            qListWidget.addItem(item)

            searchName = "{} {}".format(self.__class__.__name__, fond.name)
            item.setSelected(searchName in selectIndeces)

    def __repr__(self):
        strRet = ""
        strRet += f"---- Provider: {self.__class__.__name__} ----\n"
        for index in self.indexFonds:
            strRet += str(index)

        return strRet
