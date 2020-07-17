#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import click
import os
import population as pops
import util

def read_nyt_states():
    nytimes = os.path.expanduser("~/covid-19-data/us-states.csv")

    dd = pd.read_csv(nytimes,
                     usecols=['date', 'state', 'cases', 'deaths'],
                     parse_dates=['date'],
                     )
    return dd

def plot_them(dd, states, daily, title):
    if not title:
        if len(states) == 1:
            title = states[0]
        else:
            title = "Combined"

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    sdd = dd.loc[dd['state'].isin(pops.full_states(states)) ].copy()
    sdd = sdd.groupby('date').sum()

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=pops.state_funcs(states))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

        date_form = DateFormatter("%m-%d")
        axis.xaxis.set_major_formatter(date_form)

        for xlabel in axis.get_xticklabels():
            xlabel.set_fontsize(8)
            xlabel.set_rotation(25)

    def plot(axis, df, column, **kwargs):
        ax = df.plot(ax=axis, y=column, grid=True, **kwargs)
        decorate(ax)
        return ax

    if daily == False:
        # cumulative deaths & cases
        plot(ax1, sdd, 'deaths', title=title + " deaths", color=util.death_color)
        plot(ax2, sdd, 'cases', title=title + " cases")
    else:
        # daily deaths
        util.calc_daily(sdd, 'deaths', 'deathIncrease')
        plot(ax1, sdd, 'deathIncrease', title=title + " daily deaths", color=util.death_color, alpha=0.25)

        delta = sdd.deathIncrease.values
        sdd.loc[:, 'deathIncrease-smoothed'] = util.smooth(delta)
        plot(ax1, sdd, 'deathIncrease-smoothed', color=util.death_color)

        # daily cases
        util.calc_daily(sdd, 'cases', 'positiveIncrease')
        plot(ax2, sdd, 'positiveIncrease', title=title + " daily cases", color=util.case_color, alpha=0.25)

        delta = sdd.positiveIncrease.values
        sdd.loc[:, 'daily-cases-smoothed'] = util.smooth(delta)
        plot(ax2, sdd, 'daily-cases-smoothed', color=util.case_color)

    fig.tight_layout()

@click.command()
@click.option("--daily/--cumulative", default=True, help="Daily cases or total cases")
@click.option("--title", default="", help="Label for plot.")
@click.option("--allstates/--specified", default=False, help="Combine all states for USA plot.")
@click.argument('states', nargs=-1)

def cmdline(daily, states, allstates, title):
    dd = read_nyt_states()

    if allstates:
        states = pops.population.keys()
    elif len(states) == 0:
        states = ['PA']
    plot_them(dd, states, daily, title);
    plt.show()

if __name__ == '__main__':
    cmdline()
