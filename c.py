#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys

url = 'https://covidtracking.com/api/v1/states/daily.csv'
dd = pd.read_csv(url,
                 usecols=['date', 'state', 'positive', 'positiveIncrease', 'death'],
                 parse_dates=['date'],
                 index_col=['state']
                 )

population = {'CA': 39.512e6,
              'TX': 28.995e6,
              'FL': 21.447e6,
              'NY': 19.453e6,
              'PA': 12.802e6,
              'IL': 12.672e6,
              'OH': 11.689e6,              
              'GA': 10.617e6,
              'NC': 10.488e6,
              'MI': 9.987e6,
              'NJ': 8.882e6,
              'VA': 8.536e6,
              'WA': 7.615e6,
              'AZ': 7.279e6,
              'MA': 6.950e6,
              'TN': 6.833e6,
              'IN': 6.732e6,
              'MO': 6.137e6,
              'MD': 6.046e6,
              'WI': 5.822e6,
              'CO': 5.759e6,
              'MN': 5.640e6,
              'SC': 5.149e6,
              'AL': 4.903e6,
              'LA': 4.649e6,
              'KY': 4.468e6,
              'OR': 4.218e6,
              'OK': 3.957e6,
              'CT': 3.565e6,
              'UT': 3.206e6,
              'IA': 3.155e6,
              'NV': 3.080e6,
              'AR': 3.018e6,
              'MS': 2.976e6,
              'KS': 2.913e6,
              'NM': 2.097e6,
              'NE': 1.934e6,
              'ID': 1.787e6,
              'WV': 1.792e6,
              'HI': 1.415e6,
              'NH': 1.360e6,
              'ME': 1.344e6,
              'MT': 1.069e6,
              'RI': 1.059e6,
              'DE': 973764,
              'SD': 884659,
              'ND': 762062,
              'AK': 731545,
              'DC': 705749,
              'VT': 623989,
              'WY': 578759
             }

def funcs(state):
    def fwd(x):
        return x / population[state] * 10000

    def rev(f):
        return f * population[state] / 10000

    return (fwd, rev)

def plot_them(state):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    sdd = dd.loc[state]

    def decorate(axis):
        ax.set_xlabel('')
        sec = ax.secondary_yaxis('right', functions=funcs(state))
        sec.set_ylabel('per 10k population')

    ax = sdd.plot(ax=ax1, x='date', y='positive', grid=True, title=state+ " cases")
    decorate(ax1)

    ax = sdd.plot(ax=ax2, x='date', y='death', grid=True, title=state+" deaths")
    decorate(ax2)

    fig.tight_layout()

if len(sys.argv) == 1:
    plot_them("PA")
else:
    for state in sys.argv[1:]:
        plot_them(state.upper())

plt.show()
