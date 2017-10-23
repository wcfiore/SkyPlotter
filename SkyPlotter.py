#!/usr/bin/python
import argparse
import sys
from astropy.time import Time

# We want the user to input the neutrino event's RA, DEC, and the radius of its error circle:

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--RA', type = float, dest = 'RA', help = 'enter right ascension in degrees')
parser.add_argument('-d', '--DEC', type = float, dest = 'DEC', help = 'enter declination in degrees')
parser.add_argument('-e', '--ERR', type = float, dest = 'ERR', help = 'enter radius of the error circle in degrees')
parser.add_argument('-t', '--start', type = str, dest = 'start', help = "start time of event, format 'YYYY-MM-DD" \
                    + "HH:MM:SS.SSS...'", default=(Time.now().mjd - 365))
parser.add_argument('-s', '--stop', type = str, dest = 'stop', help = "end time of event, format 'YYYY-MM-DD" \
                    + "HH:MM:SS.SSS...'", default=Time.now().mjd)
parser.add_argument('-c', '--cats', type = str, dest = 'catalogs', nargs = '+', help = \
                    'Manually include the catalogs of your choice.' \
                    + ' Choices include: "3FGL", "2FHL", "2FAV", "TeGeV",' \
                    + '"ROSAT", "XMM", "NBG" (nearby galaxies), "FAVA", "GRB", and "SNe"')

args = parser.parse_args()



#Limit acceptable values of RA and DEC. 

if not(0.0 <= args.RA <= 360.0):
    print('Error: Right Ascension should be between 0 and 360 degrees')
    sys.exit()
    
if not(-90.0 <= args.DEC <= 90.0):
    print('Error: Declination should be between -90 and 90 degrees')
    sys.exit()

if not(0.0 <= args.ERR <= 90.0):
    print('Error: Error circle radius should be between 0 and 90 degrees')
    sys.exit()

event_parameters = {
    "RA": args.RA,
    "DEC": args.DEC,
    "ERR": args.ERR,
    "start": Time(args.start, format = 'iso', scale = 'utc'),
    "stop": Time(args.stop, format = 'iso', scale = 'utc'),
    "RA1" : args.RA - 1.5 * args.ERR,
    "RA2": args.RA + 1.5 * args.ERR,
    "DEC1": args.DEC - 1.5 * args.ERR,
    "DEC2": args.DEC + 1.5 * args.ERR
}

if 'catalogs' not in args or args.catalogs == None:
    catalogs = ['3FGL', '2FHL', '2FAV', 'TeGeV', 'ROSAT', 'XMM', 'NBG', 'FAVA', 'GRB', 'SNe']
else:
    catalogs = args.catalogs

if(event_parameters["start"] > event_parameters["stop"]):
    print("Error: Event's end time should be after its start time.")
    sys.exit()

######################################

catalog_search_results = dict()

pltRA, pltDEC, srctype, pltsize, labels, markers = [], [], [], [], [], []

check = False

for i in catalogs:
    if(i == '3FGL'):
        import readfits
        names3FGL, RAs3FGL, DECs3FGL, eflux3FGL, pflux3FGL, srctype3FGL, rshift3FGL, pltRA, pltDEC, pltsize, labels, \
        markers = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit', \
                          './3FGLCat.fit', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '3FGL', pltRA, pltDEC, pltsize, \
                                    labels, markers)
        check = True
        
if(check == False):
    names3FGL, RAs3FGL, DECs3FGL, eflux3FGL, pflux3FGL, srctype3FGL, rshift3FGL = [], [], [], [], [], [], []
else:
    check = False

for i in catalogs:
    if(i == '2FHL'):
        import readfits
        names2FHL, RAs2FHL, DECs2FHL, eflux2FHL, pflux2FHL, srctype2FHL, rshift2FHL, pltRA, pltDEC, pltsize, labels, \
        markers = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/2FHL/gll_psch_v09.fit', \
                                    './2FHLCat.fit', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '2FHL', pltRA, pltDEC, \
                                    pltsize, labels, markers)
        check = True
        
if(check == False):
    names2FHL, RAs2FHL, DECs2FHL, eflux2FHL, pflux2FHL, srctype2FHL, rshift2FHL = [], [], [], [], [], [], []
else:
    check = False

for i in catalogs:
    if(i == '2FAV'):
        import readfits
        names2FAV, RAs2FAV, DECs2FAV, eflux2FAV, pflux2FAV, srctype2FAV, rshift2FAV, pltRA, pltDEC, pltsize, labels, \
        markers = readfits.readfits('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/fava_catalog/2fav_v09.fits', \
                                    './2FAV.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, '2FAV', pltRA, pltDEC, \
                                    pltsize, labels, markers)
        check = True
        
if(check == False):
    names2FAV, RAs2FAV, DECs2FAV, eflux2FAV, pflux2FAV, srctype2FAV, rshift2FAV = [], [], [], [], [], [], []
else:
    check = False

for i in catalogs:
    if(i == 'ROSAT'):
        import readfits
        namesRX, RAsRX, DECsRX, efluxRX, pfluxRX, srctypeRX, rshiftRX, pltRA, pltDEC, pltsize, labels, markers = \
        readfits.readfits('nope', './ROSAT.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'ROSAT', pltRA, pltDEC, \
                          pltsize, labels, markers)
        check = True
        
if(check == False):
    namesRX, RAsRX, DECsRX, efluxRX, pfluxRX, srctypeRX, rshiftRX = [], [], [], [], [], [], []
else:
    check = False     

for i in catalogs:
    if(i == 'XMM'):
        import readfits
        namesXMM, RAsXMM, DECsXMM, efluxXMM, pfluxXMM, srctypeXMM, rshiftXMM, pltRA, pltDEC, pltsize, labels, \
        markers = readfits.readfits('nope', './CAIXA_XMM.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'XMM', pltRA, \
                                    pltDEC, pltsize, labels, markers)
        check = True
        
if(check == False):
    namesXMM, RAsXMM, DECsXMM, efluxXMM, pfluxXMM, srctypeXMM, rshiftXMM = [], [], [], [], [], [], []
else:
    check = False

for i in catalogs:
    if(i == 'NBG'):
        import readfits
        namesNBG, RAsNBG, DECsNBG, bmagNBG, distNBG, galtypeNBG, pltRA, pltDEC, pltsize, labels, markers = \
        readfits.readfits('nope', './neargalcat.fits', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, 'neargalcat', pltRA, \
                          pltDEC, pltsize, labels, markers)
        check = True
        
if(check == False):
    namesNBG, RAsNBG, DECsNBG, bmagNBG, distNBG, galtypeNBG = [], [], [], [], [], []
else:
    check = False

for i in catalogs:
    if(i == 'TeGeV'):
        import readTeGeV
        namesTeGeV, RAsTeGeV, DECsTeGeV, efluxTeGeV, pfluxTeGeV, srctypeTeGeV, rshiftTeGeV, pltRA, pltDEC, \
        pltsize, labels, markers = readTeGeV.readTeGeV('TeGeVCat.dat', RA, DEC, ERR, RA1, RA2, DEC1, DEC2, pltRA, pltDEC, \
                                              pltsize, labels, markers)
        check = True
        
if(check == False):
    namesTeGeV, RAsTeGeV, DECsTeGeV, efluxTeGeV, pfluxTeGeV, srctypeTeGeV, rshiftTeGeV = [], [], [], [], [], [], []
else:
    check = False

if "FAVA" in catalogs:
    import readFAVA
    FAVA_dict = readFAVA.readFAVA(event_parameters)
    catalog_search_results["FAVA"] = FAVA_dict

if "GRB" in catalogs:
    import readGCN
    catalog_search_results["GRB"] = readGCN.readGCN(event_parameters)

for i in catalogs:
    if(i == 'SNe'):
        import readSNe
        
        namesSNe, RAsSNe, DECsSNe, datesSNe, typesSNe, magsSNe, hostsSNe, pltRA, pltDEC, pltsize, markers, labels = \
        readSNe.readSNe('https://raw.githubusercontent.com/astrocatalogs/supernovae/master/output/catalog.json', \
                        'catalog.json', RA, DEC, ERR, pltRA, pltDEC, pltsize, markers, labels)
        
        check = True
        
if(check == False):
    namesSNe, RAsSNe, DECsSNe, datesSNe, typesSNe, magsSNe, hostsSNe = [], [], [], [], [], [], []
else:
    check = False
    
import printout

printout.printout(event_parameters, catalog_search_results)

from astropy.visualization import astropy_mpl_style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

import ploterrcirc

ploterrcirc.ploterrcirc(event_parameters)

import plotsrcs

plotsrcs.plotsrcs(catalog_search_results)

