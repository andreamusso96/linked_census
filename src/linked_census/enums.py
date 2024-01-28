from typing import Set

from enum import Enum

from . import data


class CensusYear(Enum):
    y1850 = 1850
    y1860 = 1860
    y1870 = 1870
    y1880 = 1880
    y1900 = 1900
    y1910 = 1910
    y1920 = 1920
    y1930 = 1930
    y1940 = 1940

    @staticmethod
    def get_next_census_year(census_year: 'CensusYear') -> 'CensusYear':
        if census_year != CensusYear.y1940 and census_year != CensusYear.y1880:
            return CensusYear(census_year.value + 10)
        elif census_year == CensusYear.y1880:
            return CensusYear.y1900
        else:
            raise ValueError(f'The census year {census_year.value} has no next census year')

    @staticmethod
    def from_int(census_year: int) -> 'CensusYear':
        census_year_enum = [census_year_enum for census_year_enum in CensusYear if census_year_enum.value == census_year][0]
        return census_year_enum


class Industry(Enum):
    @staticmethod
    def get_map_industry_code_to_aggregation_level(aggregation_level: int) -> dict:
        assert 0 <= aggregation_level <= 3, 'Aggregation level must be between 0 and 3'
        industry_codes_with_aggregation = data.data.industry_codes[['IND1950_CODE', f'IND1950_DESC_AGG{aggregation_level}']]
        map_industry_codes_to_aggregation = industry_codes_with_aggregation.set_index('IND1950_CODE')[f'IND1950_DESC_AGG{aggregation_level}'].to_dict()
        return map_industry_codes_to_aggregation


class PlaceClusterLevel(Enum):
    l5 = 5
    l10 = 10
    l50 = 50
    l100 = 100
    l200 = 200
    l300 = 300
    l500 = 500







