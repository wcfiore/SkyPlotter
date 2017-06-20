from astropy.io import fits
import argparse, sys, os, urllib.request
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

######################################

# We want the user to input the neutrino event's RA, DEC, and the radius of its error circle:

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--RA', type = float, dest = 'RA', help = 'enter right ascension in degrees')
parser.add_argument('-d', '--DEC', type = float, dest = 'DEC', help = 'enter declination in degrees')
parser.add_argument('-e', '--ERR', type = float, dest = 'ERR', help = 'enter radius of the error circle in degrees')

args = parser.parse_args()

# Limit acceptable values of RA and DEC. 
# It's possible to do this in argparse but I haven't found a good way yet.

if not(0.0 <= args.RA <= 360.0):
    print('Error: Right Ascension should be between 0 and 360 degrees')
    sys.exit()
    
if not(-90.0 <= args.DEC <= 90.0):
    print('Error: Declination should be between -90 and 90 degrees')
    sys.exit()

 Variables are easier to work with without the 'args.'

RA = args.RA
DEC = args.DEC
ERR = args.ERR

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
    if(marker == '3FGL'):
        classes = tbdata.field(73)
    if(marker == '2FHL'):
        classes = tbdata.field(34)
    
    # Plot sources that are within the error circle:
    for i in range(len(names)):
        if(((RAs[i] - RA) ** 2 + (DECs[i] - DEC) ** 2) > (ERR ** 2)):
            names[i] = 'badcoord'
            RAs[i] = 1000.0
            DECs[i] = 1000.0
            classes[i] = 'badcoord'
    
    names = list(filter(lambda a: a != 'badcoord', names))
    RAs = list(filter(lambda a: a < 900.0, RAs))
    DECs = list(filter(lambda a: a < 900.0, DECs))
    classes = list(filter(lambda a: a != 'badcoord', classes))
    
    srctype = np.zeros(len(names), dtype = '52str')
    
    for i in range(len(names)):
        if((classes[i] == 'psr') or (classes[i] == 'PSR')):
            srctype[i] = 'pulsar'
            plt.scatter(RAs[i], DECs[i], c = 'b')
        elif(classes[i] == 'pwn'):
            srctype[i] = 'psr wind nebula'
            plt.scatter(RAs[i], DECs[i], c = 'b')
        elif(classes[i] == 'snr'):
            srctype[i] = 'SNR'
            plt.scatter(RAs[i], DECs[i], c = 'g')
        elif(classes[i] == 'spp'):
            srctype[i] = 'SNR/PWN'
            plt.scatter(RAs[i], DECs[i], c = 'g')
        elif(classes[i] == 'hmb'):
            srctype[i] = 'high-mass binary'
            plt.scatter(RAs[i], DECs[i], c = 'r')
        elif(classes[i] == 'bin'):
            srctype[i] = 'binary'
            plt.scatter(RAs[i], DECs[i], c = 'r')
        elif(classes[i] == 'sfr'):
            srctype[i] = 'star-forming region'
            plt.scatter(RAs[i], DECs[i], c = 'c')
        elif((classes[i] == 'bll') or (classes[i] == 'bll-g') or (classes[i] == 'fsrq') or (classes[i] == 'bcu I') or (classes[i] == 'bcu II') or (classes[i] == 'bcu III')):
            srctype[i] = blazar
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif((classes[i] == 'agn') or (classes[i] == 'bcu')):
            srctype[i] = 'AGN / active galaxy'
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif(classes[i] == 'rdg'):
            srctype[i] = 'radio galaxy'
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif(classes[i] == 'rdg/bll'):
            srctype[i] = 'radio galaxy / BL Lac blazar'
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif(classes[i] == 'gal'):
            srctype[i] = 'normal galaxy (or part)'
            plt.scatter(RAs[i], DECs[i], c = 'y')
        elif(classes[i] == 'galclu'):
            srctype[i] = 'galaxy cluster'
            plt.scatter(RAs[i], DECs[i], c = 'k')
        elif((classes[i] == 'nlsy1') or (classes[i] == 'sey')):
            srctype[i] = 'Seyfert galaxy'
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif(classes[i] == 'nov'):
            srctype[i] = 'nova'
            plt.scatter(RAs[i], DECs[i], c = 'w')
        elif(classes[i] == 'glc'):
            srctype[i] = 'globular cluster'
            plt.scatter(RAs[i], DECs[i], c = 'black')
        elif((classes[i] == 'css') or (classes[i] == 'ssrq')):
            srctype[i] = 'quasar'
            plt.scatter(RAs[i], DECs[i], c = 'm')
        elif(classes[i] == 'sbg'):
            srctype[i] = 'starburst galaxy'
            plt.scatter(RAs[i], DECs[i], c = 'aqua')
        elif(classes[i] == 'spp'):
            srctype[i] = 'special case - potential association with SNR or PWN'
            plt.scatter(RAs[i], DECs[i], c = 'purple')
        else:
            srctype[i] = 'unknown source'
            plt.scatter(RAs[i], DECs[i], c = '0.75')
    
    # Here, we will make sure that these arrays won't be overwritten next time the function is called with a different catalog
    # Also, by setting the new arrays as global variables, we can then use them later in the program
    
    if (marker == '3FGL'):
        global names3FGL
        global RAs3FGL
        global DECs3FGL
        global classes3FGL
        global srctype3FGL
        names3FGL = names
        RAs3FGL = RAs
        DECs3FGL = DECs
        classes3FGL = classes
        srctype3FGL = srctype
    if (marker == '2FHL'):
        global names2FHL
        global RAs2FHL
        global DECs2FHL
        global classes2FHL
        global srctype2FHL
        names2FHL = names
        RAs2FHL = RAs
        DECs2FHL = DECs
        classes2FHL = classes
        srctype2FHL = srctype
    if (marker == 'TEV'):
        global namesTEV
        global RAsTEV
        global DECsTEV
        global classesTEV
        global srctypeTEV
        namesTEV = names
        RAsTEV = RAs
        DECsTEV = DECs
        classesTEV = classes
        srctypeTEV = srctype
    
######################################

#def printout(RA, DEC, ERR, names3FGL, names2FHL, namesTEV, RAs3FGL, RAs2FHL, RAsTEV, DECs3FGL, DECs2FHL, DECsTEV, srctype3FGL, srctype2FHL, srctypeTEV):
def printout(RA, DEC, ERR, names3FGL, names2FHL, RAs3FGL, RAs2FHL, DECs3FGL, DECs2FHL, srctype3FGL, srctype2FHL):    
    names = np.append(names3FGL, names2FHL)
    RAs = np.append(RAs3FGL, RAs2FHL)
    DECs = np.append(DECs3FGL, DECs2FHL)
    srctype = np.append(srctype3FGL, srctype2FHL)
    
    print('NEUTRINO SOURCE CANDIDATES WITHIN', ERR, 'DEGREES OF: RA', RA, 'DEC', DEC)
    print('')
    print()
    
######################################
######################################

ploterrcirc(RA, DEC, ERR)
plotfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit', './3FGLCat.fit', RA, DEC, ERR, '3FGL')
plotfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/2FHL/gll_psch_v09.fit', './2FHLCat.fit', RA, DEC, ERR, '2FHL')
#plotfits('', './TEVCat.fit', RA, DEC, ERR, 'TEV')
printout(RA, DEC, ERR, names3FGL, names2FHL, RAs3FGL, RAs2FHL, DECs3FGL, DECs2FHL, srctype3FGL, srctype2FHL)
plt.show()



plt
