from astropy.io import fits
import argparse, sys, os, urllib.request
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
#get_ipython().magic('matplotlib inline')

######################################

# We want the user to input the neutrino event's RA, DEC, and the radius of its error circle:

#parser = argparse.ArgumentParser()
#parser.add_argument('-r', '--RA', type = float, dest = 'RA', help = 'enter right ascension in degrees')
#parser.add_argument('-d', '--DEC', type = float, dest = 'DEC', help = 'enter declination in degrees')
#parser.add_argument('-e', '--ERR', type = float, dest = 'ERR', help = 'enter radius of the error circle in degrees')

#args = parser.parse_args()

# Limit acceptable values of RA and DEC. 
# It's possible to do this in argparse but I haven't found a good way yet.

#if not(0.0 <= args.RA <= 360.0):
#    print('Error: Right Ascension should be between 0 and 360 degrees')
#    sys.exit()
    
#if not(-90.0 <= args.DEC <= 90.0):
#    print('Error: Declination should be between -90 and 90 degrees')
#    sys.exit()

# Variables are easier to work with without the 'args.'

#RA = args.RA
#DEC = args.DEC
#ERR = args.ERR


RA = 285.7
DEC = 3.1
ERR = 1.0

######################################

def ploterrcirc(RA, DEC, ERR):
    # Set the size of the grid to be 1.5x the size of the error circle
    
    RA1 = RA - 1.5 * ERR
    RA2 = RA + 1.5 * ERR
    DEC1 = DEC - 1.5 * ERR
    DEC2 = DEC + 1.5 * ERR
    
    # Now plot the error circle
    
    fig = plt.figure(1, figsize=(7, 7))
    plt.axis([RA1, RA2, DEC1, DEC2])
    ax = fig.add_subplot(1, 1, 1)
    errcirc = plt.Circle((RA, DEC), radius = ERR, color = 'r', fill = False)
    ax.add_patch(errcirc)
    
    # Label axes
    
    plt.xlabel('RA (deg)', fontsize = 14)
    plt.ylabel('DEC (deg)', fontsize = 14)
        
    # We can also plot an 'x' at the center of the circle to mark the RA and DEC of the detection
    
    plt.plot(RA, DEC, 'x', color = 'r')
    
######################################

def plotfits(URL, file_name, RA, DEC, ERR, marker):
    # Check if the catalog exists already. If not, download it from the website and save it:
    if(os.path.isfile(file_name) == False):
        urllib.request.urlretrieve(URL, file_name)
    
    # Read data from file:
    hdulist = fits.open(file_name)
    tbdata = hdulist[1].data
    names = tbdata.field(0)
    RAs = tbdata.field(1)
    DECs = tbdata.field(2)
    classes = tbdata.field(34)
    
    # Plot sources that are within the error circle:
    for i in range(len(names)):
        if(((RAs[i] - RA) ** 2 + (DECs[i] - DEC) ** 2) > (ERR ** 2)):
            names[i] = 999.6
            RAs[i] = 999.6
            DECs[i] = 999.6
            classes[i] = 999.6
    
    list(filter(lambda a: a != 999.6, names))
    list(filter(lambda a: a != 999.6, RAs))
    list(filter(lambda a: a != 999.6, DECs))
    list(filter(lambda a: a != 999.6, classes))
    
    srctype = np.zeros(len(names), dtype = 'str')
    for i in range(len(names)):
        srctype[i] = 'unknown source'
    
    for i in range(len(names)):
        if((classes[i] == 'psr') or (classes[i] == 'PSR')):
            srctype[i] = 'pulsar'
            plt.plot(RAs[i], DECs[i], c = 'b')
        if(classes[i] == 'pwn'):
            srctype[i] = 'psr wind nebula'
            plt.plot(RAs[i], DECs[i], c = 'b')
        if(classes[i] == 'snr'):
            srctype[i] = 'SNR'
            plt.plot(RAs[i], DECs[i], c = 'g')
        if(classes[i] == 'spp'):
            srctype[i] = 'SNR/PWN'
            plt.plot(RAs[i], DECs[i], c = 'g')
        if(classes[i] == 'hmb'):
            srctype[i] = 'high-mass binary'
            plt.plot(RAs[i], DECs[i], c = 'r')
        if(classes[i] == 'bin'):
            srctype[i] = 'binary'
            plt.plot(RAs[i], DECs[i], c = 'r')
        if(classes[i] == 'sfr'):
            srctype[i] = 'star-forming region'
            plt.plot(RAs[i], DECs[i], c = 'c')
        if((classes[i] == 'bll') or (classes[i] == 'bll-g') or (classes[i] == 'fsrq') or (classes[i] == 'bcu I') or (classes[i] == 'bcu II') or (classes[i] == 'bcu III')):
            srctype[i] = blazar
            plt.plot(RAs[i], DECs[i], c = 'm')
        if((classes[i] == 'agn') or (classes[i] == 'bcu')):
            srctype[i] = 'AGN / active galaxy'
            plt.plot(RAs[i], DECs[i], c = 'm')
        if(classes[i] == 'rdg'):
            srctype[i] = 'radio galaxy'
            plt.plot(RAs[i], DECs[i], c = 'm')
        if(classes[i] == 'rdg/bll'):
            srctype[i] = 'radio galaxy / BL Lac blazar'
            plt.plot(RAs[i], DECs[i], c = 'm')
        if(classes[i] == 'gal'):
            srctype[i] = 'normal galaxy (or part)'
            plt.plot(RAs[i], DECs[i], c = 'y')
        if(classes[i] == 'galclu'):
            srctype[i] = 'galaxy cluster'
            plt.plot(RAs[i], DECs[i], c = 'k')
        if((classes[i] == 'nlsy1') or (classes[i] == 'sey')):
            srctype[i] = 'Seyfert galaxy'
            plt.plot(RAs[i], DECs[i], c = 'm')
        if(classes[i] == 'nov'):
            srctype[i] = 'nova'
            plt.plot(RAs[i], DECs[i], c = 'w')
        if(classes[i] == 'glc'):
            srctype[i] = 'globular cluster'
            plt.plot(RAs[i], DECs[i], c = 'black')
        if((classes[i] == 'css') or (classes[i] == 'ssrq')):
            srctype[i] = 'quasar'
            plt.plot(RAs[i], DECs[i], c = 'm')
        if(classes[i] == 'sbg'):
            srctype[i] = 'starburst galaxy'
            plt.plot(RAs[i], DECs[i], c = 'aqua')
        if(classes[i] == 'spp'):
            srctype[i] = 'special case - potential association with SNR or PWN'
            plt.plot(RAs[i], DECs[i], c = '0.75')
    
    # Here, we will make sure that these arrays won't be overwritten next time the function is called with a different catalog
    # Also, by setting the new arrays as global variables, we can then use them later in the program
    
    if hasattr(marker, '3FGL'):
        global names_3FGL
        global RAs_3FGL
        global DECs_3FGL
        global classes_3FGL
        global srctype_3FGL
        names_3FGL = names
        RAs_3FGL = RAs
        DECs_3FGL = DECs
        classes_3FGL = classes
        srctype_3FGL = srctype
        del names
        del RAs
        del DECs
        del classes
        del srctype
    if hasattr(marker, '2FHL'):
        global names_2FHL
        global RAs_2FHL
        global DECs_2FHL
        global classes_2FHL
        global srctype_2FHL
        names_2FHL = names
        RAs_2FHL = RAs
        DECs_2FHL = DECs
        classes_2FHL = classes
        srctype_2FHL = srctype
        del names
        del RAs
        del DECs
        del classes
        del srctype
    if hasattr(marker, 'TEV'):
        global names_TEV
        global RAs_TEV
        global DECs_TEV
        global classes_TEV
        global srctype_TEV
        names_TEV = names
        RAs_TEV = RAs
        DECs_TEV = DECs
        classes_TEV = classes
        srctype_TEV = srctype
        del names
        del RAs
        del DECs
        del classes
        del srctype
    
######################################

#def printout(RA, DEC, ERR, names_3FGL, names_2FHL, names_TEV, RAs_3FGL, RAs_2FHL, RAs_TEV, DECs_3FGL, DECs_2FHL, DECs_TEV, srctype_3FGL, srctype_2FHL, srctype_TEV):
def printout(RA, DEC, ERR, names_3FGL, names_2FHL, RAs_3FGL, RAs_2FHL, DECs_3FGL, DECs_2FHL, srctype_3FGL, srctype_2FHL):    
    names = names_3FGL + names_2FHL
    RAs = RAs_3FGL + RAs_2FHL
    DECs = DECs_3FGL + DECs_2FHL
    srctype = srctype_3FGL + srctype_2FHL
    
    print('NEUTRINO SOURCE CANDIDATES WITHIN', ERR, 'DEGREES OF: RA', RA, 'DEC', DEC)
    
    
######################################
######################################

ploterrcirc(RA, DEC, ERR)
plotfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit', './3FGLCat.fit', RA, DEC, ERR, '3FGL')
plotfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/2FHL/gll_psch_v09.fit', './2FHLCat.fit', RA, DEC, ERR, '2FHL')
#plotfits('', './TEVCat.fit', RA, DEC, ERR, 'TEV')
#printout(RA, DEC, ERR, names_3FGL, names_2FHL, RAs_3FGL, RAs_2FHL, DECs_3FGL, DECs_2FHL, srctype_3FGL, srctype_2FHL)
print(names_3FGL)

plt.show()
