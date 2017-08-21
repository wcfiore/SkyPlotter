from astropy.io import fits
import numpy as np
import os, urllib.request
import numpy as np


def readTeGeV(file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, pltRA, pltDEC, srctype, pltflux, labels):
    
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
    for i in range(len(names)):
        if(((RAs[i] - RA) ** 2 + (DECs[i] - DEC) ** 2) > (ERR ** 2)):
        #if not((RA1 <= RAs[i] <= RA2) and (DEC1 <= DECs[i] <= DEC2)):
            names[i] = 'bad'
            RAs[i] = 1000.0
            DECs[i] = 1000.0
            classes[i] = 'bad'
            eflux[i] = -15.0
            pflux[i] = -15.0
            rshift[i] = 'bad'
    
    names = list(filter(lambda a: a != 'bad', names))
    RAs = list(filter(lambda a: a < 900.0, RAs))
    DECs = list(filter(lambda a: a < 900.0, DECs))
    classes = list(filter(lambda a: a != 'bad', classes))
    eflux = list(filter(lambda a: a >= 0.0, eflux))
    pflux = list(filter(lambda a: a >= 0.0, pflux))
    rshift = list(filter(lambda a: a != 'bad', rshift))
    
    for i in range(len(names)):
        if(classes[i] == 'PWN/SNR'):
            labels.append('SNR/PWN')
            srctype.append('pwr')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif((classes[i] == 'HBL') or (classes[i] == 'LBL') or (classes[i] == 'IBL') or (classes[i] == 'Blazar') or (classes[i] == 'FSRQ')):
            labels.append('blazar')
            srctype.append('bzr')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'SNR'):
            labels.append('SNR')
            srctype.append('snr')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'Starburst'):
            labels.append('starburst')
            srctype.append('sbs')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'UNID'):
            labels.append('unknown g-ray src')
            srctype.append('unk')
            unkRA.append(RAs[i])
            unkDEC.append(DECs[i])
            unkeflux.append(eflux[i])
        elif(classes[i] == 'XRB'):
            labels.append('XRB')
            srctype.append('xrb')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'AGN'):
            labels.append('AGN / active galaxy')
            srctype.append('agn')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'SNR/MC'):
            labels.append('SNR / molecular cloud')
            srctype.append('smc')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif((classes[i] == 'PWN') or (classes[i] == 'PWN/UNID')):
            labels.append('pulsar wind nebula')
            srctype.append('pwn')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'Superbubble'):
            labels.append('superbubble')
            srctype.append('sbb')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'FRI'):
            labels.append('FRI')
            srctype.append('fri')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'BIN'):
            labels.append('binary')
            srctype.append('bin')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'WR/MSC'):
            labels.append('Wolf-Rayet star')
            srctype.append('wrs')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'SNR/SHELL'):
            labels.append('SNR / Shell')
            srctype.append('sns')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
        elif(classes[i] == 'GC'):
            labels.append('globular cluster')
            srctype.append('glc')
            pltRA.append(RAs[i])
            pltDEC.append(DECs[i])
            pltflux.append(eflux[i])
            
    return names, RAs, DECs, eflux, pflux, labels, rshift, pltRA, pltDEC, srctype, pltflux, labels