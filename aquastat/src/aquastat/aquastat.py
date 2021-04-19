import logging.config
import logging
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Set logging configuration
config_path = str(Path(__file__).parent.absolute()) + '\\..\\..\\logging.conf'
logging.config.fileConfig(config_path)
logger = logging.getLogger(__name__)


def time_slice(df, time_period):
    """For a `time_period`, creates a dataframe with a row for each country and
    a column for each AQUASTAT variable. Time periods are of the format '%Y-%Y',
    in four year increments from 1958 to 2017.

    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        time_period: time period for filtering the data set and pivoting

    Returns:
        df (:obj:`pandas.DataFrame`): Pivoted dataframe
    """

    if not isinstance(df, pd.DataFrame):
        logger.error('input is not a dataframe')
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for time period of interest
    df = df[df.time_period == time_period]

    # Pivot table
    df = df.pivot(index='country', columns='variable', values='value')

    df.columns.name = time_period

    if df.empty:
        logger.warning('dataframe is empty.')

    return df


def country_slice(df, country):
    """Creates a dataframe that tracks changes over time for all AQUASTAT variables
    given a user-specified country.
    """

    if not isinstance(df, pd.DataFrame):
        logger.error('input is not a dataframe')
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for country of interest
    df = df[df.country == country]

    # Pivot table
    df = df.pivot(index='variable', columns='time_period', values='value')

    df.index.name = country

    if df.empty:
        logger.warning('dataframe is empty.')

    return df


def variable_slice(df, variable):
    """Creates a dataframe that tracks data over time for all countries given a user-specified
    AQUASTAT variable.
    """
    if not isinstance(df, pd.DataFrame):
        logger.error('input is not a dataframe')
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    df = df[df.variable == variable]
    df = df.pivot(index='country', columns='time_period', values='value')

    if df.empty:
        logger.warning('dataframe is empty.')

    return df


def time_series(df, country, variable):
    """For a `country` and 'variable' pair, creates a dataframe with
    a row for each year and a column for the corresponding data.

    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        country: full country name, capitalized
        variable: abbreviated AQUASTAT variable name

    Returns:
        df (:obj:`pandas.DataFrame`): time series dataframe
    """

    if not isinstance(df, pd.DataFrame):
        logger.error('input is not a dataframe')
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for country/variable combo
    series = df[(df.country == country) & (df.variable == variable)]

    # Drop years with no data
    series = series.dropna()[['year_measured', 'value']]

    # Change years to int and set as index
    series.year_measured = series.year_measured.astype(int)
    series.set_index('year_measured', inplace=True)
    series.columns = [variable]

    return series


def plot_heatmap(df,
                 title='',
                 xlabel=None,
                 ylabel=None,
                 label_size=20,
                 tick_label_size=16,
                 cmap=None,
                 xticklabels=None,
                 yticklabels=None,
                 figsize=None,
                 xrotation=90,
                 yrotation=0,
                 **kwargs):
    """Creates a heatmap given a dataframe with numeric dtype, specified index, column, index name,
    and column name.

    Args:
        df: :obj:`pandas.DataFrame` with numeric dtype, specified index, column, index name,
            and column name
        title: title of the heatmap
        xlabel: X label; default is the dataframe column name
        ylabel: Y label; default is the dataframe index name
        label_size: font size of labels
        tick_label_size: font size of tick labels
        cmap: matplotlib colormap name or object, or list of colors, optional
        xticklabels: tick labels on the x axis; default is the dataframe column labels
        yticklabels: tick labels on the y axis; default is the dataframe indices
        figsize: figure size; default is 16 x 8 inches
        xrotation: degrees of rotation of xticklabels
        yrotation: degrees of rotation of yticklabels
        **kwargs: other keyword arguments that can go into the matplotlib heatmap method

    Returns:
        fig (:obj:`matplotlib.pyplot.subplots`): heatmap
    """

    if figsize is None:
        figsize = (16, 8)
    fig, ax = plt.subplots(figsize=figsize)

    if xlabel is None:
        xlabel = ' '.join(df.columns.name.split('_')).capitalize()
    if ylabel is None:
        ylabel = ' '.join(df.index.name.split('_')).capitalize()

    yticklabels = df.index.tolist() if yticklabels is None else yticklabels
    xticklabels = df.columns.tolist() if xticklabels is None else xticklabels

    if cmap is None:
        cmap = sns.cubehelix_palette(8, start=.5, rot=-.75)

    ax = sns.heatmap(df, cmap=cmap, **kwargs)
    ax.set_xticklabels(xticklabels, rotation=xrotation, size=tick_label_size)
    ax.set_yticklabels(yticklabels, rotation=yrotation, size=tick_label_size)

    ax.set_title(title, size=label_size)
    ax.set_xlabel(xlabel, size=label_size)
    ax.set_ylabel(ylabel, size=label_size)

    ax.set_ylim([0, len(df)])

    return fig, ax


def plot_histogram(df,
                   column,
                   title='',
                   xlabel=None,
                   ylabel=None,
                   label_size=20,
                   color='#0085ca',
                   alpha=0.8,
                   figsize=None,
                   **kwargs):
    """Creates a histogram given a specified numeric column of a dataframe.

    Args:
        df: :obj:`pandas.DataFrame`
        column: column of the dataframe used to plot the histogram, must have numeric dtype
        title: title of the histogram
        xlabel: X label of the histogram; default is the column name
        ylabel: Y label of the histogram; default is 'Count'
        label_size: font size of the labels
        color: color of the histogram; default is blue
        alpha: transparency level of the histogram; default is 0.8
        figsize: figure size; default is 12 x 8 inches
        **kwargs: additional keyword arguments that can go into the matplotlib histogram method

    Returns:
        fig (:obj:`matplotlib.pyplot.subplots`): histogram
    """

    if figsize is None:
        figsize = (12, 8)
    fig, ax = plt.subplots(figsize=figsize)

    if xlabel is None:
        xlabel = ' '.join(column.split('_')).capitalize()
    if ylabel is None:
        ylabel = 'Count'

    ax.hist(df[column], color=color, alpha=alpha, **kwargs)

    ax.set_title(title, size=label_size)
    ax.set_xlabel(xlabel, size=label_size)
    ax.set_ylabel(ylabel, size=label_size)

    return fig, ax


if __name__ == '__main__':
    time_slice('1', '1234')
