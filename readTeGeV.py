from astropy.io import fits
import numpy as np
import os
import numpy as np


def readTeGeV(file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, pltRA, pltDEC, pltsize, labels, markers):
    
    if(os.path.isfile(file_name) == False):
        print('***********************************')
        print('Could not find catalog file for TeGeVCat')
        print('Download the file at the URL: http://www.asdc.asi.it/tgevcat/')
        print("Make sure the units for RA and DEC are in degrees, flux is in E-12 cm2/s, and distance is in redshift." +\
              "These are changed with the dropdown menus at the top of the page. Scroll all the way down and make sure" +\
              "the only fields that are checked are 'TEV NAME', 'TYPE', 'RA (J2000)', DEC (J2000)', 'INTEGRAL FLUX', and" +\
              "'DISTANCE'. Click on 'Update Table Columns'. Scrolling back up, click on 'Raw Text Format'. Copy and paste" +\
              "the contents of the page into a text file. The file must have the name 'TeGeVCat.dat' and must be located" +\
              "in the same directory as this program.")
        print('***********************************')
    
    # Read data from file:
    names, classes, RAs, DECs, pflux, rshift = np.loadtxt(file_name, dtype = 'S20', delimiter = ' | ', skiprows = 1, \
                                                          usecols = (1,2,3,4,5,6), unpack = True)
    
    names = names.astype('str')
    classes = classes.astype('str')
    RAs = RAs.astype('float')
    DECs = DECs.astype('float')
    for i in range(len(pflux)):
        if(pflux[i] == b'-'):
            pflux[i] = b'0'
    pflux = pflux.astype('float')
    pflux = pflux * (10 ** -12)
    eflux = np.zeros(len(names)) 
    rshift = rshift.astype('str')
    
    RAs[RAs < RA1] += 360
    RAs[RAs > RA2] -= 360
        
    # We want to only plot sources that are within the error circle:
    mask = ((RAs - RA) ** 2 + (DECs - DEC) ** 2) <= (ERR ** 2)
    
    names = names[mask]
    RAs = RAs[mask]
    DECs = DECs[mask]
    eflux = eflux[mask]
    pflux = pflux[mask]
    rshift = rshift[mask]
    classes = classes[mask]
    
    for i in range(len(names)):
        names[i] = names[i].replace('TeV', 'TeGeV')
    
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
    
    pltsize = np.append(pltsize, 20 + np.multiply(pltflux, 10 ** 13))
    markers = np.append(markers, np.full(len(RAs), '.'))
 
    
    return names, RAs, DECs, eflux, pflux, labels, rshift, pltRA, pltDEC, pltsize, labels, markers