import matplotlib.pyplot as plt
import numpy as np


def plotsrcs(pltRA, pltDEC, srctype, pltflux, labels, RAsNBG, DECsNBG, bmagNBG, RAsFAVA, DECsFAVA):
    
    colors = ['b', 'lavender', 'darkred', 'g', 'r', 'pink', 'c', 'm', 'indigo', 'lime', 'aqua', 'y', 'k', 'tan', 'brown', \
              'black', 'darkviolet', 'maroon', 'dimgray', 'lightsalmon', 'indianred', 'fuchsia', 'deeppink', 'darkkhaki', \
              'rebeccapurple', 'olive', 'crimson', 'mediumorchid']
    
    if(pltRA != []):
        for st, cl, l in zip(srctype, colors, labels):
            if len(srctype[srctype == st]) > 0:
                plt.plot(pltRA[srctype == st], pltDEC[srctype == st], color = cl, markersize = \
                         np.multiply(pltflux[srctype == st], 10 ** 13) + 5, marker = 'o', label = l)
            
    if(RAsFAVA != []):
        plt.scatter(RAsFAVA, DECsFAVA, c = 'lightseagreen', s = 80, marker = 'X', label = 'FAVA Flare')
        
    if(RAsNBG != []):
        plt.scatter(RAsNBG, DECsNBG, c = 'palevioletred', s = 80 - bmagNBG, marker = '*', label = 'Nearby Galaxy')
        
    if((pltRA != []) or (RAsFAVA != []) or (RAsNBG != [])):
        plt.legend(bbox_to_anchor = (1.04, 1), loc = "upper left")
        
    plt.show()