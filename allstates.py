#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import sys
import os
import math
import click
import population as pops
import util

def read_nyt_states():
    nytimes = os.path.expanduser("~/covid-19-data/us-states.csv")

    dd = pd.read_csv(nytimes,
                     usecols=['date', 'state', 'cases', 'deaths'],
                     parse_dates=['date']
                     )
    return dd

dd = read_nyt_states()

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

    dd.set_index('state', inplace=True)
    fig, ax = plt.subplots(figsize=(24, 24))
    for i in range(n):
        ax = plt.subplot2grid( (t, s), (i//s, i%s) )

        state = states[i].upper()
        fstate = pops.full_state(state)

        sdd = dd.loc[fstate].copy()
        sdd.set_index('date', inplace=True)
        sdd.sort_index(inplace=True)

        if daily:
            util.calc_daily(sdd, 'cases', 'positiveIncrease')
            ax = sdd.plot(ax=ax, y='positiveIncrease', grid=True,
                          color=util.case_color, alpha=0.25)
        else:
            ax = sdd.plot(ax=ax, y='cases', grid=True,
                          color=util.case_color)

        title = ax.set_title(state, loc='left',
                             color='black',
                             verticalalignment='top',
                             fontweight='roman')

        title.set_position([0.05, 0.85])

        if daily:
            sdd['daily-cases-smoothed'] = util.smooth(sdd.positiveIncrease.values)
            sdd.plot(ax=ax, y='daily-cases-smoothed', grid=True, color=util.case_color)

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
