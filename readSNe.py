import os
import urllib2
import time
import stat
import json
import pprint
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u

def readSNe(parameters):
    URL = 'https://raw.githubusercontent.com/astrocatalogs/supernovae/master/output/catalog.json'
    filename = 'catalog.json'

    if not os.path.isfile(filename):
        with open(filename, "wb") as f:
            f.write(urllib2.urlopen(URL).read())
        
    db_age = time.time() - os.stat(filename)[stat.ST_MTIME]
    if(db_age > 43200):
        os.remove(filename)
        with open(filename, "wb") as f:
            f.write(urllib2.urlopen(URL).read())
        print('***********************************')
        print('Existing Open Supernova Catalog file was out of date. New file downloaded and replaced existing file.')
        print('***********************************')
        print('')
        
    with open(filename, 'r') as f:
        data = json.load(f)
    
    names = np.array([])
    RAs = np.array([])
    DECs = np.array([])
    dates = np.array([])
    types = np.array([])
    mags = np.array([])
    hosts = np.array([])
    
    for i in range(len(data)):
        if 'ra' in data[i]:
            ra = data[i]['ra'][0]['value']
            ra_list = ra.split(":")
            ra_list.reverse()
            
            ra = 0
            
            for j, dt in enumerate(ra_list):
                ra += ((float(dt) * (60 ** j)) / (60 * 60 * 24)) * 360
            
            dec = data[i]['dec'][0]['value']
            dec_list = dec.split(":")
            
            dec = 0
            
            for k, dt in enumerate(dec_list):
                dec += float(dt) / (60 ** k)
                
            if((parameters["RA"] - ra) ** 2 + (parameters["DEC"] - dec) ** 2 <
                       parameters["ERR"] ** 2):
                names = np.append(names, data[i]['name'])
                RAs = np.append(RAs, ra)
                DECs = np.append(DECs, dec)
                if 'claimedtype' in data[i]:
                    types = np.append(types, data[i]['claimedtype'][0]['value'])
                else:
                    types = np.append(types, 'nan')

                if 'maxappmag' in data[i]:
                    mags = np.append(mags, float(data[i]['maxappmag'][0]['value']))
                else:
                    mags = np.append(mags, np.nan)

                if 'host' in data[i]:
                    hosts = np.append(hosts, data[i]['host'][0]['value'])
                else:
                    hosts = np.append(hosts, 'nan')
                
                if 'discoverdate' in data[i]:
                    if(len(data[i]['discoverdate'][0]['value']) != 4):
                        dates = np.append(dates, data[i]['discoverdate'][0]['value'].replace('/', '-'))
                    else:
                        dates = np.append(dates, data[i]['discoverdate'][0]['value'].replace('/', '-'))
                else:
                    dates = np.append(dates, 'nan')

    dt = np.dtype([
        ('Name', "S50"),
        ('RA', np.float),
        ('Dec', np.float),
        ('Discovery Date', "S50"),
        ('Claimed Type', "S50"),
        ("Max Apparent Magnitude", np.float),
        ("Host", "S50"),
        ("size", np.float)
    ])

    dates = Time(dates, format="iso")
    dates.out_subfmt= "date"

    mask = dates > parameters["start"]

    table = np.zeros_like(names[mask], dtype=dt)

    for i in range(len(names[mask])):
        table[i] = np.array(
            (names[mask][i], RAs[mask][i], DECs[mask][i], dates[mask][i].iso,
             types[mask][i], mags[mask][i], hosts[mask][i], 80), dtype=dt)

    table = np.sort(table, order=['Discovery Date'], axis=0)[::-1].view()

    SNe_dict = {
        "data": table,
        "message_1": "SUPERNOVAE:",
        "message_2": 'Note: RA and DEC are given in degrees.',
        "print_mask": ["Name", "RA", "Dec", "Discovery Date", "Claimed Type",
                       "Max Apparent Magnitude", "Host"],
        "color": "brown",
        "label": "Supernovae",
        "marker": "P"
    }
    return SNe_dict
