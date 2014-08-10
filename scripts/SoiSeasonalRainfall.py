#!/opt/anaconda/bin/python
# coding=utf-8

# SoiSeasonalRainfall.py

# PROJECT: Integrating climate change risks in agriculture and health sectors in Samoa
# Author: Nicolas Fauchereau, NIWA
# Date: August 2014
# can test using:
# `./SoiSeasonalRainfall.py base_path stations from_date to_date`

### ===========================================================================
# imports
import os, sys
import time
from datetime import datetime, timedelta
from calendar import month_abbr
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from matplotlib import pyplot as plt
try:
    import seaborn as sb
    seaborn = True
except:
    print("we don't plot the seaborn module'")
    seaborn = False

### ===========================================================================
# Settings
### ===========================================================================
print("Programme: SoiSeasonalRainfall.py\n")

# set to `True` is testing on a local dataset instead of a clide table
local = False

# prints the system date
print("Date: %s\n" % ( time.strftime("%d-%m-%Y") ))

### ===========================================================================
# CLIDE utilities
### ===========================================================================
if local:
    sys.path.append('../clidesc')
    # clide: the interface to clide itself
    from clide import *
    # utils: some utility functions
    from utils import *
else:
    # source path from the absolute path containing the script
    source_path = os.path.dirname(os.path.realpath(sys.argv[0]))
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
    sName = station['name_primary'][0]
    # get the start date
    sDate = station['start_date'][0]

### ===========================================================================
# DATA SETUP
### ===========================================================================

if local:
    # if local expects this file in the same directory
	iFile = './Apia_rain24h.csv'
	iData = pd.read_csv(iFile, index_col=0)
else:
    #loads the data from clide
    iData = clidesc_rain24h(conn, stations, from_date, to_date)

clidesc_progress(base_path, 10)

"""
sorts the data in chronological order just in case
"""
iData.sort_index(inplace=True)


"""
The DataFrame from clide is likely to contain missing indexes
so we create a continuous datetime index and reindex
"""

daterange = pd.period_range(start = from_date, end = to_date, freq = 'D').to_datetime()
iData = iData.reindex(daterange)


"""
Then we reindex again to have 'complete' years, starting the
1st of Jan. of the first year selected, ending the 31st of Dec. of the last year
"""
index = pd.date_range(start = datetime(iData.index.year[0], 1, 1), \
                     end = datetime(iData.index.year[-1], 12, 31), freq='1D')
iData = iData.reindex(index)

clidesc_progress(base_path, 20)

"""
minimum number of days for calculating a monthly statistic
"""
minvals = 20

def calcmonsum(x):
    if pd.isnull(x).sum() <= minvals:
        z = x.sum()
    else:
        z = np.NaN
    return z


"""
Calculates monthly cumulative rainfall and index
"""
mData = iData.groupby([iData.index.year, iData.index.month])[['rain_24h']].aggregate(calcmonsum)
mData.index = [datetime(x[0],x[1],1) for x in mData.index.get_values()]

clidesc_progress(base_path, 30)

"""
Calculates a monthly climatology
"""
clim = mData.groupby(mData.index.month).mean()


"""
calculates anomalies
"""
mData['anoms'] =  mData[['rain_24h']] - np.resize(clim.values, mData.shape)

clidesc_progress(base_path, 40)


"""
NOW READS THE Southern Oscillation Index from http://www.cgd.ucar.edu/cas/catalog/climind/SOI.signal.ascii
!!! NEEDS an internet connection
"""

try:
    soi = pd.read_table('http://www.cgd.ucar.edu/cas/catalog/climind/SOI.signal.ascii', sep='\s*', index_col=0, header=None, na_values=-99.9)
    clidesc_progress(base_path,50)
except:
    "! WARNING: Unable to read the SOI at http://www.cgd.ucar.edu/cas/catalog/climind/SOI.signal.ascii\n"

soi = soi.stack(dropna=False)

soi.index = [datetime(x[0],x[1],1) for x in soi.index.get_values()]

mData['soi'] = soi


"""
Calculates the 3 months rolling averages of the SOI and the Rainfall anomalies
"""
seasData = pd.rolling_mean(mData[['anoms','soi']], 3, min_periods=2)

total_data = len(seasData.dropna())

clidesc_progress(base_path, 60)

"""
Groups by month (season) and calculates R and p-value
"""
groups = seasData.groupby(seasData.index.month)

R = []; P =[]
for i in np.arange(1,13):
    ds = groups.get_group(i)
    ds = ds.dropna()
    r, p = pearsonr(ds['anoms'], ds['soi'])
    R.append(r)
    P.append(p)
R = np.array(R); P = np.array(P)

seasons = ['NDJ', 'DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND']

Rmax = np.max(np.abs(R)) + 0.1 * np.max(np.abs(R))

clidesc_progress(base_path, 70)

"""
The significance level is set at 90 % (alpha = 0.1)

set to 0.05 if wanted 95 % sig. level
"""
ppp = ( (P < 0.1) & (R > 0))
ppn = ( (P < 0.1) & (R < 0))

"""
Barplot of the seasonal correlations between the SOI and the seasonal rainfall anomalies
"""
f, ax =  plt.subplots(figsize=(6,6))

f.subplots_adjust(bottom=0.2, left=0.15)

ax.bar(np.arange(len(R))[R > 0], R[R > 0], color= 'coral', alpha=0.5, width=1, edgecolor='k')
ax.bar(np.arange(len(R))[R < 0], R[R < 0], color='steelblue', alpha=0.5, width=1, edgecolor='k')

ax.bar(np.arange(len(R))[ppp], R[ppp], color='coral', width=1, edgecolor='k', hatch='/')
ax.bar(np.arange(len(R))[ppn], R[ppn], color='steelblue', width=1, edgecolor='k', hatch='/')

ax.set_xticks(np.arange(0.5, len(R) + 0.5))
ax.set_xticklabels(seasons, fontsize=14, rotation=90)
[l.set_fontsize(14) for l in ax.get_yticklabels()]
ax.set_title('Correlation Rainfall <> SOI for {}\ncalculated with a total of {} seasons'.format(sName, total_data))
ax.set_xlabel('Season')
ax.set_ylabel("Pearson's R")
ax.set_ylim(-Rmax, Rmax)
f.savefig(os.path.join(base_path, 'Barplot_SoiSeasonalRainfall_WS.png'))

clidesc_progress(80)

if seaborn:
    """
    facet plot of the regressions between the SOI and the seasonal rainfall anomalies
    """
    f, axes = plt.subplots(nrows=4, ncols=3, figsize=(10,14))

    f.subplots_adjust(bottom=0.1)

    axes = axes.flatten()

    for i, m in enumerate(np.arange(1,13)):
        ax = axes[i]
        ds = groups.get_group(m)
        ds = ds.dropna()
        sb.regplot(ds['soi'], ds['anoms'], ax=ax, color='#000099')
        ax.set_title("{}, R = {:4.2f}".format(seasons[i],ds.corr().ix[1,0]))
        ax.set_xlabel('SOI')
        if m in [1,4,7,10]:
            ax.set_ylabel('anoms. (mm)')
        else:
            ax.set_ylabel('')
    f.savefig(os.path.join(base_path, 'Regplot_SoiSeasonalRainfall_WS.png'))

clidesc_progress(base_path, 100)

clidesc_close(base_path, conn)
