from importlib import import_module

import logging
import math
logger = logging.getLogger()


def load_institution(listOfIndices, progressBar):
    """
    This method reads in the indices and try to find and load the implementation of the corresponding index provider.
    It returns a list with the initialized institutions.
    """
    institutions = []
    progressBar.setValue(0)
    valPerIndex = math.ceil(progressBar.maximum() / len(listOfIndices))

    for index in listOfIndices:
        part = str(index).split(" ", 1)

        try:
            # import given institution
            institution = import_module(
                f"institutions.{str(part[0]).lower()}").__getattribute__(str(part[0]).upper())

            # initialize it
            institutions.append(institution(part[1]))
        except Exception as e:
            logger.exception(e)

        val = progressBar.value() + valPerIndex
        progressBar.setValue(val if val < 100 else 100)

    return institutions
