import matplotlib.pyplot as plt
import numpy as np


def plotsrcs(psrRA, psrDEC, psreflux, pwnRA, pwnDEC, pwneflux, snrRA, snrDEC, snreflux, sppRA, sppDEC, sppeflux, hmbRA, hmbDEC, hmbeflux, bzrRA, bzrDEC, bzreflux, rdgRA, rdgDEC, rdgeflux, gclRA, gclDEC, gcleflux, agnRA, agnDEC, agneflux, binRA, binDEC, bineflux, sfrRA, sfrDEC, sfreflux, galRA, galDEC, galeflux, rgbRA, rgbDEC, rgbeflux, seyRA, seyDEC, seyeflux, novRA, novDEC, noveflux, glcRA, glcDEC, glceflux, qsrRA, qsrDEC, qsreflux, sbgRA, sbgDEC, sbgeflux, unkRA, unkDEC, unkeflux, stbRA, stbDEC, stbeflux, xrbRA, xrbDEC, xrbeflux, snmRA, snmDEC, snmeflux, sblRA, sblDEC, sbleflux, friRA, friDEC, frieflux, wrsRA, wrsDEC, wrseflux, snsRA, snsDEC, snseflux, RAsFAVA, DECsFAVA, nbgRA, nbgDEC, nbgbmag):
    
    if(psrRA != []):
        plt.scatter(psrRA, psrDEC, c = 'b', s = np.multiply(psreflux, 10 ** 13) + 25, label = 'pulsar')
    if(pwnRA != []):
        plt.scatter(pwnRA, pwnDEC, c = 'lavender', s = np.multiply(pwneflux, 10 ** 13) + 25, label = 'psr wind nebula')
    if(snrRA != []):
        plt.scatter(snrRA, snrDEC, c = 'darkred', s = np.multiply(snreflux, 10 ** 13) + 25, label = 'supernova remnant')
    if(sppRA != []):
        plt.scatter(sppRA, sppDEC, c = 'g', s = np.multiply(sppeflux, 10 ** 13) + 25, label = 'SNR or PWN')
    if(hmbRA != []):
        plt.scatter(hmbRA, hmbDEC, c = 'r', s = np.multiply(hmbeflux, 10 ** 13) + 25, label = 'high-mass binary')
    if(binRA != []):
        plt.scatter(binRA, binDEC, c = 'pink', s = np.multiply(bineflux, 10 ** 13) + 25, label = 'binary')
    if(sfrRA != []):
        plt.scatter(sfrRA, sfrDEC, c = 'c', s = np.multiply(sfreflux, 10 ** 13) + 25, label = 'star-forming region')
    if(bzrRA != []):
        plt.scatter(bzrRA, bzrDEC, c = 'm', s = np.multiply(bzreflux, 10 ** 13) + 25, label = 'blazar')
    if(agnRA != []):
        plt.scatter(agnRA, agnDEC, c = 'indigo', s = np.multiply(agneflux, 10 ** 13) + 25, label = 'AGN / active galaxy')
    if(rdgRA != []):
        plt.scatter(rdgRA, rdgDEC, c = 'lime', s = np.multiply(rdgeflux, 10 ** 13) + 25, label = 'radio galaxy')
    if(rgbRA != []):
        plt.scatter(rgbRA, rgbDEC, c = 'aqua', s = np.multiply(rgbeflux, 10 ** 13) + 25, label = 'radio galaxy / BL Lac blazar')
    if(galRA != []):    
        plt.scatter(galRA, galDEC, c = 'y', s = np.multiply(galeflux, 10 ** 13) + 25, label = 'galaxy')
    if(gclRA != []):
        plt.scatter(gclRA, gclDEC, c = 'k', s = np.multiply(gcleflux, 10 ** 13) + 25, label = 'galaxy cluster')
    if(seyRA != []):
        plt.scatter(seyRA, seyDEC, c = 'tan', s = np.multiply(seyeflux, 10 ** 13) + 25, label = 'Seyfert galaxy')
    if(novRA != []):
        plt.scatter(novRA, novDEC, c = 'brown', s = np.multiply(noveflux, 10 ** 13) + 25, label = 'nova')
    if(glcRA != []):
        plt.scatter(glcRA, glcDEC, c = 'black', s = np.multiply(glceflux, 10 ** 13) + 25, label = 'globular cluster')
    if(qsrRA != []):
        plt.scatter(qsrRA, qsrDEC, c = 'darkviolet', s = np.multiply(qsreflux, 10 ** 13) + 25, label = 'quasar')
    if(sbgRA != []):
        plt.scatter(sbgRA, sbgDEC, c = 'maroon', s = np.multiply(sbgeflux, 10 ** 13) + 25, label = 'starburst galaxy')
    if(unkRA != []):    
        plt.scatter(unkRA, unkDEC, c = 'dimgray', s = np.multiply(unkeflux, 10 ** 13) + 25, label = 'unknown g-ray src')
    if(stbRA != []):    
        plt.scatter(stbRA, stbDEC, c = 'lightsalmon', s = np.multiply(stbeflux, 10 ** 13) + 25, label = 'starburst')
    if(xrbRA != []):    
        plt.scatter(xrbRA, xrbDEC, c = 'indianred', s = np.multiply(xrbeflux, 10 ** 13) + 25, label = 'XRB')
    if(snmRA != []):    
        plt.scatter(snmRA, snmDEC, c = 'fuchsia', s = np.multiply(snmeflux, 10 ** 13) + 25, label = 'SNR / molecular cloud')
    if(sblRA != []):    
        plt.scatter(sblRA, sblDEC, c = 'deeppink', s = np.multiply(sbleflux, 10 ** 13) + 25, label = 'Superbubble')
    if(friRA != []):    
        plt.scatter(friRA, friDEC, c = 'darkkhaki', s = np.multiply(frieflux, 10 ** 13) + 25, label = 'FRI')
    if(wrsRA != []):    
        plt.scatter(wrsRA, wrsDEC, c = 'rebeccapurple', s = np.multiply(wrseflux, 10 ** 13) + 25, label = 'Wolf-Rayet star')
    if(snsRA != []):    
        plt.scatter(snsRA, snsDEC, c = 'olive', s = np.multiply(unkeflux, 10 ** 13) + 25, label = 'SNR / Shell')
    if(RAsFAVA != []):
        plt.scatter(RAsFAVA, DECsFAVA, c = 'lightseagreen', s = 50, label = 'FAVA Flare')
    if(nbgRA != []):
        plt.scatter(nbgRA, nbgDEC, c = 'palevioletred', s = 45 - nbgbmag, label = 'Nearby Galaxy')
    if((psrRA != []) or (pwnRA != []) or (snrRA != []) or (sppRA != []) or (hmbRA != []) or (binRA != []) or (sfrRA != []) or (bzrRA != []) or (agnRA != []) or (rdgRA != []) or (rgbRA != []) or (galRA != []) or (gclRA != []) or (seyRA != []) or (novRA != []) or (glcRA != []) or (qsrRA != []) or (sbgRA != []) or (unkRA != []) or (stbRA != []) or (xrbRA != []) or (snmRA != []) or (sblRA != []) or (friRA != []) or (wrsRA != []) or (snsRA != []) or (RAsFAVA != []) or nbgRA != []):
        plt.legend(bbox_to_anchor = (1.04, 1), loc = "upper left")