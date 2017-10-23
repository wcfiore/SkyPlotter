from astropy.time import Time
import sys
import os
import urllib2
import time
import stat
import numpy as np
import sqlite3

def readFAVA(parameters):
    URL = 'http://slac.stanford.edu/~kocevski/FAVA/weekly/P8R2_SOURCE_V6/db/fava_flares.db'
    filename = './fava_flares.db'
    
    if not os.path.isfile(filename):
        with open(filename, "wb") as f:
            f.write(urllib2.urlopen(URL).read())
        
    db_age = time.time() - os.stat(filename)[stat.ST_MTIME]
    if(db_age > 604800):
        os.remove(filename)
        with open(filename, "wb") as f:
            f.write(urllib2.urlopen(URL).read())
        print'***********************************'
        print'Existing FAVA database file was out of date. New file downloaded and replaced existing file.'
        print'***********************************'
        print''
    
    conn = sqlite3.connect('fava_flares.db')
    cursor = conn.execute("SELECT flareID, num, best_ra, best_dec, tmin, tmax, le_flux, he_flux from flares")
    
    flareID = []
    num = []
    RAs = []
    DECs = []
    t1 = []
    t2 = []
    leflux = []
    heflux = []
    
    for row in cursor:
        flareID = np.append(flareID, row[0])
        num = np.append(num, row[1])
        RAs = np.append(RAs, row[2])
        DECs = np.append(DECs, row[3])
        t1 = np.append(t1, row[4])
        t2 = np.append(t2, row[5])
        leflux = np.append(leflux, row[6])
        heflux = np.append(heflux, row[7])
    
    conn.close()

    RAs = RAs.astype('float')
    for i in range(len(RAs)):
        if(RAs[i] < parameters["RA1"]):
            RAs[i] += 360
        elif(RAs[i] > parameters["RA2"]):
            RAs[i] -= 360
    
    DECs = DECs.astype('float')
    
    t1 = t1.astype('float')
    t2 = t2.astype('float')
    
    t1 = t1 + 978307200
    t2 = t2 + 978307200
    
    t1 = Time(t1, format = 'unix', scale = 'utc')
    t2 = Time(t2, format = 'unix', scale = 'utc')
    
    leflux = leflux.astype('float')
    heflux = heflux.astype('float')
    
    # We want to only plot sources that are within the error circle:
    
    mask = (
        (((RAs - parameters["RA"]) ** 2 + (DECs - parameters["DEC"]) ** 2)
         <= (parameters["ERR"] ** 2))
        & (t2 > parameters["start"]) & (t1 < parameters["stop"]))

    
    names = np.zeros(len(flareID), dtype = 'S30')
    for i in range(len(names)):
        names[i] = 'FAVA Flare ' + flareID[i]

    dt = np.dtype([
        ('Name', "S50"),
        ('Flare ID', "S50"),
        ('RA', np.float),
        ('Dec', np.float),
        ('Start Time', "S50"),
        ('Stop Time', "S50"),
        ('Low Energy Flux', np.float),
        ("High Energy Flux", np.float),
        ("size", np.float)
    ])

    table = np.zeros_like(names[mask], dtype=dt)

    for i in range(len(names[mask])):
        table[i] = np.array((names[mask][i], flareID[mask][i],
                        RAs[mask][i], DECs[mask][i],
                        t1[mask][i].iso, t2[mask][i].iso,
                        leflux[mask][i], heflux[mask][i],
                        60),
                       dtype=dt)

    table = np.sort(table, order=['Start Time'], axis=0)[::-1].view()

    FAVA_dict = {
        "data": table,
        "message_1": 'FAVA FLARES:',
        "message_2": "Note: RA and DEC are given in degrees. LE Flux is "
                     "100-800 MeV, HE Flux is 0.8-300 GeV. Fluxes are given "
                     "in ph/cm^2/s.",
        "print_mask": ["Name", "RA", "Dec", "Start Time", "Stop Time",
                       "Low Energy Flux", "High Energy Flux"],
        "color": 'lightseagreen',
        "label": "FAVA flare",
        "marker": "X"
    }
    
    return FAVA_dict