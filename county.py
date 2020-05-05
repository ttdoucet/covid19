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
# Presently this code cannot show the NYC data for this reason.
#

import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob
import os

import population as pops

# Crufty but useful for debugging.
# from pandasgui import show

nytimes = os.path.expanduser("~/covid-19-data/us-counties.csv")
dd = pd.read_csv(nytimes,
                 parse_dates = ['date'],
                 index_col = ['fips']
                )

def funcs(fips):
    fips = int(fips)
    def fwd(x):
        return x / pops.county_pop(fips) * 10000

    def rev(f):
        return f * pops.county_pop(fips) / 10000

    return (fwd, rev)

def plot_them(fips):
    fips = int(fips)

    sdd = dd.loc[fips]

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=funcs(fips))
        sec.set_ylabel('per 10k population')
        axis.get_legend().remove()

    if len(sdd.index) == 0:
        print("no data")
        return

    place = pops.county_name(fips)
    print(place + ": ", pops.county_pop(fips))

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    ax = sdd.plot(ax=ax1, x='date', y='deaths', logy=False, grid=True, title = "Deaths: " + place)
    decorate(ax)

    ax = sdd.plot(ax=ax2, x='date', y='cases', logy=False, grid=True, title = "Confirmed: " + place)
    decorate(ax)

    fig.tight_layout()


def fip_stat(fips):
    pop = pops.county_pop(fips)
    name = pops.county_name(fips)
    print(name + ": " + str(pop) )

if len(sys.argv) == 1:
    plot_them(42003) # Allegheny County

else:
    for fips in sys.argv[1:]:
        plot_them(fips.upper())

plt.show()
