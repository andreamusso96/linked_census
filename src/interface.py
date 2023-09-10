from typing import Union, List

import pandas as pd

from .data import data
from . import enums


def get_intercity_migrations(census_year: enums.CensusYear, industry: enums.Industry = enums.Industry.ALL, cluster_level: enums.PlaceClusterLevel = enums.PlaceClusterLevel.l5) -> pd.DataFrame:
    df = data.data(census_year=census_year)
    years = sorted(list(df['YEAR'].unique()))
    from_year, to_year = years[0], years[1]

    individual_ids = _get_ids_of_individuals_within_industry_in_year(df=df, industry=industry, year=from_year)
    census_individuals_within_industry_in_initial_year = df.loc[df['HIK'].isin(individual_ids)].copy()
    city__person_by_year = census_individuals_within_industry_in_initial_year.pivot(index='HIK', columns='YEAR', values='clusterid_k5')
    city__person_by_year = _map_clusterid5_to_clusterid_level(df=city__person_by_year, cluster_level=cluster_level)
    city__person_by_year = city__person_by_year[[from_year, to_year]]
    city__person_by_year.dropna(inplace=True)
    city__person_by_year['count'] = 1

    migrations_from_city_to_city_across_years = city__person_by_year.groupby(by=[from_year, to_year]).agg({'count': 'sum'})
    migrations_from_city_to_city_across_years.reset_index(inplace=True)
    migration_matrix__city_by_city = migrations_from_city_to_city_across_years.pivot(index=from_year, columns=to_year, values='count')
    migration_matrix__city_by_city.fillna(value=0, inplace=True)

    return migration_matrix__city_by_city


def _get_ids_of_individuals_within_industry_in_year(df: pd.DataFrame, industry: enums.Industry, year: int) -> pd.DataFrame:
    data_industry_and_year = df.loc[(df['YEAR'] == year) & (df['IND1950'].isin(enums.Industry.get_codes(industry=industry)))]
    individual_ids = data_industry_and_year['HIK'].values
    return individual_ids


def _map_clusterid5_to_clusterid_level(df: pd.DataFrame, cluster_level: enums.PlaceClusterLevel) -> pd.DataFrame:
    cluster5_to_cluster_map = data.place_data[['consistent_place_5', f'consistent_place_{cluster_level.value}']].drop_duplicates().set_index('consistent_place_5')[f'consistent_place_{cluster_level.value}'].to_dict()
    df = df.applymap(lambda x: cluster5_to_cluster_map[x])
    return df



def get_city_population(census_year: enums.CensusYear) -> pd.DataFrame:
    geo_df = data.geo_data(census_year=census_year)
    geo_df['count'] = 1
    city_population = geo_df.groupby(by=['clusterid_k5']).agg({'count': 'sum'})
    return city_population

## OLD CODE BELOW

def _get_census_individuals_within_industry(industry: enums.Industry) -> pd.DataFrame:
    codes = enums.Industry.get_codes(industry=industry)
    filtered_data = data.data.loc[data.data['IND1950'].isin(codes)].copy()
    return filtered_data


def get_share_of_agricultural_workers_by_city(year: Union[int, List[int]] = None) -> pd.DataFrame:
    assert data.data is not None, 'Data has not been loaded'
    year_ = year if year is not None else list(data.data['YEAR'].unique())

    if isinstance(year_, int):
        year_ = [year]
    else:
        year_ = year

    census_agriculture = _get_census_individuals_within_industry(industry=enums.Industry.AGRICULTURE)
    agriculture_workers_by_city = census_agriculture.groupby(by=['YEAR', 'CITY']).agg({'HIK': 'count'}).rename(columns={'HIK': 'AGR'})

    census_non_agriculture = _get_census_individuals_within_industry(industry=enums.Industry.NON_AGRICULTURE)
    non_agriculture_workers_by_city = census_non_agriculture.groupby(by=['YEAR', 'CITY']).agg({'HIK': 'count'}).rename(columns={'HIK': 'NON_AGR'})

    number_of_agr_and_non_agr_workers_by_city = pd.merge(agriculture_workers_by_city, non_agriculture_workers_by_city, left_index=True, right_index=True, how='outer')
    number_of_agr_and_non_agr_workers_by_city.fillna(value=0, inplace=True)
    number_of_agr_and_non_agr_workers_by_city['AGR_SHARE'] = number_of_agr_and_non_agr_workers_by_city['AGR'] / (number_of_agr_and_non_agr_workers_by_city['AGR'] + number_of_agr_and_non_agr_workers_by_city['NON_AGR'])
    number_of_agr_and_non_agr_workers_by_city_selected_year = number_of_agr_and_non_agr_workers_by_city.loc[(year_, slice(None))]
    return number_of_agr_and_non_agr_workers_by_city_selected_year


def get_city_name(city_code: Union[str, List[str]]) -> pd.DataFrame:
    if isinstance(city_code, str):
        city_code_ = [city_code]
    else:
        city_code_ = city_code
    return data.city_codes_and_names.set_index('CITY').loc[city_code_]



