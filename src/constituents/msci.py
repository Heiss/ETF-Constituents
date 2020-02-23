from constituents.abstract_institution import Institution, Constituent, IndexFond
import logging

logger = logging.getLogger()


class MSCI(Institution):
    def __init__(self, listOfSearchedIndex=None):
        super().__init__(listOfSearchedIndex=listOfSearchedIndex)

    def load_indexfonds(self, listOfSearchedIndex):

        import csv
        l = []

        with open("src/constituents/data/msci_id.full.data", newline="") as f:
            reader = csv.DictReader(f)

            l = [MSCIIndex(con["name"], con["id"])
                 for con in reader if con["name"] in listOfSearchedIndex]
        # you may also want to remove whitespace characters like `\n` at the end of each line
        return l


class MSCIIndex(IndexFond):
    url = "https://www.msci.com/c/portal/layout?p_l_id=1317535&p_p_cacheability=cacheLevelPage&p_p_id=indexconstituents_WAR_indexconstituents_INSTANCE_nXWh5mC97ig8&p_p_lifecycle=2&p_p_resource_id={}"

    def __init__(self, name, id=None):
        super().__init__(name, id=id)

    def load_constituents(self):
        import requests

        resp = requests.get(self.url.format(self.identifier)).json()
        l = []

        try:
            for con in resp["constituents"]:
                l.append(Constituent(
                    con["security_name"], float(con["security_weight"])))
        except Exception as e:
            logger.exception(e)

        return l
