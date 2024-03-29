import pandas as pd

from . import config, preprocessing


class Data:
    def __init__(self):
        self._data = None
        self._census_year = None
        self._industry_codes = None
        self._place_data = None

    def data(self, census_year) -> pd.DataFrame:
        if self._data is None or census_year != self._census_year:
            self._data = preprocessing.load_data(census_year=census_year)
            self._census_year = census_year
        return self._data.copy()

    @property
    def place_data(self):
        if self._place_data is None:
            self._place_data = pd.read_csv(config.place_data_file())
        return self._place_data.copy()

    @property
    def industry_codes(self) -> pd.DataFrame:
        if self._industry_codes is None:
            self._industry_codes = pd.read_csv(config.industry_codes_file(), dtype={'IND1950_CODE': int})
        return self._industry_codes.copy()


data = Data()
