from astropy.io import fits
import numpy as np
import os, urllib.request
import numpy as np

# This function reads downloads and data from fits files and sorts the sources by type
# It is called once per catalog, and requires some fine tuning based on 
# which catalog is being read

def readfits(URL, file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, marker, psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux):
    
    # Check if the catalog exists already. If not, download it from the website and save it:
    if((os.path.isfile(file_name) == False) and (URL != 'nope')):
        urllib.request.urlretrieve(URL, file_name)
    
    if((os.path.isfile(file_name) == False) and (URL == 'nope')):
        print('Could not find ' + marker + ' Catalog')
        names, RAs, DECs, eflux, pflux, srctype, rshift = [], [], [], [], [], [], []
        return names, RAs, DECs, eflux, pflux, srctype, rshift
    
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
    for i in range(len(names)):
        if(((RAs[i] - RA) ** 2 + (DECs[i] - DEC) ** 2) > (ERR ** 2)):
        #if not((RA1 <= RAs[i] <= RA2) and (DEC1 <= DECs[i] <= DEC2)):
            names[i] = 'bad'
            RAs[i] = 1000.0
            DECs[i] = 1000.0
            if(marker != 'neargalcat'): 
                eflux[i] = -15.0               
                pflux[i] = -15.0
                rshift[i] = 'bad'
                classes[i] = 'bad'
            if(marker == 'neargalcat'):
                dist[i] = -15.0
                galtype[i] = 'bad'
        if(marker != 'neargalcat'):
            if(np.isnan(pflux[i]) == True):
                pflux[i] = 0.0
    
    names = list(filter(lambda a: a != 'bad', names))
    RAs = list(filter(lambda a: a < 900.0, RAs))
    DECs = list(filter(lambda a: a < 900.0, DECs))
    if(marker != 'neargalcat'):
        eflux = list(filter(lambda a: a >= -10.0, eflux))
        pflux = list(filter(lambda a: a >= -10.0, pflux))
        rshift = list(filter(lambda a: a != 'bad', rshift))
        classes = list(filter(lambda a: a != 'bad', classes))
        srctype = np.zeros(len(names), dtype = '52str')
        for i in range(len(names)):
            if((classes[i] == 'psr') or (classes[i] == 'PSR')):
                srctype[i] = 'pulsar'
                psrRA.append(RAs[i])
                psrDEC.append(DECs[i])
                psreflux.append(eflux[i])
            elif(classes[i] == 'pwn'):
                srctype[i] = 'psr wind nebula'
                pwnRA.append(RAs[i])
                pwnDEC.append(DECs[i])
                pwneflux.append(eflux[i])
            elif(classes[i] == 'snr'):
                srctype[i] = 'SNR'
                snrRA.append(RAs[i])
                snrDEC.append(DECs[i])
                snreflux.append(eflux[i])
            elif(classes[i] == 'spp'):
                srctype[i] = 'SNR/PWN'
                sppRA.append(RAs[i])
                sppDEC.append(DECs[i])
                sppeflux.append(eflux[i])
            elif(classes[i] == 'hmb'):
                srctype[i] = 'high-mass binary'
                hmbRA.append(RAs[i])
                hmbDEC.append(DECs[i])
                hmbeflux.append(eflux[i])
            elif(classes[i] == 'bin'):
                srctype[i] = 'binary'
                binRA.append(RAs[i])
                binDEC.append(DECs[i])
                bineflux.append(eflux[i])
            elif(classes[i] == 'sfr'):
                srctype[i] = 'star-forming region'
                sfrRA.append(RAs[i])
                sfrDEC.append(DECs[i])
                sfreflux.append(eflux[i])
            elif((classes[i] == 'bll') or (classes[i] == 'bll-g') or (classes[i] == 'fsrq') or (classes[i] == 'bcu I') or (classes[i] == 'bcu II') or (classes[i] == 'bcu III')):
                srctype[i] = 'blazar'
                bzrRA.append(RAs[i])
                bzrDEC.append(DECs[i])
                bzreflux.append(eflux[i])
            elif((classes[i] == 'agn') or (classes[i] == 'bcu') or (classes[i] == 'AGN')):
                srctype[i] = 'AGN / active galaxy'
                agnRA.append(RAs[i])
                agnDEC.append(DECs[i])
                agneflux.append(eflux[i])
            elif(classes[i] == 'rdg'):
                srctype[i] = 'radio galaxy'
                rdgRA.append(RAs[i])
                rdgDEC.append(DECs[i])
                rdgeflux.append(eflux[i])
            elif(classes[i] == 'rdg/bll'):
                srctype[i] = 'radio galaxy / BL Lac blazar'
                rgbRA.append(RAs[i])
                rgbDEC.append(DECs[i])
                rgbeflux.append(eflux[i])
            elif(classes[i] == 'gal'):
                srctype[i] = 'normal galaxy (or part)'
                galRA.append(RAs[i])
                galDEC.append(DECs[i])
                galeflux.append(eflux[i])
            elif(classes[i] == 'galclu'):
                srctype[i] = 'galaxy cluster'
                gclRA.append(RAs[i])
                gclDEC.append(DECs[i])
                gcleflux.append(eflux[i])
            elif((classes[i] == 'nlsy1') or (classes[i] == 'sey')):
                srctype[i] = 'Seyfert galaxy'
                seyRA.append(RAs[i])
                seyDEC.append(DECs[i])
                seyeflux.append(eflux[i])
            elif(classes[i] == 'nov'):
                srctype[i] = 'nova'
                novRA.append(RAs[i])
                novDEC.append(DECs[i])
                noveflux.append(eflux[i])
            elif(classes[i] == 'glc'):
                srctype[i] = 'globular cluster'
                glcRA.append(RAs[i])
                glcDEC.append(DECs[i])
                glceflux.append(eflux[i])
            elif((classes[i] == 'css') or (classes[i] == 'ssrq')):
                srctype[i] = 'quasar'
                qsrRA.append(RAs[i])
                qsrDEC.append(DECs[i])
                qsreflux.append(eflux[i])
            elif(classes[i] == 'sbg'):
                srctype[i] = 'starburst galaxy'
                sbgRA.append(RAs[i])
                sbgDEC.append(DECs[i])
                sbgeflux.append(eflux[i])
            else:
                srctype[i] = 'unknown g-ray src'
                unkRA.append(RAs[i])
                unkDEC.append(DECs[i])
                unkeflux.append(eflux[i])
            
    else:
        dist = list(filter(lambda a: a >= -10.0, dist))
        galtype = list(filter(lambda a: a != 'bad', galtype))    

    if((marker == 'ROSAT') or (marker == 'XMM')):
        return names, RAs, DECs, eflux, pflux, srctype, rshift, agnRA, agnDEC, agneflux
    elif(marker == 'neargalcat'):
        return names, RAs, DECs, bmag, dist, galtype
    else:
        return names, RAs, DECs, eflux, pflux, srctype, rshift, psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux