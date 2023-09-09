from . import preprocessing
from . import enums


class Data:
    def __init__(self):
        self._data = None
        self._census_year = None

    def data(self, census_year: enums.CensusYear):
        if self._data is None or census_year != self._census_year:
            self._data = preprocessing.load(census_year=census_year)
            self._census_year = census_year
        return self._data


data = Data()
