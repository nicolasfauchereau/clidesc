#!/opt/anaconda/bin/python
# coding=utf-8

# DroughtMonitoring.py

# PROJECT: Integrating climate change risks in agriculture and health sectors in Samoa
# Author: Nicolas Fauchereau, NIWA
# Date: August 2014
# can test using: 
# `./DroughtMonitoring.py base_path stations from_date to_date` 

### ===========================================================================
# imports
import os, sys
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

### ===========================================================================
# Settings
### ===========================================================================
print("Programme: DroughtMonitoring.py\n")

# set to `True` is testing on a local dataset instead of a clide table
local = False

### ===========================================================================
### defines minimum year (station needs to have been opened before that date)
### ===========================================================================
min_year = 1972

### ===========================================================================
### defines the window (days)
### ===========================================================================
window = 90

### ===========================================================================
### defines the minimum percentage of obs to calculate an avearge in the window
### ===========================================================================
min_per = 0.6

### ===========================================================================
### defines the `alert` levels (in percentage of normal)
### ===========================================================================
level_1 = 60
level_2 = 30

# prints the system date
print("Date: %s\n" % ( time.strftime("%d-%m-%Y") ))

### ===========================================================================
# CLIDE utilities
### ===========================================================================
if local:
    sys.path.append('../common')
    # clide: the interface to clide itself
    from clide import *
    # utils: some utility functions
    from utils import *
else:
    # source path from the absolute path containing the script
    source_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    #source_path = os.getcwd()
    sys.path.append(os.path.join(source_path, '../common'))
    # clide: the interface to clide itself
    from clide import *
    # utils: some utility functions
    from utils import *
    # opens the connection
    conn = clidesc_open(base_path)

### ===========================================================================
# STATION DETAILS
### ===========================================================================
if local:
    sName = 'Station_Name'
else:
    station = clidesc_stations(conn, stations)
    # get the primary name 
    sName = station['name_primary']
    # get the start date
    sDate = station['start_date'][0]

### ===========================================================================
# tests the opening data of the station
### ===========================================================================
if pd.to_datetime(sDate) > datetime(min_year,1,1):
    print("! WARNING, the station has been opened after 1972, not enough data to calculate normals\n")
    sys.exit(1)

### ===========================================================================
# DATA SETUP
### ===========================================================================

if local:
    # if local expects this file in the same directory
	iFile = './Apia_rain24h.csv'
	iData = pd.read_csv(iFile, index_col=0)
else:
    #loads the data from clide
    iData = clidesc_rain24h(conn, stations, datetime(min_year, 1 1).strftime("%Y-%m-%d"), to_date)

# The DataFrame from clide is likely to contain missing indexes
# so we create a continuous datetime index and reindex 

daterange = pd.period_range(start = datetime(min_year, 1 1).strftime("%Y-%m-%d"), end = to_date, freq = 'D').to_datetime()

iData = iData.reindex(daterange)

### ===========================================================================
### calculates the rolling cumulative rainfall over the period
### ===========================================================================

min_periods = np.int(np.floor(min_per * window))
datars = pd.rolling_sum(iData[['rain_24h']], window, min_periods=min_periods)

### ===========================================================================
### calculates monthly means (will be displayed by the green bars in the graphics)
### ===========================================================================

datam = iData[['rain_24h']].resample('1M', how='sum')
datam.columns = [['monthly means']]

### ===========================================================================
### calculates the normals for the [window] days periods 
### ===========================================================================

normal = ['1972-01-01','2012-12-31']

normals = datars[normal[0]:normal[-1]]

normals['year'] = normals.index.year
normals['month'] = normals.index.month
normals['day'] = normals.index.day

datars['year'] = datars.index.year
datars['month'] = datars.index.month
datars['day'] = datars.index.day

clim = normals.groupby(['month','day'])[['rain_24h']].mean()

clim['month'] = clim.index.get_level_values(0)
clim['day'] = clim.index.get_level_values(1)

merged_df_mean = pd.merge(datars, clim, how='left', on=['month','day'])

merged_df_mean = merged_df_mean.sort(['year','month','day'], axis=0)

merged_df_mean.columns = ['rain_24h', 'year', 'month','day', 'clim']

### ===========================================================================
### calculates the anomalies (in percentage of normals) for the [window] days 
### periods and add these to the DataFrame
### ===========================================================================

merged_df_mean['anomalies'] = (merged_df_mean['rain_24h'] / merged_df_mean['clim']) * 100.

merged_df_mean.index = datars.index

merged_df_mean['monthly means'] = datam['monthly means']

merged_df_mean['monthly means'].fillna(method='bfill', inplace=True)

### ===========================================================================
### Selects the period (from_date to the end)
### ===========================================================================

subsetper = merged_df_mean[from_date::]

### ===========================================================================
### plot
### ===========================================================================

f, ax = plt.subplots(figsize=(12,8))

f.subplots_adjust(bottom=0.15, left=0.08, right=1)

### get the axes position and shrink the width to 80 % (for legend placement)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.78, box.height])

### first ax: monthtly average rainfall (mm)

ax.plot(subsetper.index, subsetper['monthly means'], color='g', alpha=0.5)
ax.fill_between(subsetper.index, subsetper['monthly means'],color='g', alpha=0.3)
ax.set_ylim(0, max(subsetper['monthly means'] + 0.2 * subsetper['monthly means']))
ax.set_ylabel("monthly (calendar month) rainfall (mm)")
[l.set_rotation(90) for l in ax.xaxis.get_ticklabels()]
ax.grid('off') # no grid lines for the monthly rainfall


### second ax: [window] days anomalies (% of normal)

ax2 = ax.twinx()
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.78, box.height])


ax2.plot(subsetper.index, subsetper['anomalies'], lw=2, color='b', label='90 days rainfall', zorder=12)

# horizontal lines
ax2.axhline(100, color='k', zorder=10)
ax2.axhline(level_1, color='r', zorder=10)
ax2.axhline(level_2, color='r', zorder=10, lw=2)

ax2.fill_between(subsetper.index, subsetper['anomalies'], np.ones(len(subsetper)) * 100., \
                 where=subsetper['anomalies'] > 100., color='b', interpolate=True, alpha=0.05)

ax2.fill_between(subsetper.index, subsetper['anomalies'], np.ones(len(subsetper)) * 30., \
                 where=subsetper['anomalies'] < level_2, color='#700000', interpolate=True, alpha=0.9)

ax2.fill_between(subsetper.index, subsetper['anomalies'], np.ones(len(subsetper)) * 60., \
                 where=subsetper['anomalies'] < level_1, color='r', interpolate=True, alpha=0.4)

ax2.fill_between(subsetper.index, subsetper['anomalies'], np.ones(len(subsetper)) * 100., \
                 where=subsetper['anomalies'] < 100., color='r', interpolate=True, alpha=0.05)

ax2.set_ylabel('percentage of normal', fontsize=16)

ax2.grid('on') # gridlines ON for the percentage anomalies

ax2.set_ylim(0, subsetper['anomalies'].max()+5)

# this proves necessary or the (possible) missing values 
# at the end are ignored in the plot ...
ax2.set_xlim(subsetper.index[0], subsetper.index[-1])

# title
ax2.set_title("{} days cumulative rainfall anomalies (% of normal)\nending {}".format(window, subsetper.index[-1].strftime("%d %B %Y")), fontsize=16)

### legend section
p1 = plt.Rectangle((0, 0), 1, 1, fc="r", alpha=0.05)
p2 = plt.Rectangle((0, 0), 1, 1, fc="r", alpha=0.4)
p3 = plt.Rectangle((0, 0), 1, 1, fc="#700000", alpha=0.9)
leg = plt.legend([p1, p2, p3], ['< mean', '< 60%', '< 30%'],\
          loc='upper left', bbox_to_anchor = (1.035, 1.01), fontsize=19)
leg.draw_frame(False)

# saves the figure in png (dpi = 200)
f.savefig(os.path.join(base_path,'drought_monitoring_{}days_{}.png'.format(window, station_no)), dpi=200)
