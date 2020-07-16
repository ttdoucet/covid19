#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
import sys
import math
import click

import population as pops
import util

# import state

url = 'https://covidtracking.com/api/v1/states/daily.csv'
dd = pd.read_csv(url,
                 usecols=['date', 'state', 'positive', 'positiveIncrease', 'death'],
                 parse_dates=['date'],
                 index_col=['state']
                 )

def smooth(y):
    yhat = savgol_filter(y, 7, 1)
    return yhat

from matplotlib.dates import DateFormatter
# from matplotlib.dates import ConciseDateFormatter
# import matplotlib.dates as mdates

def plot_grid(states, daily):
    n = len(states)
    
    s = int(math.sqrt(n))
    t = s
    while s * t < n:
        t = t + 1

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=pops.state_funcs([state]))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

        date_form = DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(date_form)

        for xlabel in ax.get_xticklabels():
            xlabel.set_fontsize(6)
            xlabel.set_rotation(20)

    fig, ax = plt.subplots(figsize=(24, 24))
    for i in range(n):
        ax = plt.subplot2grid( (t, s), (i//s, i%s) )

        state = states[i].upper()
        sdd = dd.loc[state].copy()

        if daily:
            ax = sdd.plot(ax=ax, x='date', y='positiveIncrease', grid=True, style='-',
                          color=util.case_color, alpha=0.25)
        else:
            ax = sdd.plot(ax=ax, x='date', y='positive', grid=True, style='-',
                          color=util.case_color)

        title = ax.set_title(state, loc='left',
                             color='black',
                             verticalalignment='top',
                             fontweight='roman')

        title.set_position([0.05, 0.85])

        if daily:
            delta = sdd.positiveIncrease.values
            delta[-1] = 0

            sdd['daily-cases-smoothed'] = smooth(delta)
            sdd.plot(ax=ax, x='date',  y='daily-cases-smoothed', grid=True, color=util.case_color)

        decorate(ax)

    fig.tight_layout()



import matplotlib
import sys

@click.command()
@click.option("--daily/--cumulative", default=True, help="Daily cases or total cases")
@click.argument('states', nargs=-1)
def cmdline(daily, states):
    if len(states) == 0:
        plot_grid( list(pops.population.keys()), daily)
    else:
        plot_grid(states, daily)
    plt.show()

if __name__ == '__main__':
    cmdline()
