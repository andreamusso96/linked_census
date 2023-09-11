import pandas as pd

from .data import data
from . import enums
from . import utils


def get_intercity_migrations(census_year: enums.CensusYear, cluster_level: enums.PlaceClusterLevel = enums.PlaceClusterLevel.l5) -> pd.DataFrame:
    utils.logger.debug(f'get_intercity_migrations: called with census_year={census_year.value}, cluster_level={cluster_level.value}')
    next_census_year = enums.CensusYear.get_next_census_year(census_year=census_year)

    utils.logger.debug(f'get_intercity_migrations: loading data from year {census_year.value} and year {next_census_year.value}')
    data_year_1 = data.data(census_year=census_year)
    data_year_2 = data.data(census_year=next_census_year)

    utils.logger.debug(f'get_intercity_migrations: merging data from year {census_year.value} with data from year {next_census_year.value}')
    df = data_year_1.merge(data_year_2, how='left', left_on='HIK', right_on='HIK', suffixes=('_1', '_2'))[['HIK', 'clusterid_k5_1', 'clusterid_k5_2', 'IND1950_1']]
    df.set_index('HIK', inplace=True)
    df.rename(columns={'clusterid_k5_1': census_year.value, 'clusterid_k5_2': next_census_year.value}, inplace=True)
    df.dropna(inplace=True)

    utils.logger.debug(f'get_intercity_migrations: selecting census place clusters at level {cluster_level.value}')
    df = _map_clusterid5_to_clusterid_level(df=df, cluster_level=cluster_level)

    utils.logger.debug(f'get_intercity_migrations: aggregating migrations from city to city across years')
    df['count'] = 1
    migrations_from_city_to_city_across_years = df.groupby(by=[census_year.value, next_census_year.value]).agg({'count': 'sum'})
    migrations_from_city_to_city_across_years.reset_index(inplace=True)
    migration_matrix__city_by_city = migrations_from_city_to_city_across_years.pivot(index=census_year.value, columns=next_census_year.value, values='count')
    migration_matrix__city_by_city.fillna(value=0, inplace=True)

    utils.logger.debug(f'get_intercity_migrations: done')
    return migration_matrix__city_by_city


def _map_clusterid5_to_clusterid_level(df: pd.DataFrame, cluster_level: enums.PlaceClusterLevel) -> pd.DataFrame:
    if cluster_level == enums.PlaceClusterLevel.l5:
        return df
    else:
        cluster5_to_cluster_map = data.place_data[['consistent_place_5', f'consistent_place_{cluster_level.value}']].drop_duplicates().set_index('consistent_place_5')[f'consistent_place_{cluster_level.value}'].to_dict()
        df = df.applymap(lambda x: cluster5_to_cluster_map[int(x)])
        return df


def get_city_population(census_year: enums.CensusYear, cluster_level: enums.PlaceClusterLevel) -> pd.DataFrame:
    utils.logger.debug(f'get_city_population: called with census_year={census_year.value}, cluster_level={cluster_level.value}')

    utils.logger.debug(f'get_city_population: loading data from year {census_year.value}')
    df = data.data(census_year=census_year)[['clusterid_k5']].copy()

    utils.logger.debug(f'get_city_population: selecting census place clusters at level {cluster_level.value}')
    df = _map_clusterid5_to_clusterid_level(df=df, cluster_level=cluster_level)
    df.rename(columns={'clusterid_k5': f'clusterid_k{cluster_level.value}'}, inplace=True)

    utils.logger.debug(f'get_city_population: aggregating population across cities')
    df['count'] = 1
    city_population = df.groupby(by=[f'clusterid_k{cluster_level.value}']).agg({'count': 'sum'})
    city_population.rename(columns={'count': 'population'}, inplace=True)

    utils.logger.debug(f'get_city_population: done')
    return city_population
