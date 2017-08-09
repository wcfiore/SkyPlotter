from astropy.io import fits
import numpy as np
import os, urllib.request
import numpy as np


def readTeGeV(file_name, RA, DEC, ERR, RA1, RA2, DEC1, DEC2, sppRA, sppDEC, sppeflux, bzrRA, bzrDEC, bzreflux, snrRA, snrDEC, snreflux, stbRA, stbDEC, stbeflux, unkRA, unkDEC, unkeflux, xrbRA, xrbDEC, xrbeflux, agnRA, agnDEC, agneflux, snmRA, snmDEC, snmeflux, pwnRA, pwnDEC, pwneflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, binRA, binDEC, bineflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, glcRA, glcDEC, glceflux):
    
    # Read data from file:
    names, classes, RAs, DECs, pflux, rshift = np.loadtxt(file_name, dtype = 'S20', delimiter = ' | ', skiprows = 1, usecols = (1,2,3,4,5,6), unpack = True)
    
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
    
    srctype = np.zeros(len(names), dtype = '52str')
    
    for i in range(len(names)):
        if(classes[i] == 'PWN/SNR'):
            srctype[i] = 'SNR/PWN'
            sppRA.append(RAs[i])
            sppDEC.append(DECs[i])
            sppeflux.append(eflux[i])
        elif((classes[i] == 'HBL') or (classes[i] == 'LBL') or (classes[i] == 'IBL') or (classes[i] == 'Blazar') or (classes[i] == 'FSRQ')):
            srctype[i] = 'blazar'
            bzrRA.append(RAs[i])
            bzrDEC.append(DECs[i])
            bzreflux.append(eflux[i])
        elif(classes[i] == 'SNR'):
            srctype[i] = 'SNR'
            snrRA.append(RAs[i])
            snrDEC.append(DECs[i])
            snreflux.append(eflux[i])
        elif(classes[i] == 'Starburst'):
            srctype[i] = 'starburst'
            stbRA.append(RAs[i])
            stbDEC.append(DECs[i])
            stbeflux.append(eflux[i])
        elif(classes[i] == 'UNID'):
            srctype[i] = 'unknown g-ray src'
            unkRA.append(RAs[i])
            unkDEC.append(DECs[i])
            unkeflux.append(eflux[i])
        elif(classes[i] == 'XRB'):
            srctype[i] = 'XRB'
            xrbRA.append(RAs[i])
            xrbDEC.append(DECs[i])
            xrbeflux.append(eflux[i])
        elif(classes[i] == 'AGN'):
            srctype[i] = 'AGN / active galaxy'
            agnRA.append(RAs[i])
            agnDEC.append(DECs[i])
            agneflux.append(eflux[i])
        elif(classes[i] == 'SNR/MC'):
            srctype[i] = 'SNR / molecular cloud'
            snmRA.append(RAs[i])
            snmDEC.append(DECs[i])
            snmeflux.append(eflux[i])
        elif((classes[i] == 'PWN') or (classes[i] == 'PWN/UNID')):
            srctype[i] = 'pulsar wind nebula'
            pwnRA.append(RAs[i])
            pwnDEC.append(DECs[i])
            pwneflux.append(eflux[i])
        elif(classes[i] == 'Superbubble'):
            srctype[i] = 'superbubble'
            sblRA.append(RAs[i])
            sblDEC.append(DECs[i])
            sbleflux.append(eflux[i])
        elif(classes[i] == 'FRI'):
            srctype[i] = 'FRI'
            friRA.append(RAs[i])
            friDEC.append(DECs[i])
            frieflux.append(eflux[i])
        elif(classes[i] == 'BIN'):
            srctype[i] = 'binary'
            binRA.append(RAs[i])
            binDEC.append(DECs[i])
            bineflux.append(eflux[i])
        elif(classes[i] == 'WR/MSC'):
            srctype[i] = 'Wolf-Rayet star'
            wrsRA.append(RAs[i])
            wrsDEC.append(DECs[i])
            wrseflux.append(eflux[i])
        elif(classes[i] == 'SNR/SHELL'):
            srctype[i] = 'SNR / Shell'
            snsRA.append(RAs[i])
            snsDEC.append(DECs[i])
            snseflux.append(eflux[i])
        elif(classes[i] == 'GC'):
            srctype[i] = 'globular cluster'
            glcRA.append(RAs[i])
            glcDEC.append(DECs[i])
            glceflux.append(eflux[i])
            
    return names, RAs, DECs, eflux, pflux, srctype, rshift, sppRA, sppDEC, sppeflux, bzrRA, bzrDEC, bzreflux, snrRA, snrDEC, snreflux, stbRA, stbDEC, stbeflux, unkRA, unkDEC, unkeflux, xrbRA, xrbDEC, xrbeflux, agnRA, agnDEC, agneflux, snmRA, snmDEC, snmeflux, pwnRA, pwnDEC, pwneflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, binRA, binDEC, bineflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, glcRA, glcDEC, glceflux