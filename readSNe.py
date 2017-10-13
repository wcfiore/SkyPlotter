import os, urllib.request, time, stat, json, pprint
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u

def readSNe(URL, file_name, RA, DEC, ERR, pltRA, pltDEC, pltsize, markers, labels):
    
    if(os.path.isfile(file_name) == False):
        urllib.request.urlretrieve(URL, file_name)
        
    db_age = time.time() - os.stat(file_name)[stat.ST_MTIME]
    if(db_age > 43200):
        os.remove(file_name)
        urllib.request.urlretrieve(URL, file_name)
        print('***********************************')
        print('Existing Open Supernova Catalog file was out of date. New file downloaded and replaced existing file.')
        print('***********************************')
        print('')
        
    with open(file_name, 'r') as f:
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
                
            if((RA - ra) ** 2 + (DEC - dec) ** 2 < ERR ** 2):
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
                        dates = np.append(dates, data[i]['discoverdate'][0]['value'])
                    else:
                        dates = np.append(dates, data[i]['discoverdate'][0]['value'])
                else:
                    dates = np.append(dates, 'nan')
         
                
    pltRA = np.append(pltRA, RAs)
    pltDEC = np.append(pltDEC, DECs)
    pltsize = np.append(pltsize, np.full(len(names), 80))
    markers = np.append(markers, np.full(len(names), 'P'))
    labels = np.append(labels, np.full(len(names), 'supernova'))
                
    return names, RAs, DECs, dates, types, mags, hosts, pltRA, pltDEC, pltsize, markers, labels
