import numpy as np
from tabulate import tabulate

# This function outputs a table onto the command line listing the sources
# inside the error circle, along with their coordinates, name, type, and eflux.

def printout(RA, DEC, ERR, start, stop, names3FGL, RAs3FGL, DECs3FGL, eflux3FGL, pflux3FGL, srctype3FGL, rshift3FGL, names2FHL, RAs2FHL, DECs2FHL, eflux2FHL, pflux2FHL, srctype2FHL, rshift2FHL, names2FAV, RAs2FAV, DECs2FAV, eflux2FAV, pflux2FAV, srctype2FAV, rshift2FAV, namesRX, RAsRX, DECsRX, efluxRX, pfluxRX, srctypeRX, rshiftRX, namesXMM, RAsXMM, DECsXMM, efluxXMM, pfluxXMM, srctypeXMM, rshiftXMM, namesTeGeV, RAsTeGeV, DECsTeGeV, efluxTeGeV, pfluxTeGeV, srctypeTeGeV, rshiftTeGeV, namesFAVA, RAsFAVA, DECsFAVA, srctypeFAVA, t1FAVA, t2FAVA, lefluxFAVA, hefluxFAVA, namesNBG, RAsNBG, DECsNBG, bmagNBG, distNBG, galtypeNBG):
    
    names = np.append(names3FGL, names2FHL)
    names = np.append(names, names2FAV)
    names = np.append(names, namesTeGeV)
    names = np.append(names, namesRX)
    names = np.append(names, namesXMM)
    
    RAs = np.append(RAs3FGL, RAs2FHL)
    RAs = np.append(RAs, RAs2FAV)
    RAs = np.append(RAs, RAsTeGeV)
    RAs = np.append(RAs, RAsRX)
    RAs = np.append(RAs, RAsXMM)
    RAs[RAs > 360] -= 360
    RAs[RAs < 0] += 360
    RAs = np.around(RAs, decimals = 3)
    
    DECs = np.append(DECs3FGL, DECs2FHL)
    DECs = np.append(DECs, DECs2FAV)
    DECs = np.append(DECs, DECsTeGeV)
    DECs = np.append(DECs, DECsRX)
    DECs = np.append(DECs, DECsXMM)
    DECs = np.around(DECs, decimals = 3)
    
    eflux = np.append(eflux3FGL, eflux2FHL)
    eflux = np.append(eflux, eflux2FAV)
    eflux = np.append(eflux, efluxTeGeV)
    eflux = np.append(eflux, efluxRX)
    eflux = np.append(eflux, efluxXMM)
    
    for i in range(len(eflux)):
        eflux[i] = round(eflux[i], 15)
    pflux = np.append(pflux3FGL, pflux2FHL)
    pflux = np.append(pflux, pflux2FAV)
    pflux = np.append(pflux, pfluxTeGeV)
    pflux = np.append(pflux, pfluxRX)
    pflux = np.append(pflux, pfluxXMM)
    for i in range(len(pflux)):
        pflux[i] = round(pflux[i], 13)
        
    rshift = np.append(rshift3FGL, rshift2FHL)
    rshift = np.append(rshift, rshift2FAV)
    rshift = np.append(rshift, rshiftTeGeV)
    rshift = np.append(rshift, rshiftRX)
    rshift = np.append(rshift, rshiftXMM)
    
    for i in range(len(rshift)):
        if((rshift[i] == '-') or (rshift[i] == 'nan')):
            rshift[i] = '0.0'
    srctype = np.append(srctype3FGL, srctype2FHL)
    srctype = np.append(srctype, srctype2FAV)
    srctype = np.append(srctype, srctypeTeGeV)
    srctype = np.append(srctype, srctypeRX)
    srctype = np.append(srctype, srctypeXMM)

    #print(pflux3FGL, pflux2FHL, pflux2FAV, pfluxTeGeV)
    table = np.zeros(len(names), dtype = '20str, f, f, f, f, 5str, 30str')
    
    headers = ('Catalog & Name', 'RA', 'DEC', 'Energy Flux', 'Photon Flux', 'Redshift', 'Type')
    for i in range(len(names)):
        table[i] = (names[i], RAs[i], DECs[i], eflux[i], pflux[i], rshift[i], srctype[i])

    # Sort by eflux
    
    table = np.sort(table.view('20str, f, f, f, f, 5str, 30str'), order = ['f3'], axis = 0)[::-1].view()
    
    for i in range(len(names)):
        
        if(table[i][3] == 0.0):
            table[i][3] = np.nan
        if(table[i][4] == 0.0):
            table[i][4] = np.nan
        if(table[i][5] == '0.0'):
            table[i][5] = 'nan'
    
    names2 = namesFAVA
    
    RAs2 = RAsFAVA
    
    for i in range(len(RAs2)):
        if(RAs2[i] > 360):
            RAs2[i] -= 360
        elif(RAs2[i] < 0):
            RAs2[i] += 360

    RAs2 = np.around(RAs2, decimals = 3)

    DECs2 = DECsFAVA
    DECs2 = np.around(DECs2, decimals = 3)
    
    if(len(t1FAVA) != 0):
        t1 = t1FAVA.iso

        t2 = t2FAVA.iso
        
    leflux = lefluxFAVA
    heflux = hefluxFAVA
    
    table2 = np.zeros(len(names2), dtype = '20str, f, f, f, f, 30str, 30str')
    
    headers2 = ('Name', 'RA', 'DEC', 'LE Flux', 'HE Flux', 'Start Time', 'Stop Time')
    
    for i in range(len(names2)):
        table2[i] = (names2[i], RAs2[i], DECs2[i], leflux[i], heflux[i], t1[i], t2[i])
        
    table3 = np.zeros(len(namesNBG), dtype = '30str, f, f, f, f, 30str')
    
    headers3 = ('Name', 'RA', 'DEC', 'Bmag', 'Distance', 'Morphological Type')
    
    for i in range(len(namesNBG)):
        table3[i] = (namesNBG[i], RAsNBG[i], DECsNBG[i], bmagNBG[i], distNBG[i], galtypeNBG[i])
    
    print('NEUTRINO SOURCE CANDIDATES WITHIN', ERR, 'DEGREES OF: RA', RA, 'DEC', DEC)
    print('BETWEEN ' + start.iso + ' AND ' + stop.iso)
    print('')
    if(len(table) != 0):
        print('STEADY SOURCES:')
        print(tabulate(table, headers))
        print('')
        print("Note: RA and DEC are given in degrees. Energy flux is given in ergs/cm^2/s. " + \
              "Photon flux is given in ph/cm^2/s. Size of markers increases linearly with " + \
              "energy flux for sources with an energy flux value.")
    if(len(table2) != 0):
        print('TRANSIENTS:')
        print(tabulate(table2, headers2))
        print('')
        print("Note: RA and DEC are given in degrees. LE Flux is 100-800 MeV, HE Flux is 0.8-300 GeV. " + \
              "Fluxes are given in ph/cm^2/s.")
    if(len(table3) != 0):
        print('NEARBY GALAXIES:')
        print(tabulate(table3, headers3))
        print('')
        print("Note: RA and DEC are given in degrees. Distance is given in Mpc.")
    if((len(table) == 0) and (len(table2) == 0) and (len(table3) == 0)):
        print('NO SOURCES FOUND WITHIN ERROR CIRCLE')
    