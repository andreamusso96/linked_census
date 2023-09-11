import os
from . import enums

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_dir = f'{base_dir}/data'


def census_data_file(census_year: enums.CensusYear) -> str:
    return f'{data_dir}/census/usa_{census_year.value}.csv.gz'


def geo_data_file(census_year: enums.CensusYear) -> str:
    return f'{data_dir}/geo/histid_place_crosswalk_{census_year.value}.csv.gz'


def industry_codes_file() -> str:
    return f'{data_dir}/industry_base1950_codes.csv'


def place_data_file() -> str:
    return f'{data_dir}/geo/place_component_crosswalk.csv'







