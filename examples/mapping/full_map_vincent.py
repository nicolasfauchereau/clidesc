import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import vincent
import folium
import pandas as pd

stations = pd.read_csv('../../data/stations_open_1950.csv')

Samoa = folium.Map(location=[-13.9, -171.75], width=2000, height=1000, zoom_start=10, tiles='Mapbox', API_key='nicolasf.ic0ebom5')

x = np.random.randn(len(stations))

for i in range(len(stations)): 
    dat = stations.ix[i]
    val = x[i]
    print(val)
    lat = dat['latitude']
    lon = dat['longitude']
    name = dat['name_primary']
    dat = dat[['station_no','name_primary','start_date','end_date']]
    dat = pd.DataFrame(dat)
    #text = "<!DOCTYPE html> <html> <body> " + dat.to_html(na_rep=' ', header=False, index=False).replace('\n','') + " </body> </html>"
    text = "NAME: <b>%s</b><br>\
            LAT: %4.2f<br>LON: %6.2f<br>\
            VALUE: %4.2f" % (name, lat, lon, val)
    #text = dat.to_html(na_rep=' ', header=False, index=False).replace('\n','')
    if val < 0: 
        Samoa.circle_marker(location=[lat, lon], fill_color='#0000FF', radius=-val*1500, line_color=None, popup=text)
    else: 
        Samoa.circle_marker(location=[lat, lon], fill_color='#FF0000', radius=val*1500, line_color=None, popup=text)

Samoa.create_map(path='Samoa.html')                         
