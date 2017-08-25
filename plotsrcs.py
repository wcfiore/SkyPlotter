import matplotlib.pyplot as plt
import numpy as np


def plotsrcs(pltRA, pltDEC, srctype, pltflux, labels, RAsNBG, DECsNBG, bmagNBG, RAsFAVA, DECsFAVA, RAGRB, DECGRB):
    
    printlegend = False
    
    colors = ['b', 'lavender', 'darkred', 'g', 'r', 'pink', 'c', 'm', 'indigo', 'lime', 'aqua', 'y', 'k', 'tan', 'brown', \
              'black', 'darkviolet', 'maroon', 'dimgray', 'lightsalmon', 'indianred', 'fuchsia', 'deeppink', 'darkkhaki', \
              'rebeccapurple', 'olive', 'crimson', 'mediumorchid']
    marker_colors = []
    lb = []
    j = 0
    for i in range(len(labels)):
        if labels[i] not in lb:
            lb.append(labels[i])
            marker_colors.append(colors[j])
            j += 1
        else:
            for k in range(len(lb)):
                if(labels[i] == lb[k]):
                    marker_colors.append(colors[k])   
    
    if(len(pltRA) > 0):
        printlegend = True
        for st, cl, l in zip(srctype, marker_colors, labels):
            if len(srctype[srctype == st]) > 0:
                #plt.plot(pltRA[srctype == st], pltDEC[srctype == st], color = cl, \
                #         markersize = np.multiply(pltflux[srctype == st], 10 ** 13) - 15, label = l)
                plt.scatter(pltRA[srctype == st], pltDEC[srctype == st], c = cl, s = 20, label = l)
            
    if(len(RAsFAVA) > 0):
        printlegend = True
        plt.scatter(RAsFAVA, DECsFAVA, c = 'lightseagreen', s = 80, marker = 'X', label = 'FAVA Flare')
        
    if(len(RAsNBG) > 0):
        printlegend = True
        plt.scatter(RAsNBG, DECsNBG, c = 'palevioletred', s = 80 - bmagNBG, marker = '*', label = 'Nearby Galaxy')
        
    if(len(RAGRB) > 0):
        printlegend = True
        plt.scatter(RAGRB, DECGRB, c = 'r', s = 40, marker = 'D', label = 'Possible GRB')
        
    if(printlegend == True):
        plt.legend(bbox_to_anchor = (1.04, 1), loc = "upper left")
        plt.show()