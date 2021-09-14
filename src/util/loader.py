from importlib import import_module

import logging
import math
logger = logging.getLogger()


def load_institution(listOfIndices):
    """
    This method reads in the indices and tries to find and load the implementation of the corresponding index provider.
    It returns a list with the initialized institutions.
    """
    institutions = []

    for index in listOfIndices:
        part = str(index).split(" ", 1)

        try:
            # import given institution
            institution = import_module(
                f"institutions").__getattribute__(str(part[0]))

            # initialize it
            institutions.append(institution(part[1]))
        except Exception as e:
            logger.exception(e)

    return institutions
