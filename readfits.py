from astropy.io import fits
import numpy as np
import os, urllib.request
import numpy as np

# This function reads downloads and data from fits files and sorts the sources by type
# It is called once per catalog, and requires some fine tuning based on 
# which catalog is being read

def readfits(URL, file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, marker, pltRA, pltDEC, srctype, pltflux, labels):
    
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
            return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, srctype, pltflux, labels
        elif(marker == 'neargalcat'):
            print('https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?tablehead=name%3D ' \
                  + 'neargalcat&Action=More+Options')
            print("Check the fields for 'name', 'ra', 'dec', 'bmag', 'distance', and 'morph_type'. " \
                  + "Limit results to 'no limit'. Select FITS output and press search. " \
                  + "The file must have the name 'neargalcat.fits' and must be located in " \
                  + "the same directory as this program.")
            names, RAs, DECs, bmag, dist, galtype = [], [], [], [], [], []
            return names, RAs, DECs, bmag, dist, galtype
        else:
            names, RAs, DECs, eflux, pflux, rshift = [], [], [], [], [], [], []
            return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, srctype, pltflux, labels
    
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
        
        for i in range(len(names)):
            if((classes[i] == 'psr') or (classes[i] == 'PSR')):
                labels.append('pulsar')
                srctype.append('psr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'pwn'):
                labels.append('psr wind nebula')
                srctype.append('pwn')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'snr'):
                labels.append('SNR')
                srctype.append('snr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'spp'):
                labels.append('SNR/PWN')
                srctype.append('spp')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'hmb'):
                labels.append('high-mass binary')
                srctype.append('hmb')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'bin'):
                labels.append('binary')
                srctype.append('bin')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'sfr'):
                labels.append('star-forming region')
                srctype.append('sfr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif((classes[i] == 'bll') or (classes[i] == 'bll-g') or (classes[i] == 'fsrq') or \
                 (classes[i] == 'bcu I') or (classes[i] == 'bcu II') or (classes[i] == 'bcu III')):
                labels.append('blazar')
                srctype.append('bzr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif((classes[i] == 'agn') or (classes[i] == 'bcu') or (classes[i] == 'AGN')):
                labels.append('AGN / active galaxy')
                srctype.append('agn')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'rdg'):
                labels.append('radio galaxy')
                srctype.append('rdg')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'rdg/bll'):
                labels.append('radio galaxy / BL Lac blazar')
                srctype.append('rzr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'gal'):
                labels.append('normal galaxy (or part)')
                srctype.append('gal')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'galclu'):
                labels.append('galaxy cluster')
                srctype.append('gcl')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif((classes[i] == 'nlsy1') or (classes[i] == 'sey')):
                labels.append('Seyfert galaxy')
                srctype.append('sey')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'nov'):
                labels.append('nova')
                srctype.append('nov')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'glc'):
                labels.append('globular cluster')
                srctype.append('glc')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif((classes[i] == 'css') or (classes[i] == 'ssrq')):
                labels.append('quasar')
                srctype.append('qsr')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            elif(classes[i] == 'sbg'):
                labels.append('starburst galaxy')
                srctype.append('sbg')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
            else:
                labels.append('unknown g-ray src')
                srctype.append('unk')
                pltRA.append(RAs[i])
                pltDEC.append(DECs[i])
                pltflux.append(eflux[i])
        mask1 = np.full(limit, False)
        mask2 = np.full(len(labels) - limit, True)
        mask = np.append(mask1, mask2)
        types = np.array(labels)[mask]
    else:
        dist = dist[mask]
        galtype = galtype[mask]   

    if((marker == 'ROSAT') or (marker == 'XMM')):
        return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, srctype, pltflux, labels
    elif(marker == 'neargalcat'):
        return names, RAs, DECs, bmag, dist, galtype
    else:
        return names, RAs, DECs, eflux, pflux, types, rshift, pltRA, pltDEC, srctype, pltflux, labels