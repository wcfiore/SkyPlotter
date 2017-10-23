import matplotlib.pyplot as plt

def plotsrcs(catalog_search_results):
    
    printlegend = False
    
    # colors = ['b', 'lavender', 'darkred', 'g', 'r', 'pink', 'c', 'm', 'indigo', 'lime', 'aqua', 'y', 'k', 'tan', 'brown', \
    #           'black', 'darkviolet', 'maroon', 'dimgray', 'lightsalmon', 'indianred', 'fuchsia', 'deeppink', 'darkkhaki', \
    #           'rebeccapurple', 'olive', 'crimson', 'mediumorchid', 'lightseagreen', 'palevioletred', 'brown']
    #
    # lb = ['pulsar', 'psr wind nebula', 'supernova remnant', 'SNR / PWN', 'high-mass binary', 'binary', \
    #       'star-forming region', 'blazar', 'active galaxy / AGN', 'radio galaxy', 'radio galaxy / BL Lac blazar', \
    #       'normal galaxy (or part), gamma ray source', 'galaxy cluster', 'Seyfert galaxy', 'nova', 'globular cluster', \
    #       'quasar', 'starburst galaxy', 'unassociated gamma ray source', 'starburst', 'XRB', 'SNR / molecular cloud', \
    #       'superbubble', 'FRI', 'Wolf-Rayet star', 'SNR / shell', 'nearby galaxy', 'FAVA flare', 'Possible GRB', 'supernova']
    #
    # j = 0
    #
    # for i in lb:
    #     if(len(pltRA[labels == i]) > 0):
    #         # plt.scatter(
    #         #     pltRA[labels == i], pltDEC[labels == i], c=colors[j],
    #         #     s=pltsize[labels == i], marker=markers[labels==i][0], label=i)
    #         plt.scatter(
    #             pltRA[labels == i], pltDEC[labels == i], c=colors[j],
    #             marker=markers[labels==i][0], label=i)
    #         j += 1
            
    # plt.legend(bbox_to_anchor = (1.04, 1), loc = "upper left")

    for name in catalog_search_results.keys():
        catalog = catalog_search_results[name]
        plt.scatter(
            catalog["data"]["RA"], catalog["data"]["Dec"], c=catalog["color"],
            s=catalog["data"]["size"], marker=catalog["marker"],
            label=catalog["label"]
        )

    plt.legend()
    plt.show()
    plt.savefig("output.pdf")
