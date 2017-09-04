from astropy.io import fits
import numpy as np
import os, urllib.request
import numpy as np

# This function reads downloads and data from fits files and sorts the sources by type
# It is called once per catalog, and requires some fine tuning based on 
# which catalog is being read

def readfits(URL, file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, marker, pltRA, pltDEC, pltsize, labels, markers):
    
    # Check if the catalog exists already. If not, download it from the website and save it:
    if((os.path.isfile(file_name) == False) and (URL != 'nope')):
        urllib.request.urlretrieve(URL, file_name)
    
    if((os.path.isfile(file_name) == False) and (URL == 'nope')):
        print('***********************************')
        print('Could not find catalog file for ' + marker + '.')
        if((marker == 'ROSAT') or (marker == 'XMM')):
            if(marker == 'ROSAT'):
                print('Download the file at the URL: https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?' \
                      + 'tablehead=name%3Drosnepagn&Action=More+Options')
                print("Check the fields for 'name', 'ra', 'dec', 'flux_corr', and 'redshift'. " \
                + "Limit results to 'no limit'. Select FITS output and press search. " \
                      + "The file must have the name 'ROSAT.fits' and must be located in the same directory as this program.")
            else:
                print('Download the file at the URL: https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?' \
                      + 'tablehead=name%3Dcaixa&Action=More+Options')
                print("Check the fields for 'name', 'ra', 'dec', 'hb_flux', and 'redshift'. " \
                      + "Limit results to 'no limit'. Select FITS output and press search. " \
                      + "The file must have the name 'CAIXA_XMM.fits' and must be located in " \
                      + "the same directory as this program.")
            print('***********************************')
            names, RAs, DECs, eflux, pflux, rshift = [], [], [], [], [], [], []
            return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, srctype, pltsize, labels, markers
        elif(marker == 'neargalcat'):
            print('https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?tablehead=name%3D' \
                  + 'neargalcat&Action=More+Options')
            print("Check the fields for 'name', 'ra', 'dec', 'bmag', 'distance', and 'morph_type'. " \
                  + "Limit results to 'no limit'. Select FITS output and press search. " \
                  + "The file must have the name 'neargalcat.fits' and must be located in " \
                  + "the same directory as this program.")
            names, RAs, DECs, bmag, dist, galtype = [], [], [], [], [], []
            return names, RAs, DECs, bmag, dist, galtype, pltRA, pltDEC, pltsize, labels, markers
        else:
            names, RAs, DECs, eflux, pflux, rshift = [], [], [], [], [], [], []
            return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, pltsize, labels, markers
    
    # Read data from file:
    hdulist = fits.open(file_name)
    tbdata = hdulist[1].data
    names = tbdata.field(0)
    if(marker == '3FGL'):
        RAs = tbdata.field(1)
        DECs = tbdata.field(2)
        classes = tbdata.field(73)
        eflux = tbdata.field(19)
        pflux = tbdata.field(17)
        rshift = np.zeros(len(names))
        rshift = rshift.astype('str')
    if(marker == '2FHL'):
        RAs = tbdata.field(1)
        DECs = tbdata.field(2)
        classes = tbdata.field(34)
        eflux = tbdata.field(16)
        pflux = tbdata.field(14)
        rshift = tbdata.field(35)
        rshift = rshift.astype('str')
    if(marker == '2FAV'):
        for i in range(len(names)):
            names[i] = '2FAV ' + names[i]
        RAs = tbdata.field(2)
        DECs = tbdata.field(3)
        classes = tbdata.field(13)
        eflux = np.zeros(len(names))
        pflux = np.zeros(len(names))
        rshift = np.zeros(len(names))
        rshift = rshift.astype('str')
    if(marker == 'ROSAT'):
        RAs = tbdata.field(1)
        DECs = tbdata.field(2)
        classes = np.full(len(names), 'AGN')
        eflux = tbdata.field(3)
        pflux = np.zeros(len(names))
        rshift = tbdata.field(4)
        rshift = rshift.astype('str')
    if(marker == 'XMM'):
        RAs = tbdata.field(1)
        DECs = tbdata.field(2)
        classes = np.full(len(names), 'AGN')
        eflux = tbdata.field(3)
        pflux = np.zeros(len(names))
        rshift = tbdata.field(4)
        rshift = rshift.astype('str')
    if(marker == 'neargalcat'):
        RAs = tbdata.field(1)
        DECs = tbdata.field(2)
        bmag = tbdata.field(3)
        dist = tbdata.field(4)
        galtype = tbdata.field(5)
    
    RAs[RAs < RA1] += 360
    RAs[RAs > RA2] -= 360
        
    # We want to only plot sources that are within the error circle:
    mask = ((RAs - RA) ** 2 + (DECs - DEC) ** 2) <= (ERR ** 2)
    
    names = names[mask]
    RAs = RAs[mask]
    DECs = DECs[mask]
    if(marker != 'neargalcat'):
        eflux = eflux[mask]
        pflux = pflux[mask]
        rshift = rshift[mask]
        classes = classes[mask]
        
        limit = len(labels)
        
        pltflux = []
        
        for i in range(len(names)):
            if((classes[i] == 'psr') or (classes[i] == 'PSR')):
                labels = np.append(labels, 'pulsar')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'pwn'):
                labels = np.append(labels, 'psr wind nebula')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'snr'):
                labels = np.append(labels, 'supernova remnant')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'spp'):
                labels = np.append(labels, 'SNR / PWN')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'hmb'):
                labels = np.append(labels, 'high-mass binary')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'bin'):
                labels = np.append(labels, 'binary')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'sfr'):
                labels = np.append(labels, 'star-forming region')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif((classes[i] == 'bll') or (classes[i] == 'bll-g') or (classes[i] == 'fsrq') or \
                 (classes[i] == 'bcu I') or (classes[i] == 'bcu II') or (classes[i] == 'bcu III')):
                labels = np.append(labels, 'blazar')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif((classes[i] == 'agn') or (classes[i] == 'bcu') or (classes[i] == 'AGN')):
                labels = np.append(labels, 'active galaxy / AGN')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'rdg'):
                labels = np.append(labels, 'radio galaxy')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'rdg/bll'):
                labels = np.append(labels, 'radio galaxy / BL Lac blazar')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'gal'):
                labels = np.append(labels, 'normal galaxy (or part), gamma ray source')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'galclu'):
                labels = np.append(labels, 'galaxy cluster')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif((classes[i] == 'nlsy1') or (classes[i] == 'sey')):
                labels = np.append(labels, 'Seyfert galaxy')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'nov'):
                labels = np.append(labels, 'nova')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'glc'):
                labels = np.append(labels, 'globular cluster')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif((classes[i] == 'css') or (classes[i] == 'ssrq')):
                labels = np.append(labels, 'quasar')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            elif(classes[i] == 'sbg'):
                labels = np.append(labels, 'starburst galaxy')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
            else:
                labels = np.append(labels, 'unassociated gamma ray source')
                pltRA = np.append(pltRA, RAs[i])
                pltDEC = np.append(pltDEC, DECs[i])
                pltflux = np.append(pltflux, eflux[i])
        mask1 = np.full(limit, False)
        mask2 = np.full(len(labels) - limit, True)
        mask = np.append(mask1, mask2)
        types = np.array(labels)[mask]
        pltsize = np.append(pltsize, 20 + np.multiply(pltflux, 10 ** 13))
        markers = np.append(markers, np.full(len(RAs), '.'))
        
    else:
        dist = dist[mask]
        galtype = galtype[mask]
        pltsize = np.append(pltsize, 80 - dist * 2)
        labels = np.append(labels, np.full(len(RAs), 'nearby galaxy'))
        pltRA = np.append(pltRA, RAs)
        pltDEC = np.append(pltDEC, DECs)
        markers = np.append(markers, np.full(len(RAs), 'D'))
        
    if((marker == 'ROSAT') or (marker == 'XMM')):
        return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, pltsize, labels, markers
    elif(marker == 'neargalcat'):
        return names, RAs, DECs, bmag, dist, galtype, pltRA, pltDEC, pltsize, labels, markers
    else:
        return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, pltsize, labels, markers