import matplotlib.pyplot as plt

# This function plots the error circle of the neutrino event

def ploterrcirc(params):

    fig = plt.figure(1, figsize=(7, 7))
    plt.axis([params["RA1"], params["RA2"], params["DEC1"], params["DEC2"]])
    ax = fig.add_subplot(1, 1, 1)
    errcirc = plt.Circle((params["RA"], params["DEC"]), radius=params["ERR"],
                         color='r', fill=False)
    ax.add_patch(errcirc)

    ticks = ax.get_xticks()
    ticks[ticks > 359.9999] -= 360
    ticks[ticks < 0.0] += 360
    ax.set_xticklabels([int(tick) for tick in ticks])

    plt.xlabel('RA (deg)', fontsize = 14)
    plt.ylabel('DEC (deg)', fontsize = 14)

    plt.plot(params["RA"], params["DEC"], 'x', color = 'r')
