import os, sys
from datetime import datetime
from dateutil import parser
import psycopg2
import pandas as pd
import pandas.io.sql as psql
from matplotlib import pyplot as plt
import Image

###########################################################################
# Settings
dbhost = 'localhost'
#dbhost = 'clidesc.niwa.co.nz'

###########################################################################
# get the command line parameters
# we add some testing to the length of the passed parameters first
# that is in order to allow stand-alone non standard scripts to be developed
# (e.g. the ICU one ...)

if len(sys.argv) == 5:
    base_path = sys.argv[1] # base path is the path where the outputs, progress files and figures are saved
    stations = sys.argv[2] # list of stations, assumes string is passed, and comma is the separator
    from_date = parser.parse(sys.argv[3]) # from date: transform into a datetime object
    from_date = from_date.strftime('%Y-%m-%d') # and format correctly just in case the date wasnt entered YYYY-MM-DD
    to_date = parser.parse(sys.argv[4]) # to date: idem
    to_date = to_date.strftime('%Y-%m-%d')
    station_no = stations.split(',')[0] # assumes the first station is the 'primary' station

# Manage the progress file
progress_count = 0

###########################################################################
def clidesc_progress(base_path, percent):
    with open(os.path.join(base_path,'progress.txt'), 'w+') as f:
        f.write("%s".format(percent)
        f.close()

###########################################################################
def clidesc_open(base_path, database="clideDB", user="XXX", password="XXX", dbhost='localhost'):
    """
    Open the ClideDB database and the progress file

    Parameters
    ----------

    base_path : filesystem path
        The base path where all the outputs etc are dumped

    database : string
        The name of the Database (ClideDB usually)

    user : string
        The username

    password : string
        The passowrd

    dbhost : string
        The host server name ('localhost' if clide is accessed
        locally)

    Returns
    -------

    conn : db connection
        A database connection object as returned by psycopg2.connect()

    """
    clidesc_progress(base_path, 0)
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=dbhost)
        clidesc_progress(base_path, 1)
        return conn
    except:
        print('\n\nERROR!: Unable to establish the connection to the database\n\n')

################################################################
def clidesc_getColumns(conn, table):
    """
    Return the column names of a table

    Parameters
    ----------

    conn : the postgresql connection
    table : string
        the table (e.g. 'obs_daily', 'obs_subdaily')

    Returns
    -------
    columns : Pandas.DataFrame
        A Pandas.Series containing the column names

    Usage
    -----

    columns = clidesc_getColumns(conn, 'obs_subdaily')
    columns = clidesc_getColumns(conn, 'obs_daily')
    """

    query = "SELECT column_name FROM information_schema.columns WHERE table_name = '{}'".format(table)
    columns = psql.frame_query(query, conn)
    return columns

################################################################
def clidesc_stations(conn, stations):
    """
    Gets all the station details for a station number
    It opens the connection, reads the stations table
    station_no is a string, with stations separated by ','

    Parameters
    ----------

    conn : db connection
        Database connection object as returned by clidesc_open()

    stations : string
        The station or station list
        if several station should be passed as string, not list
        e.g. 'XXXXX, YYYYY, ZZZZZ'

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame object containing the station
        information
    """

    if isinstance(stations, str) and ',' in stations:
        stations = stations.replace(',','\',\'')

    # builds the query string
    query = """SELECT * FROM stations WHERE station_no IN ('%s') ORDER BY station_no""" % (stations)

    # get the table returned by the query as a pandas dataframe
    table = psql.frame_query(query, conn)
    return table

################################################################
def clidesc_getStationsByCountry(conn, country):
    """
    Gets all the station details for all stations in a given country code (single or vector).
    It opens the connection, reads the stations table
    country must be a string, with country codes (if more than one)
    separated by ','

    Parameters
    ----------

    conn : db connection
        A database connection object as returned by clides_open()

    country : string
        The two letters country identifier
        e.g. 'WS' for Samoa, 'FJ' for Fiji, ...

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame object containing the list of stations
        available for the country

    """

    if ',' in country:
        country = country.replace(',','\',\'')

    # builds the query string
    query = """SELECT * FROM stations WHERE country_code IN ('%s') ORDER BY country_code, station_no""" % ( country )
    # get the table returned by the query as a pandas dataframe
    table = psql.frame_query(query, conn)
    return table

################################################################
def clidesc_ObsDaily(conn, channels, stations, from_date, to_date):
    """
    returns the daily observations table for the requested stations, channels and date range.

    Parameters
    ----------

    conn : db connection
        A database connection object as returned by clides_open()

    channels : string
        The variable channels in the table

    stations : string
        The station or stations list

    from_date : string
        The starting date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    to_date : string
        The end date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame containing the data

    """

    # some string formatting on the stations if more than one
    if isinstance(stations, str) and ',' in stations:
        stations = stations.replace(',','\',\'')

    inputs = '%s::%s::%s::%s' % (channels, stations, from_date, to_date)

    query = """
    SELECT station_no, TO_CHAR(lsd, 'yyyy-mm-dd') as LSD,
    %s FROM obs_daily WHERE station_no IN ('%s') AND lsd >= TO_TIMESTAMP('%s', 'yyyy-mm-dd')
    AND lsd <= TO_TIMESTAMP('%s', 'yyyy-mm-dd') ORDER BY lsd""" % (channels, stations, from_date, to_date)

    # get the table returned by the query as a pandas dataframe
    try:
        table = psql.frame_query(query, conn)
        # the index of the pandas DataFrame is the 'lsd' field, correctly
        # cast to pandas datetime index and named 'timestamp'
        table.index = pd.to_datetime(table.lsd)
        table.index.name = 'timestamp'
        return table
    except:
        print('query failed for %s, was probably malformed' % (inputs))
        return None


################################################################
def clidesc_rain24h(conn, stations, from_date, to_date):
    """
    Utility function to read the rain_24h channel from the obs_daily table

    Parameters
    ----------

    conn : db connection
        A database connection object as returned by clides_open()

    stations : string
        The station or stations list

    from_date : string
        The starting date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    to_date : string
        The end date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame containing the data
    """
    return clidesc_ObsDaily(conn, 'rain_24h', stations, from_date, to_date)

################################################################
def clidesc_ObsSubDaily(conn, channels, stations, from_date, to_date):
    """
    Read channels for stations (stations) from the obs_subdaily table

    Parameters
    ----------

    conn : db connection
        A database connection object as returned by clides_open()

    channels : string
        The variable channels in the table

    stations : string
        The station or stations list

    from_date : string
        The starting date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    to_date : string
        The end date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame containing the data

    usage:
    table = clidesc_ObsSubDaily(clideDB, channels, stations, from_date, to_date )
    """

    inputs = '%s::%s::%s::%s' % (channels, stations, from_date, to_date)

    # some string formatting on the stations if more than one
    if isinstance(stations, str) and ',' in stations:
        stations = stations.replace(',','\',\'')

    # builds the query string
    query = """SELECT station_no
    , TO_CHAR(lsd, 'yyyy-mm-dd') as LSD
    , %s
    FROM obs_subdaily AS tab
    WHERE station_no IN ('%s')
    AND lsd >= TO_TIMESTAMP('%s', 'yyyy-mm-dd')
    AND lsd <= TO_TIMESTAMP('%s', 'yyyy-mm-dd')
    ORDER BY lsd""" % (channels, stations, from_date, to_date)

    # get the table returned by the query as a pandas dataframe
    try:
        table = psql.frame_query(query, conn)
        # the index of the pandas DataFrame is the 'lsd' field, correctly
        # cast to pandas datetime index and named 'timestamp'
        table.index = pd.to_datetime(table.lsd)
        table.index.name = 'timestamp'
        return table
    except:
        print('query failed for %s, was probably malformed' % (inputs))
        return None


################################################################
def clidesc_Obs(conn, table, channels, stations, from_date, to_date):
    """
    returns the given observations table for the requested stations, date range and columns
    depends on an open clidDB connection clideDB

    Parameters
    ----------

    conn : db connection
        A database connection object as returned by clides_open()

    table: string
        The table from which the observations are required, can be:
            + 'obs_daily'
            + 'obs_subdaily'

    channels : string
        The channel to retrieve, ex. 'wind_speed', 'rain_24h'

    stations : string
        The station(s), if more than one 'XXXXX, YYYYY'

    from_date : string
        The starting date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    to_date : string
        The end date in 'YYYY-MM-DD' format
        e.g. '2014-01-01'

    Returns
    -------

    table : Pandas.DataFrame
        A Pandas.DataFrame containing the data
    """

    # some string formatting on the stations if more than one
    if isinstance(stations, str) and ',' in stations:
        stations = stations.replace(',','\',\'')

    inputs = '%s::%s::%s::%s::%s' % (channels, table, stations, from_date, to_date)

    query = """SELECT station_no
    , TO_CHAR(lsd, 'yyyy-mm-dd') as LSD
    , %s
    FROM %s AS tab
    WHERE station_no IN ('%s')
    AND lsd >= TO_TIMESTAMP('%s', 'yyyy-mm-dd')
    AND lsd <= TO_TIMESTAMP('%s', 'yyyy-mm-dd')
    ORDER BY lsd""" % (channels, table, stations, from_date, to_date)

    # get the table returned by the query as a pandas dataframe
    try:
        table = psql.frame_query(query, conn)
        # the index of the pandas DataFrame is the 'lsd' field, correctly
        # cast to pandas datetime index and named 'datetime'
        table.index = pd.to_datetime(table.lsd)
        table.index.name = 'timestamp'
        return table
    except:
        print('query failed for %s, was probably malformed' % (inputs))
        return None


################################################################
# CLOSE
# Closes the connection && Frees all the resources on the driver

def clidesc_close(base_path, conn):
    """
    closes a clide connection

    Parameters
    ----------

    base_path : path
        The base path

    conn : db connection
        A database connection object as returned by clides_open()
    """
    clidesc_progress(base_path, 100)
    if conn.closed == 0:
        conn.close()
