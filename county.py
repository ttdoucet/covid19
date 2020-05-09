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
import sys
import glob
import os
import click

import population as pops

# Crufty but useful for debugging.
# from pandasgui import show

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

def funcs(fips):
    if fips != nyc:
        fips = int(fips)

    def fwd(x):
        return x / pops.county_pop(fips) * 10000

    def rev(f):
        return f * pops.county_pop(fips) / 10000

    return (fwd, rev)

def plot_them(fips, daily):
    if fips == nyc:
        sdd = by_name.loc[fips]
    else:
        fips = int(fips)
        sdd = by_fips.loc[fips]

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

    if daily:
        sdd['deaths'] = sdd['deaths'] - sdd['deaths'].shift(1)
        sdd['cases'] = sdd['cases'] - sdd['cases'].shift(1)

    ax = sdd.plot(ax=ax1, x='date', y='deaths', logy=False, grid=True,
                  title = ("New Deaths: " if daily else "Deaths: ") + place)
    decorate(ax)

    ax = sdd.plot(ax=ax2, x='date', y='cases', logy=False, grid=True,
                  title = ("New Cases: " if daily else "Cases: ") + place)
    decorate(ax)

    fig.tight_layout()


def fip_stat(fips):
    pop = pops.county_pop(fips)
    name = pops.county_name(fips)
    print(name + ": " + str(pop) )

@click.command()
@click.option("--daily/--cumulative", default=False, help="Daily cases or total cases")
@click.argument('counties', nargs=-1)
def foobar(daily, counties):
    if len(counties) == 0:
        plot_them(42003, daily) # Allegheny County
    else:
        for county in counties:
            plot_them(county, daily)
    plt.show()

if __name__ == '__main__':
    foobar()


# if len(sys.argv) == 1:
#     plot_them(42003) # Allegheny County

# else:
#     for fips in sys.argv[1:]:
#         plot_them(fips)

# plt.show()
