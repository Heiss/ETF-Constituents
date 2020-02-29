from abc import ABC, abstractmethod


class Constituent(ABC):
    def __init__(self, name, weight):
        super().__init__()

        self.name = name
        self.weight = weight

    def __str__(self):
        return f"Constituent: {self.name} ({self.weight})"


class IndexFond(ABC):
    def __init__(self, name, id=None):
        """
        Set id, if you need something to identifier this fond against the index provider.
        """
        super().__init__()

        if id is not None:
            self.identifier = id

        self.name = name
        self.constituents = self.load_constituents()

    @abstractmethod
    def load_constituents(self):
        pass

    def getConstituents(self):
        return self.constituents

    def addConstituents(self, constituent: Constituent):
        self.constituents.append(constituent)

    def __str__(self):
        res = f"---- Fond: {self.name} ----\n"

        for con in self.constituents:
            res += f"{con.name} ({con.weight})\n"

        return res


class Institution(ABC):
    def __init__(self, listOfSearchedIndex=None):
        super().__init__()

        if listOfSearchedIndex is None:
            listOfSearchedIndex = []
        
        # for easier usage
        if isinstance(listOfSearchedIndex, str):
            listOfSearchedIndex = [listOfSearchedIndex]

        if not isinstance(listOfSearchedIndex, list):
            raise ValueError("No list given.")

        self.indexFonds = self.load_indexfonds(listOfSearchedIndex)

    @abstractmethod
    def load_indexfonds(self, listOfSearchedIndex: list):
        """
        The given list will be searched for constituents.
        It has to return a list with IndexFond as Objects. 
        """
        return []

    def __str__(self):
        strRet = ""
        strRet += f"---- Provider: {self.__class__.__name__} ----\n"
        for index in self.indexFonds:
            strRet += str(index)

        return strRet
