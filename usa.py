#!/usr/bin/env python3

#
# This relies on the New York Times dataset
#
#  https://github.com/nytimes/covid-19-data.git (fetch)
#
# and it is assumed to be cloned to the home directory.
#

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
import os
import click

from scipy.signal import savgol_filter

import population as pops

# Crufty but useful for debugging.
#from pandasgui import show

nytimes = os.path.expanduser("~/covid-19-data/us.csv")
df = pd.read_csv(nytimes,
                 parse_dates = ['date']
                )

pop_us = 328.2e6

def funcs(fips):
    def fwd(x):
        return x / pop_us * 10000

    def rev(f):
        return f * pop_us / 10000

    return (fwd, rev)


def smooth(y):
    yhat = savgol_filter(y[1:], 7, 0)
    yhat = np.insert(yhat, 0, 0, axis=0)
    return yhat

def plot_them(daily):
    sdd = df

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=funcs(pop_us))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

    if len(sdd.index) == 0:
        print("no data")
        return

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    if daily:
        sdd['deaths'] = sdd['deaths'] - sdd['deaths'].shift(1)
        sdd['cases'] = sdd['cases'] - sdd['cases'].shift(1)


    sdd['cases-smoothed'] = smooth(sdd.cases.values)
    sdd['deaths-smoothed'] = smooth(sdd.deaths.values)

    ax = sdd.plot(ax=ax1, x='date', y='deaths', logy=False, grid=True,
                  title = ("New Deaths: " if daily else "Deaths: ") + "USA")

    if daily:
        sdd.plot(ax=ax1, x='date',  y='deaths-smoothed', grid=True, color='darksalmon')

    decorate(ax)

    ax = sdd.plot(ax=ax2, x='date', y='cases', logy=False, grid=True,
                  title = ("New Cases: " if daily else "Cases: ") + "USA")

    if daily:
        sdd.plot(ax=ax2, x='date',  y='cases-smoothed', grid=True, color='darksalmon')

    decorate(ax)

    fig.tight_layout()

@click.command()
@click.option("--daily/--cumulative", default=False, help="Daily cases or total cases")
def cmdline(daily):
    plot_them(daily)
    plt.show()

if __name__ == '__main__':
    cmdline()
