import os
from . import enums

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = f'{base_dir}/data'


def census_data_file(census_year: enums.CensusYear) -> str:
    next_census_year = enums.CensusYear.get_next_census_year(census_year=census_year)
    return f'{data_dir}/usa_{census_year.value}-{next_census_year.value}.csv.gz'


def geo_data_file(census_year: enums.CensusYear) -> str:
    return f'{data_dir}/Geo/{census_year.value}_csv.zip'







