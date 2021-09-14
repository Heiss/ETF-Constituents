from institutions.abstract_institution import Institution, Constituent, IndexFond
import logging
import requests

logger = logging.getLogger()


class MSCIIndex(IndexFond):
    URL = "https://www.msci.com/c/portal/layout?p_l_id=1317535&p_p_cacheability=cacheLevelPage&p_p_id=indexconstituents_WAR_indexconstituents_INSTANCE_nXWh5mC97ig8&p_p_lifecycle=2&p_p_resource_id={}"

    def __init__(self, name, id=None, autoLoad=True):
        super().__init__(name, id=id, autoLoad=autoLoad)

    def load_constituents(self, autoLoad=True):
        l = []
        if autoLoad:
            resp = requests.get(self.URL.format(self.identifier)).json()

            try:
                for con in resp["constituents"]:
                    l.append(Constituent(
                        con["security_name"], float(con["security_weight"])))
            except Exception as e:
                logger.exception(e)

        return l


class MSCI(Institution):
    URL = "https://www.msci.com/c/portal/layout?p_l_id=1317535&p_p_cacheability=cacheLevelPage&p_p_id=indexconstituents_WAR_indexconstituents_INSTANCE_nXWh5mC97ig8&p_p_lifecycle=2"

    def __init__(self, listOfSearchedIndex=None, autoLoad=True):
        super().__init__(listOfSearchedIndex=listOfSearchedIndex, autoLoad=autoLoad)

    def load_indexfonds(self, listOfSearchedIndex, autoLoad=True):
        logger.debug("Load fonds from list: {}".format(listOfSearchedIndex))
        l = []

        rq = requests.get(self.URL)
        reader = rq.json()["indices"]

        if len(listOfSearchedIndex) == 0:
            l = [MSCIIndex(con["index_name"], con["index_code"], autoLoad=autoLoad)
                 for con in reader]
        else:
            l = [MSCIIndex(con["index_name"], con["index_code"], autoLoad=autoLoad)
                 for con in reader if con["index_name"] in listOfSearchedIndex]

        # you may also want to remove whitespace characters like `\n` at the end of each line
        logger.debug("found indexfonds: {}".format(l))

        return l
