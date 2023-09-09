from typing import List

import pandas as pd

from . import config
from . import enums


def load(census_year: enums.CensusYear) -> pd.DataFrame:
    next_census_year = enums.CensusYear.get_next_census_year(census_year=census_year)
    census_data = load_census_data(census_year=census_year)
    census_data.set_index(['YEAR', 'HIK'], inplace=True)
    geo_data = load_geo_data(years=[census_year, next_census_year])
    geo_data.set_index(['YEAR', 'HIK'], inplace=True)
    data = census_data.merge(geo_data, how='left', left_index=True, right_index=True)
    return data


def load_census_data(census_year: enums.CensusYear) -> pd.DataFrame:
    data = pd.read_csv(config.census_data_file(census_year=census_year), compression='gzip', dtype={'YEAR': int, 'CITY': int, 'HIK': str})
    return data


def load_geo_data(years: List[enums.CensusYear]) -> pd.DataFrame:
    data = []

    for year in years:
        data_year = pd.read_csv(config.geo_data_file(census_year=year), compression='zip', dtype={'histid': str, 'clusterid_k5': int})
        data_year['YEAR'] = year.value
        data_year.rename(columns={'histid': 'HIK'}, inplace=True)
        data.append(data_year)

    data = pd.concat(data, axis=0)
    return data