#!/opt/anaconda/bin/python
# coding=utf-8

# WindFitting.py

# PROJECT: Integrating climate change risks in agriculture and health sectors in Samoa
# Author: Nicolas Fauchereau, NIWA
# Date: August 2014
# can test using: 
# `./WindFitting.py base_path stations from_date to_date` 

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
print("Programme: WindFitting.py\n")

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
    sName = station['name_primary'][0]
    # get the start date
    sDate = station['start_date'][0]

### ===========================================================================
# DATA SETUP
### ===========================================================================

if local:
    # if local expects this file in the same directory
	iFile = '../data/table_obs_subdaily.csv'
	iData = pd.read_csv(iFile, index_col=0)
else:
    # loads the data from clide
    iData = clidesc_ObsSubDaily(conn, 'wind_speed', stations, from_date, to_date)

iData.sort_index(in_place=True)

"""
get rid of aberrant values, might want to change that 
"""

iData['wind_speed'][data['wind_speed'] >= 50] = np.nan
iData['wind_speed'][data['wind_speed'] < 0] = np.nan




# saves the figure in png (dpi = 200)
f.savefig(os.path.join(base_path,'drought_monitoring_{}days_{}.png'.format(window, sName)), dpi=200)

clidesc_close(base_path, conn)
