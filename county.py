#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob
import os

import population as pops

# Crufty but useful for debugging.
#from pandasgui import show

data_dir = os.path.expanduser("~/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/")
files = glob.glob(data_dir + "*.csv")

data_frames = [pd.read_csv(file) for file in files]
combined_df = pd.concat(data_frames, ignore_index=True)
combined_df['date'] = 'date'

fips_df = combined_df[combined_df.FIPS.notnull()]
fips_df['date'] = pd.to_datetime(fips_df['Last_Update'])

def plot_them(fips):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    sdd = fips_df[fips_df.FIPS==int(fips)]
    sdd_sort = sdd.sort_values(by="date")

    def decorate(axis):
        ax.set_xlabel('')
        ax.get_legend().remove()

    place = sdd['Combined_Key'].iloc[0]
    print("place: ", place)

    ax = sdd.plot(ax=ax1, x='date', y='Deaths', logy=False, grid=True, title = "Deaths: " + place)
    decorate(ax2)

#    ax = sdd.plot(ax=ax1, x='date', y='Confirmed', logy=False, grid=True, title = "Confirmed: " + place)
#    decorate(ax1)

    ax = sdd.plot(ax=ax2, x='date', y='Confirmed', logy=False, grid=True, title = "Confirmed: " + place)
    decorate(ax1)

    fig.tight_layout()

if len(sys.argv) == 1:
    plot_them("42003")
else:
    for fips in sys.argv[1:]:
        plot_them(fips.upper())

plt.show()
