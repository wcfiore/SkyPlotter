import argparse, sys
from astropy.time import Time
import matplotlib.pyplot as plt
import readfits, readTeGeV, readFAVA, ploterrcirc, plotsrcs, printout

# The following parameters are set this way so that the legend
# is not cut off when the program is run from a terminal:

from matplotlib import rcParams
rcParams.update({'figure.subplot.right': 0.73})
rcParams.update({'figure.subplot.left': 0.15})
rcParams.update({'figure.subplot.top': 0.89})
rcParams.update({'figure.subplot.bottom': 0.22})

# For running in ipython notebook (comment out otherwise):
# %matplotlib inline

# This part not needed if running from ipython notebook
# When using ipython notebook, set RA, DEC, ERR manually

# We want the user to input the neutrino event's RA, DEC, and the radius of its error circle:

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--RA', type = float, dest = 'RA', help = 'enter right ascension in degrees')
parser.add_argument('-d', '--DEC', type = float, dest = 'DEC', help = 'enter declination in degrees')
parser.add_argument('-e', '--ERR', type = float, dest = 'ERR', help = 'enter radius of the error circle in degrees')
parser.add_argument('-t', '--start', type = str, dest = 'start', help = "start time of event, format 'YYYY-MM-DD HH:MM:SS.SSS...'")
parser.add_argument('-s', '--stop', type = str, dest = 'stop', help = "end time of event, format 'YYYY-MM-DD HH:MM:SS.SSS...'")

args = parser.parse_args()

#Limit acceptable values of RA and DEC. 
#It's possible to do this in argparse but I haven't found a good way yet.

if not(0.0 <= args.RA <= 360.0):
   print('Error: Right Ascension should be between 0 and 360 degrees')
   sys.exit()
    
if not(-90.0 <= args.DEC <= 90.0):
   print('Error: Declination should be between -90 and 90 degrees')
   sys.exit()

if not(0.0 <= args.ERR <= 90.0):
   print('Error: Error should be between 0 and 90 degrees')
   sys.exit()

if(args.start > args.stop):
    print("Error: Event's end time should be after its start time.")
    sys.exit()

# Variables are easier to work with without the 'args.'

RA = args.RA
DEC = args.DEC
ERR = args.ERR
start = args.start
stop = args.stop

start = Time(start, format = 'iso', scale = 'utc')
stop = Time(stop, format = 'iso', scale = 'utc')

######################################

RA1 = RA - 1.5 * ERR
RA2 = RA + 1.5 * ERR
DEC1 = DEC - 1.5 * ERR
DEC2 = DEC + 1.5 * ERR

######################################

psrRA, psrDEC, psreflux = [], [], []
pwnRA, pwnDEC, pwneflux = [], [], []
snrRA, snrDEC, snreflux = [], [], []
sppRA, sppDEC, sppeflux = [], [], []
hmbRA, hmbDEC, hmbeflux = [], [], []
bzrRA, bzrDEC, bzreflux = [], [], []
rdgRA, rdgDEC, rdgeflux = [], [], []
gclRA, gclDEC, gcleflux = [], [], []
agnRA, agnDEC, agneflux = [], [], []
binRA, binDEC, bineflux = [], [], []
sfrRA, sfrDEC, sfreflux = [], [], []
galRA, galDEC, galeflux = [], [], []
rgbRA, rgbDEC, rgbeflux = [], [], []
seyRA, seyDEC, seyeflux = [], [], []
novRA, novDEC, noveflux = [], [], []
glcRA, glcDEC, glceflux = [], [], []
qsrRA, qsrDEC, qsreflux = [], [], []
sbgRA, sbgDEC, sbgeflux = [], [], []
unkRA, unkDEC, unkeflux = [], [], []
stbRA, stbDEC, stbeflux = [], [], []
xrbRA, xrbDEC, xrbeflux = [], [], []
snmRA, snmDEC, snmeflux = [], [], []
sblRA, sblDEC, sbleflux = [], [], []
friRA, friDEC, frieflux = [], [], []
wrsRA, wrsDEC, wrseflux = [], [], []
snsRA, snsDEC, snseflux = [], [], []

names3FGL, RAs3FGL, DECs3FGL, eflux3FGL, pflux3FGL, srctype3FGL, rshift3FGL, psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit', './3FGLCat.fit', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '3FGL', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

names2FHL, RAs2FHL, DECs2FHL, eflux2FHL, pflux2FHL, srctype2FHL, rshift2FHL, psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/2FHL/gll_psch_v09.fit', './2FHLCat.fit', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '2FHL', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

names2FAV, RAs2FAV, DECs2FAV, eflux2FAV, pflux2FAV, srctype2FAV, rshift2FAV, psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/fava_catalog/2fav_v09.fits', './2FAV.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '2FAV', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

namesRX, RAsRX, DECsRX, efluxRX, pfluxRX, srctypeRX, rshiftRX, agnRA, agnDEC, agneflux = readfits.readfits('nope', './ROSAT.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'ROSAT', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

namesXMM, RAsXMM, DECsXMM, efluxXMM, pfluxXMM, srctypeXMM, rshiftXMM, agnRA, agnDEC, agneflux = readfits.readfits('nope', './CAIXA_XMM.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'XMM', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

namesNBG, RAsNBG, DECsNBG, bmagNBG, distNBG, galtypeNBG = readfits.readfits('nope', './neargalcat.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'neargalcat', psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux)

namesTeGeV, RAsTeGeV, DECsTeGeV, efluxTeGeV, pfluxTeGeV, srctypeTeGeV, rshiftTeGeV, sppRA, sppDEC, sppeflux, bzrRA, bzrDEC, bzreflux, snrRA, snrDEC, snreflux, stbRA, stbDEC, stbeflux, unkRA, unkDEC, unkeflux, xrbRA, xrbDEC, xrbeflux, agnRA, agnDEC, agneflux, snmRA, snmDEC, snmeflux, pwnRA, pwnDEC, pwneflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, binRA, binDEC, bineflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, glcRA, glcDEC, glceflux = readTeGeV.readTeGeV('TeGeVCat.dat', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, sppRA, sppDEC, sppeflux, bzrRA, bzrDEC, bzreflux, snrRA, snrDEC, snreflux, stbRA, stbDEC, stbeflux, unkRA, unkDEC, unkeflux, xrbRA, xrbDEC, xrbeflux, agnRA, agnDEC, agneflux, snmRA, snmDEC, snmeflux, pwnRA, pwnDEC, pwneflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, binRA, binDEC, bineflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, glcRA, glcDEC, glceflux)

namesFAVA, RAsFAVA, DECsFAVA, srctypeFAVA, t1FAVA, t2FAVA, lefluxFAVA, hefluxFAVA = readFAVA.readFAVA(RA, DEC, ERR, start, stop, RA1, RA2, DEC1, DEC2)

ploterrcirc.ploterrcirc(RA, DEC, ERR, RA1, RA2, DEC1, DEC2)

printout.printout(RA, DEC, ERR, start, stop, names3FGL, RAs3FGL, DECs3FGL, eflux3FGL, pflux3FGL, srctype3FGL, rshift3FGL, names2FHL, RAs2FHL, DECs2FHL, eflux2FHL, pflux2FHL, srctype2FHL, rshift2FHL, names2FAV, RAs2FAV, DECs2FAV, eflux2FAV, pflux2FAV, srctype2FAV, rshift2FAV, namesRX, RAsRX, DECsRX, efluxRX, pfluxRX, srctypeRX, rshiftRX, namesXMM, RAsXMM, DECsXMM, efluxXMM, pfluxXMM, srctypeXMM, rshiftXMM, namesTeGeV, RAsTeGeV, DECsTeGeV, efluxTeGeV, pfluxTeGeV, srctypeTeGeV, rshiftTeGeV, namesFAVA, RAsFAVA, DECsFAVA, srctypeFAVA, t1FAVA, t2FAVA, lefluxFAVA, hefluxFAVA, namesNBG, RAsNBG, DECsNBG, bmagNBG, distNBG, galtypeNBG)

plotsrcs.plotsrcs(psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux, stbRA, stbDEC, stbeflux, xrbRA, xrbDEC, xrbeflux, snmRA, snmDEC, snmeflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, RAsFAVA, DECsFAVA, RAsNBG, DECsNBG, bmagNBG)

plt.show()