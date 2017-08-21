from astropy.time import Time
import sys, os, urllib.request, time, stat
import numpy as np
import sqlite3
import math


def readFAVA(RA, DEC, ERR, start, stop, RA1, RA2, DEC1, DEC2):
    URL = 'http://slac.stanford.edu/~kocevski/FAVA/weekly/P8R2_SOURCE_V6/db/fava_flares.db'
    filename = './fava_flares.db'
    
    if(os.path.isfile(filename) == False):
        urllib.request.urlretrieve(URL, filename)
        
    db_age = time.time() - os.stat(filename)[stat.ST_MTIME]
    if(db_age > 604800):
        os.remove(filename)
        urllib.request.urlretrieve(URL, filename)
    
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
        if(RAs[i] < RA1):
            RAs[i] += 360
        elif(RAs[i] > RA2):
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

    mask = (((RAs - RA) ** 2 + (DECs - DEC) ** 2) <= (ERR ** 2)) & (t2 > start) & (t1 < stop)
    
    flareID = flareID[mask]
    RAs = RAs[mask]
    DECs = DECs[mask]
    t1 = t1[mask]
    t2 = t2[mask]
    leflux = leflux[mask]
    heflux = heflux[mask]
    
    names = np.zeros(len(flareID), dtype = 'S30')
    for i in range(len(names)):
        names[i] = 'FAVA Flare ' + flareID[i]
    srctype = np.zeros(len(flareID), dtype = 'S20')
    for i in range(len(srctype)):
        srctype[i] = 'FAVA Flare'
    
    return names, RAs, DECs, srctype, t1, t2, leflux, heflux