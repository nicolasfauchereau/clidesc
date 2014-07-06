import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import Image

################################################################
def make_thumbnail(srcfile, thumbfile, height, width):
    with Image.open(srcfile) as im:
        im.thumbnail((width, height), Image.ANTIALIAS)
        im.save(thumbfile)

################################################################
def cm2inch(*tupl):
    """
    A little function that converts cm in inches
    It is used in 'clidesc_Figure'
    """
    inch = 2.54
    if type(tupl[0]) == tuple:
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple()

################################################################
def clidesc_Figure(size='A4'):
    """
    Initializes figures (f) and axes (ax) with correct
    figure size and dpi value for:
    'A4' (default)
    'A5'
    '16/12in'
    """
    if size == 'A4':
        figsize = cm2inch((29.7,21.0))
        f, ax = plt.subplots(figsize=figsize, dpi=300)
    elif size == 'A5':
        figsize = cm2inch((29.7,21.0))
        f, ax = plt.subplots(figsize=figsize, dpi=150)
    elif size == '16/12in':
        figsize = cm2inch((16,12))
        f, ax = plt.subplots(figsize=figsize, dpi=75)
    return f, ax


def conform_calendar(df, freq='D'):
    pass

################################################################
def calc_monthly_stat(df, min_periods = 0.7, stat = 'mean'):
    """
    calc_monthly_stat(df, min_periods = 0.7, stat = 'mean'):
    """
    pass

################################################################
def calc_daily_stat(df, min_periods = 0.7, stat = 'mean'):
    """
    calc_monthly_stat(df, min_periods = 0.7, stat = 'mean'):
    """
    pass
