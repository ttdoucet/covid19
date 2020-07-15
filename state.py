#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from scipy.signal import savgol_filter
import numpy as np
import sys
import click

import population as pops
import util

url = 'https://covidtracking.com/api/v1/states/daily.csv'
dd = pd.read_csv(url,
                 usecols=['date', 'state', 'positive', 'positiveIncrease', 'death', 'deathIncrease'],
                 parse_dates=['date'],
                 index_col=['state']
                 )

def smooth(y):
    yhat = savgol_filter(y, 7, 1)
    return yhat

def plot_them(state, daily):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    sdd = dd.loc[state].copy()

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=pops.state_funcs(state))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

        date_form = DateFormatter("%m-%d")
        axis.xaxis.set_major_formatter(date_form)


    if daily == False:
        # Cumulative Deaths
        ax = sdd.plot(x='date', y='death', ax=ax1, grid=True, title=state+" deaths", color=util.death_color)
        decorate(ax)

        # Cumulative Cases
        ax = sdd.plot(ax=ax2, x='date', y='positive', grid=True, title=state+ " cases")
        decorate(ax)

    else:
        # Daily Deaths
        ax = sdd.plot(ax=ax1, x='date', y='deathIncrease',
                      color=util.death_color, alpha=0.25,
                      grid=True,
                      title=state+ " daily deaths")

        delta = sdd.deathIncrease.values
        delta[-1] = 0

        sdd.loc[:, 'deathIncrease-smoothed'] = smooth(delta)

        sdd.plot(ax=ax1, x='date',  y='deathIncrease-smoothed', grid=True, color=util.death_color)
        decorate(ax)

        # Daily Cases
        ax = sdd.plot(ax=ax2, x='date', y='positiveIncrease',
                      color=util.case_color, alpha=0.25,
                      grid=True,
                      title=state+ " daily cases")

        delta = sdd.positiveIncrease.values
        delta[-1] = 0

        sdd.loc[:, 'daily-cases-smoothed'] = smooth(delta)
        sdd.plot(ax=ax2, x='date',  y='daily-cases-smoothed', grid=True, color=util.case_color)

        decorate(ax)

    fig.tight_layout()

@click.command()
@click.option("--daily/--cumulative", default=True, help="Daily cases or total cases")
@click.argument('states', nargs=-1)
def cmdline(daily, states):
    if len(states) == 0:
        plot_them('PA', daily)
    else:
        for state in states:
            plot_them(state.upper(), daily)
    plt.show()

if __name__ == '__main__':
    cmdline()
