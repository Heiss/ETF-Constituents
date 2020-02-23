from abc import ABC


class Constituent(ABC):
    def __init__(self, name, weight):
        super().__init__()

        self.name = name
        self.weight = weight


class Institution(ABC):
    def __init__(self):
        super().__init__()

        self.constituents = []

    def getConstituents(self):
        return self.constituents

    def addConstituents(self, constituent: Constituent):
        self.constituents.append(constituent)

    def __str__(self):
        res = f"---- {self.__class__.__name__} ----\n"

        for con in self.constituents:
            res += f"{con.name} ({con.weight})\n"

        return res
