import pandas as pd

from . import config, enums, utils


def load(census_year: enums.CensusYear) -> pd.DataFrame:
    utils.logger.info(f'Loading data for year {census_year.value}')
    utils.logger.debug(f'Loading IPUMS data year {census_year.value}')

    census_data = load_census_data(census_year=census_year)
    geo_data = _load_geo_data_only_for_census_data_hist_ids(census_data=census_data, census_year=census_year)

    utils.logger.debug(f'Merging census and geo data for year {census_year.value}')

    geo_data.set_index(['YEAR', 'HISTID'], inplace=True)
    census_data.set_index(['YEAR', 'HISTID'], inplace=True)
    data = census_data.merge(geo_data, how='left', left_index=True, right_index=True)
    data.reset_index(inplace=True)

    utils.logger.info(f'Loaded data for year {census_year.value}')
    return data


def _load_geo_data_only_for_census_data_hist_ids(census_data: pd.DataFrame, census_year: enums.CensusYear) -> pd.DataFrame:
    utils.logger.debug(f'Loading geo_data')

    next_census_year = enums.CensusYear.get_next_census_year(census_year=census_year)
    geo_data = []
    for year in [census_year, next_census_year]:
        utils.logger.debug(f'Loading geo data for year {year.value}')
        ipums_hist_id_year = census_data.loc[census_data['YEAR'] == year.value, 'HISTID'].values.flatten()
        geo_data_year = load_geo_data(year=year)
        geo_data_year = geo_data_year.loc[geo_data_year['HISTID'].isin(ipums_hist_id_year)]
        geo_data.append(geo_data_year)

    geo_data = pd.concat(geo_data, axis=0)

    utils.logger.debug(f'Loaded geo_data')
    return geo_data


def load_census_data(census_year: enums.CensusYear) -> pd.DataFrame:
    data = pd.read_csv(config.census_data_file(census_year=census_year), compression='gzip', dtype={'YEAR': int, 'HISTID': str}, usecols=['YEAR', 'HISTID', 'HIK', 'IND1950'])
    return data


def load_geo_data(year: enums.CensusYear) -> pd.DataFrame:
    geo_data = pd.read_csv(config.geo_data_file(census_year=year), compression='gzip', dtype={'histid': str}, low_memory=False, usecols=['clusterid_k5', 'histid'])
    geo_data['YEAR'] = year.value
    geo_data.rename(columns={'histid': 'HISTID'}, inplace=True)
    return geo_data