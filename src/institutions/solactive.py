from institutions.abstract_institution import Institution, Constituent, IndexFond
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


class SolactiveIndex(IndexFond):
    URL = "https://www.solactive.com/indices/?index={}"

    def __init__(self, name, id=None, autoLoad=True):
        super().__init__(name, id=id, autoLoad=autoLoad)

    def load_constituents(self, autoLoad=True):
        l = []
        if autoLoad:
            rq = requests.get(self.URL.format(self.identifier)).json()
            soup = BeautifulSoup(rq.text)
            table = soup.find('table', attrs={
                'class': 'members table table-hover datatable dataTable no-footer'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')

            try:
                for row in rows:
                    l.append(Constituent(
                        row[0].text.strip(), float(row[1].text.strip())))
            except Exception as e:
                logger.exception(e)

        return l


class Solactive(Institution):
    URL = "https://www.solactive.com/indices/"

    def __init__(self, listOfSearchedIndex=None, autoLoad=True):
        super().__init__(listOfSearchedIndex=listOfSearchedIndex, autoLoad=autoLoad)

    def load_indexfonds(self, listOfSearchedIndex, autoLoad=True):
        logger.debug("Load fonds from list: {}".format(listOfSearchedIndex))
        import csv
        l = []

        rq = requests.get(self.URL)
        soup = BeautifulSoup(rq.text)

        table = soup.find('table', attrs={
                          'class': 'groups table table-hover datatable-indices dataTable no-footer'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        l = []
        for row in rows:
            data = row.find_all('td')
            if len(listOfSearchedIndex) > 0:
                if data[0].text in listOfSearchedIndex:
                    l.append(SolactiveIndex(
                        data[0].text.strip(), data[1].text.strip(), autoLoad=autoLoad))
            else:
                l.append(SolactiveIndex(
                    data[0].text.strip(), data[1].text.strip(), autoLoad=autoLoad))

        logger.debug("found indexfonds: {}".format(l))

        return l
