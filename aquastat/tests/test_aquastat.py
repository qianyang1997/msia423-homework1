import pytest
from aquastat.aquastat import time_slice, country_slice, variable_slice, \
    time_series

import pandas as pd
import numpy as np


def create_test_data():
    """create sample data for unit tests.
    """
    df_in_values = [['Indonesia', 'World | Asia', 'total_pop',
                     'Total population (1000 inhab)', '1958-1962', 1962.0, 92558.0],
                    ['Indonesia', 'World | Asia', 'total_pop',
                     'Total population (1000 inhab)', '1963-1967', 1967.0, 105907.0],
                    ['Indonesia', 'World | Asia', 'rural_pop',
                     'Rural population (1000 inhab)', '1958-1962', 1962.0, 78538.0],
                    ['Indonesia', 'World | Asia', 'rural_pop',
                     'Rural population (1000 inhab)', '1963-1967', 1967.0, 88701.0],
                    ['Indonesia', 'World | Asia', 'urban_pop',
                     'Urban population (1000 inhab)', '1958-1962', 1962.0, 14020.0],
                    ['Indonesia', 'World | Asia', 'urban_pop',
                     'Urban population (1000 inhab)', '1963-1967', 1967.0, 17206.0],
                    ['Indonesia', 'World | Asia', 'gdp',
                     'Gross Domestic Product (GDP) (current US$)', '1958-1962', np.nan,
                     np.nan],
                    ['Indonesia', 'World | Asia', 'gdp',
                     'Gross Domestic Product (GDP) (current US$)', '1963-1967',
                     1967.0, 5980840376.0],
                    ['United Kingdom', 'World | Europe', 'total_pop',
                     'Total population (1000 inhab)', '1958-1962', 1962.0, 53147.0],
                    ['United Kingdom', 'World | Europe', 'total_pop',
                     'Total population (1000 inhab)', '1963-1967', 1967.0, 54905.0],
                    ['United Kingdom', 'World | Europe', 'rural_pop',
                     'Rural population (1000 inhab)', '1958-1962', 1962.0, 11474.0],
                    ['United Kingdom', 'World | Europe', 'rural_pop',
                     'Rural population (1000 inhab)', '1963-1967', 1967.0, 12293.0],
                    ['United Kingdom', 'World | Europe', 'urban_pop',
                     'Urban population (1000 inhab)', '1958-1962', 1962.0, 41673.0],
                    ['United Kingdom', 'World | Europe', 'urban_pop',
                     'Urban population (1000 inhab)', '1963-1967', 1967.0, 42612.0],
                    ['United Kingdom', 'World | Europe', 'gdp',
                     'Gross Domestic Product (GDP) (current US$)', '1958-1962',
                     1962.0, 80601939635.0],
                    ['United Kingdom', 'World | Europe', 'gdp',
                     'Gross Domestic Product (GDP) (current US$)', '1963-1967',
                     1967.0, 111000000000.0]]

    df_in_index = [3024, 3025, 3600, 3601, 4176, 4177, 4752, 4753,
                   102900, 102901, 103644, 103645, 104388, 104389, 105132, 105133]

    df_in_columns = ['country', 'region', 'variable', 'variable_full', 'time_period',
                     'year_measured', 'value']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    return df_in


'''
def create_plot_data():
    """create sample data for plot unit tests.
    """
    df_in_values = [[11.89, 12.22, 12.32, 12.33, 12.34, 12.32, 12.3,  11.93, 11.88, 12.12,  12.12, 12.12],
                    [16.94, 19.34, 21.7,  24.07, 24.66, 24.83, 24.45, 24.35, 24.31, 24.28,  24.21, 24.21],
                    [2.897, 2.883, 2.986, 3.167, 3.153, 3.201, 3.398, 3.426, 3.445, 3.523,  3.539, 3.543],
                    [2.128, 2.128, 2.128, 2.128, 2.128, 2.128, 4.255, 4.255, 5.319, 4.894,  5.106, 5.957],
                    [2.567, 2.671, 2.727, 2.727, 2.727, 2.727, 2.807, 2.807, 2.719, 2.96,   4.003, 4.163]]
    df_in_index = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola']
    df_in_columns = ['1958-1962', '1963-1967', '1968-1972', '1973-1977', '1978-1982',
                     '1983-1987', '1988-1992', '1993-1997', '1998-2002', '2003-2007',
                     '2008-2012', '2013-2017']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)
    df_in.columns.name = 'time_period'
    df_in.index.name = 'country'

    return df_in
'''


def test_time_slice():
    # Define input dataframe
    df_in = create_test_data()

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[5980840376.0, 88701.0, 105907.0, 17206.0],
         [111000000000.0, 12293.0, 54905.0, 42612.0]],
        index=['Indonesia', 'United Kingdom'],
        columns=['gdp', 'rural_pop', 'total_pop', 'urban_pop'])

    df_true.index.name = 'country'
    df_true.columns.name = '1963-1967'

    # Compute test output

    df_test = time_slice(df_in, '1963-1967')

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_time_slice_empty():
    # Define input dataframe
    df_in = create_test_data()

    # Define expected output, df_true
    df_true = pd.DataFrame([], index=[],
                           columns=[])

    df_true.columns.name = '2013-2017'
    df_true.index.name = "country"

    # Compute test output
    df_test = time_slice(df_in, '2013-2017')

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_time_slice_non_df():
    df_in = 'This is not a dataframe.'

    with pytest.raises(TypeError):
        time_slice(df_in, '2013-2017')


def test_country_slice():
    df_in = create_test_data()

    df_true_values = [[80601939635.0, 111000000000.0],
                      [11474.0, 12293.0],
                      [53147.0, 54905.0],
                      [41673.0, 42612.0]]

    df_true_index = ['gdp', 'rural_pop', 'total_pop', 'urban_pop']

    df_true_columns = ['1958-1962', '1963-1967']

    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)
    df_true.index.name = 'United Kingdom'
    df_true.columns.name = 'time_period'

    df_test = country_slice(df_in, 'United Kingdom')

    assert df_test.equals(df_true)


def test_country_slice_empty():

    df_in = create_test_data()

    df_true = pd.DataFrame([], index=[],
                           columns=[])

    df_true.columns.name = 'time_period'
    df_true.index.name = "Wonderland"

    df_test = country_slice(df_in, 'Wonderland')

    assert df_test.equals(df_true)


def test_variable_slice():
    df_in = create_test_data()

    df_true_values = [[np.nan, 5980840376.0],
                      [80601939635.0, 111000000000.0]]

    df_true_index = ['Indonesia', 'United Kingdom']

    df_true_columns = ['1958-1962', '1963-1967']

    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)
    df_true.index.name = 'country'
    df_true.columns.name = 'time_period'

    df_test = variable_slice(df_in, 'gdp')

    assert df_test.equals(df_true)


def test_variable_slice_empty():
    df_in = create_test_data()

    df_true = pd.DataFrame([], index=[],
                           columns=[])

    df_true.columns.name = 'time_period'
    df_true.index.name = "country"

    df_test = variable_slice(df_in, 'mortality rate')

    assert df_test.equals(df_true)


def test_time_series():
    df_in = create_test_data()

    df_true_values = [[80601939635.0], [111000000000.0]]

    df_true_index = [1962, 1967]

    df_true_columns = ['gdp']

    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)
    df_true.index.name = 'year_measured'

    df_test = time_series(df_in, 'United Kingdom', 'gdp')

    assert df_test.equals(df_true)


def test_time_series_empty_country():
    df_in = create_test_data()

    df_true_values = np.array([], dtype='float')

    df_true_index = np.array([], dtype='int')

    df_true_columns = ['gdp']

    df_true = pd.DataFrame(df_true_values, index=df_true_index, columns=df_true_columns)
    df_true.index.name = 'year_measured'

    df_test = time_series(df_in, 'Wonderland', 'gdp')
    print(df_test.dtypes)
    print(df_true.dtypes)

    assert df_test.equals(df_true)
