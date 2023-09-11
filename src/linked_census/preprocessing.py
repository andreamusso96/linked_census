import pandas as pd
import numpy as np

from . import config, enums, utils


def load_data(census_year: enums.CensusYear) -> pd.DataFrame:
    utils.logger.debug(f'Loading data for {census_year.value}')
    utils.logger.debug('Loading census data')
    census_data = load_census_data(census_year=census_year)
    utils.logger.debug('Loading geo data')
    geo_data = load_geo_data(year=census_year)
    utils.logger.debug('Merging census and geo data')
    merged_data = census_data.merge(geo_data, how='inner', on='HISTID')
    merged_data.dropna(subset=['clusterid_k5'], inplace=True)
    merged_data['clusterid_k5'] = merged_data['clusterid_k5'].astype(int)
    utils.logger.debug('Done loading data')
    return merged_data


def load_census_data(census_year: enums.CensusYear) -> pd.DataFrame:
    data = pd.read_csv(config.census_data_file(census_year=census_year), compression='gzip', dtype={'YEAR': int, 'HISTID': str, 'HIK': str, 'IND1950': int, 'OCC1950': int}, usecols=['YEAR', 'HISTID', 'HIK', 'IND1950', 'OCC1950'])
    data.drop_duplicates(subset=['HISTID'], inplace=True)
    data['HIK'] = data['HIK'].replace(' ' * 21, np.nan)
    return data


def load_geo_data(year: enums.CensusYear) -> pd.DataFrame:
    geo_data = pd.read_csv(config.geo_data_file(census_year=year), compression='gzip', dtype={'histid': str}, low_memory=False, usecols=['clusterid_k5', 'histid'])
    geo_data.rename(columns={'histid': 'HISTID'}, inplace=True)
    geo_data.drop_duplicates(subset=['HISTID'], inplace=True)
    geo_data['HISTID'] = geo_data['HISTID'].apply(lambda x: x.upper())
    return geo_data