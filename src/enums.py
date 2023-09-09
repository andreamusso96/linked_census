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
    def get_next_census_year(census_year: 'CensusYear'):
        if census_year != CensusYear.y1940 and census_year != CensusYear.y1880:
            return CensusYear(census_year.value + 10)
        elif census_year == CensusYear.y1880:
            return CensusYear.y1900
        else:
            raise ValueError(f'The census year {census_year.value} has no next census year')


class Industry(Enum):
    ALL = 'ALL'
    AGRICULTURE = 'AGR'
    NON_AGRICULTURE = 'NON_AGR'

    @staticmethod
    def get_codes(industry: 'Industry') -> Set[int]:
        assert data.data is not None, 'Data has not been loaded'
        if industry == industry.ALL:
            return set(data.data['IND1950'].unique())
        elif industry == industry.AGRICULTURE:
            return {105, 116, 126, 306, 409, 619}.union({0, 979, 995, 997, 998, 999})
        elif industry == industry.NON_AGRICULTURE:
            return Industry.get_codes(industry=Industry.ALL) - Industry.get_codes(industry=Industry.AGRICULTURE)
        else:
            raise NotImplementedError(f'Industry is not implemented: {industry}')

    @staticmethod
    def from_string(industry: str):
        if industry == Industry.ALL.value:
            return Industry.ALL
        elif industry == Industry.AGRICULTURE.value:
            return Industry.AGRICULTURE
        elif industry == Industry.NON_AGRICULTURE.value:
            return Industry.NON_AGRICULTURE
        else:
            raise NotImplementedError(f'Industry is not implemented: {industry}')




