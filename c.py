#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys

import population as pops

url = 'https://covidtracking.com/api/v1/states/daily.csv'
dd = pd.read_csv(url,
                 usecols=['date', 'state', 'positive', 'positiveIncrease', 'death'],
                 parse_dates=['date'],
                 index_col=['state']
                 )


def funcs(state):
    def fwd(x):
        return x / pops.us_pop(state) * 10000

    def rev(f):
        return f * pops.us_pop(state) / 10000

    return (fwd, rev)

def plot_them(state):
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))
    sdd = dd.loc[state]

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=funcs(state))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

    ax = sdd.plot(ax=ax1, x='date', y='death', grid=True, title=state+" deaths")
    decorate(ax)

    ax = sdd.plot(ax=ax2, x='date', y='positive', grid=True, title=state+ " cases")
    decorate(ax)

    ax = sdd.plot(ax=ax3, x='date', y='positiveIncrease', grid=True, title=state+ " daily cases")
    decorate(ax)

    fig.tight_layout()
    # fig.savefig(state+".png")

if len(sys.argv) == 1:
    plot_them("PA")
else:
    for state in sys.argv[1:]:
        plot_them(state.upper())

plt.show()
