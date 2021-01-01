#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
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
                      index_col = ['county'],
                     )

def plot_them(fips, daily):
    if fips == 'New York City':
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
        util.calc_daily(sdd, 'deaths', 'daily_deaths');
        ax = sdd.plot(ax=ax1, x='date', y='daily_deaths', logy=False, grid=True,
                      color=util.death_color, alpha=0.25,
                      title = "Daily Deaths: " + place)

        sdd.loc[:, 'deaths-smoothed'] = util.smooth(sdd.daily_deaths.values)
        sdd.plot(ax=ax1, x='date',  y='deaths-smoothed', grid=True, color=util.death_color)

    else:
        ax = sdd.plot(ax=ax1, x='date', y='deaths', logy=False, grid=True,
                      color=util.death_color,
                      title = "Deaths: " + place)
    decorate(ax)

    if daily:
        util.calc_daily(sdd, 'cases', 'daily_cases');
        ax = sdd.plot(ax=ax2, x='date', y='daily_cases', logy=False, grid=True,
                      color=util.case_color, alpha=0.25,
                      title = ("Daily Cases: " + place))

        sdd['cases-smoothed'] = util.smooth(sdd.daily_cases.values)
        sdd.plot(ax=ax2, x='date',  y='cases-smoothed', grid=True, color=util.case_color)

    else:
        ax = sdd.plot(ax=ax2, x='date', y='cases', logy=False, grid=True,
                      color=util.case_color,
                      title = ("Cases: " + place))
    decorate(ax)
    fig.tight_layout()


def plot_combined(counties, daily, title):

    dd = pd.read_csv(nytimes,
                     usecols=['date', 'fips', 'cases', 'deaths'],
                     parse_dates=['date'],
    )

    sdd = dd.loc[dd['fips'].isin(counties)].copy()
    sdd = sdd.groupby('date').sum()

    def decorate(axis):
        axis.set_xlabel('')
        sec = axis.secondary_yaxis('right', functions=pops.county_funcs(counties))
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

    #place = pops.county_name(fips)
    if title:
        place = title
    else:
        place = "Combined"

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    if daily:
        util.calc_daily(sdd, 'deaths', 'daily_deaths');
        ax = sdd.plot(ax=ax1, y='daily_deaths', logy=False, grid=True,
                      color=util.death_color, alpha=0.25,
                      title = "Daily Deaths: " + place)

        sdd.loc[:, 'deaths-smoothed'] = util.smooth(sdd.daily_deaths.values)
        sdd.plot(ax=ax1, y='deaths-smoothed', grid=True, color=util.death_color)

    else:
        ax = sdd.plot(ax=ax1, y='deaths', logy=False, grid=True,
                      color=util.death_color,
                      title = "Deaths: " + place)
    decorate(ax)

    if daily:
        util.calc_daily(sdd, 'cases', 'daily_cases');
        ax = sdd.plot(ax=ax2, y='daily_cases', logy=False, grid=True,
                      color=util.case_color, alpha=0.25,
                      title = ("Daily Cases: " + place))

        sdd['cases-smoothed'] = util.smooth(sdd.daily_cases.values)
        sdd.plot(ax=ax2, y='cases-smoothed', grid=True, color=util.case_color)

    else:
        ax = sdd.plot(ax=ax2, y='cases', logy=False, grid=True,
                      color=util.case_color,
                      title = ("Cases: " + place))
    decorate(ax)
    fig.tight_layout()


@click.command()
@click.option("--daily/--cumulative", default=False, help="Daily cases or total cases")
@click.option("--combined/--separate", default=False, help="Plot counties separately or combined into  super-county.")
@click.option("--title", default="", help="Label for plot.")
@click.argument('counties', nargs=-1)
def cmdline(daily, counties, combined, title):
    if combined:
        plot_combined(counties, daily, title)
    else:
        for county in counties:
            plot_them(county, daily)
    plt.show()

if __name__ == '__main__':
    cmdline()
