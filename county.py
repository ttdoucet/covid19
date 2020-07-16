#!/usr/bin/env python3

#
# This relies on the New York Times dataset
#
#  https://github.com/nytimes/covid-19-data.git (fetch)
#
# and it is assumed to be cloned to the home directory.
#
# This dataset is organized by FIPS county code, except
# for the case of New York City, whose five counties are
# collected into one place named New York City, with the
# FIPS code left blank.
#
# On the command line, you can type either a FIPS county code
# or the string "New York City", or any combination.
#

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from scipy.signal import savgol_filter
import numpy as np
import sys
import glob
import os
import click

import population as pops
import util

nytimes = os.path.expanduser("~/covid-19-data/us-counties.csv")
by_fips = pd.read_csv(nytimes,
                      parse_dates = ['date'],
                      index_col = ['fips']
                     )
by_name = pd.read_csv(nytimes,
                      parse_dates = ['date'],
                      index_col = ['county']
                     )

nyc = 'New York City'

def smooth(y):
    yhat = savgol_filter(y, 7, 1)
    return yhat

def plot_them(fips, daily):
    if fips == nyc:
        sdd = by_name.loc[fips].copy()
    else:
        fips = int(fips)
        sdd = by_fips.loc[fips].copy()

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=pops.county_funcs([fips]))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()
        date_form = DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(date_form)

        for xlabel in ax.get_xticklabels():
            xlabel.set_fontsize(8)
            xlabel.set_rotation(20)

    if len(sdd.index) == 0:
        print("no data")
        return

    place = pops.county_name(fips)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    if daily:
        sdd.loc[:, 'daily_deaths'] = sdd['deaths'] - sdd['deaths'].shift(1)
        sdd.loc[:, 'daily_cases'] = sdd['cases'] - sdd['cases'].shift(1)
        sdd.daily_deaths = sdd.daily_deaths.fillna(0)
        sdd.daily_cases = sdd.daily_cases.fillna(0)

        ax = sdd.plot(ax=ax1, x='date', y='daily_deaths', logy=False, grid=True,
                      color=util.death_color, alpha=0.25,
                      title = "Daily Deaths: " + place)

        sdd.loc[:, 'deaths-smoothed'] = smooth(sdd.daily_deaths.values)
        sdd.plot(ax=ax1, x='date',  y='deaths-smoothed', grid=True, color=util.death_color)

    else:
        ax = sdd.plot(ax=ax1, x='date', y='deaths', logy=False, grid=True,
                      color=util.death_color,
                      title = "Deaths: " + place)

    decorate(ax)

    if daily:
        ax = sdd.plot(ax=ax2, x='date', y='daily_cases', logy=False, grid=True,
                      color=util.case_color, alpha=0.25,
                      title = ("Daily Cases: " + place))

        sdd['cases-smoothed'] = smooth(sdd.daily_cases.values)
        sdd.plot(ax=ax2, x='date',  y='cases-smoothed', grid=True, color=util.case_color)

    else:
        ax = sdd.plot(ax=ax2, x='date', y='cases', logy=False, grid=True,
                      color=util.case_color,
                      title = ("Cases: " + place))

    decorate(ax)

    fig.tight_layout()


@click.command()
@click.option("--daily/--cumulative", default=False, help="Daily cases or total cases")
@click.argument('counties', nargs=-1)
def cmdline(daily, counties):
    if len(counties) == 0:
        plot_them(42003, daily) # Allegheny County
    else:
        for county in counties:
            plot_them(county, daily)
    plt.show()

if __name__ == '__main__':
    cmdline()
