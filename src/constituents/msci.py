from constituents.abstract_institution import Institution, Constituent
import logging

logger = logging.getLogger()


class MSCI(Institution):
    def __init__(self):
        super().__init__()

        self.load_informations()

    def load_informations(self):
        def load_data_file():
            with open("src/constituents/data/msci_id.data") as f:
                content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            return [x.strip() for x in content]

        def load_id_informations(list_of_identifiers, url):
            import requests
            for id in list_of_identifiers:
                resp = requests.get(url.format(id)).json()

                try:
                    for con in resp["constituents"]:
                        self.addConstituents(
                            Constituent(con["security_name"], float(con["security_weight"])))
                except Exception as e:
                    logger.exception(e)

        load_id_informations(load_data_file(
        ), "https://www.msci.com/c/portal/layout?p_l_id=1317535&p_p_cacheability=cacheLevelPage&p_p_id=indexconstituents_WAR_indexconstituents_INSTANCE_nXWh5mC97ig8&p_p_lifecycle=2&p_p_resource_id={}")
