import urllib2
from bs4 import BeautifulSoup
import sys
from astropy.time import Time
import astropy.units as u
import numpy as np

def readGCN(parameters):

    triggerNs = []
    burstDates = []
    burstTimes = []
    RAs = []
    Decs = []
    Errors = []

    for tel in ["Swift", "MAXI", "Fermi", "Integral"]:

        htmlAddress = "https://gcn.gsfc.nasa.gov/%s_grbs.html"%tel.lower()

        if tel == 'Swift':
            trigInd  = 0
            dateInd  = 1
            timeInd  = 2
            raInd    = 3
            decInd   = 4
            errorInd = 5
        elif tel == "MAXI" or tel=="Fermi" or tel=='Integral':
            trigInd  = 0
            dateInd  = 1
            timeInd  = 2
            raInd    = 4
            decInd   = 5
            errorInd = 6
        else:
            print("%s is not a valid choice. Valid choices are MAXI, Fermi, Integral, Swift. Exit")
            sys.exit()

        sock = urllib2.urlopen(htmlAddress)
        htmlSource = sock.read()

        parsed_html = BeautifulSoup(htmlSource, "lxml")

        table = parsed_html.body.find("table")
        rows = table.findAll('tr')


        for row in rows:
            cols = row.findAll("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols) > 1:
                allInd = [trigInd, dateInd, timeInd, raInd, decInd, errorInd]
                info = [cols[i] for i in allInd]
                if "" not in info:
                    trigger = tel + " " + cols[trigInd]
                    triggerNs.append(trigger)
                    date = cols[dateInd]
                    burstDates.append(date)
                    time = '20' + date + ' ' + cols[timeInd]
                    time = time.replace('/', '-')

                    burstTimes.append(time)
                    RAs.append(cols[raInd])
                    Decs.append(cols[decInd])
                    Errors.append(cols[errorInd])

    burstTimes = Time(burstTimes, format="iso", scale="utc")
    t1 = parameters["start"] - 300 * u.s
    t2 = parameters["stop"] + 300 * u.s

    triggerNs = np.asarray(triggerNs)
    burstTimes = np.asarray(burstTimes)
    RAs = np.asarray(RAs)
    Decs = np.asarray(Decs)
    Errors = np.asarray(Errors)

    RAs = RAs.astype('float')
    Decs = Decs.astype('float')

    RAs[RAs < parameters["RA1"]] += 360
    RAs[RAs > parameters["RA2"]] -= 360

    mask = (
        (((RAs - parameters["RA"]) ** 2 + (Decs - parameters["DEC"]) ** 2)
         <= (parameters["ERR"] ** 2))
        & (t1 < burstTimes) & (burstTimes < t2))

    triggerNs = triggerNs[mask]
    burstTimes = burstTimes[mask]
    RAs = RAs[mask]
    Decs = Decs[mask]
    Errors = Errors[mask]

    for i in range(len(RAs)):
        if(RAs[i] > 360):
            RAs[i] -= 360
        elif(RAs[i] < 0):
            RAs[i] += 360

    dt = np.dtype([
        ('Name', "S50"),
        ('RA', np.float),
        ('Dec', np.float),
        ('Time', "S50"),
        ('Error', np.float),
        ('size', np.float)
    ])

    table = np.zeros(len(triggerNs), dtype=dt)

    for i in range(len(triggerNs)):
        new = np.array((triggerNs[i], RAs[i], Decs[i],
                        burstTimes[i].iso, Errors[i],
                        80), dtype=dt)
        table[i] = new

    table = np.sort(table, order = ['Time'], axis = 0)[::-1].view()

    GCN_dict = {
        "data": table,
        "message_1": "GAMMA RAY BURSTS:",
        "message_2": 'Note: RA and DEC are given in degrees. Error is given ' +
                     'in arcminutes.A negative Error value indicates a ' +
                     'Retraction of a previous notice. That notice is NOT a' +
                     'GRB.Make sure to check the GCN website for more' +
                     'information: https://gcn.gsfc.nasa.gov/burst_info.html',
        "print_mask": ["Name", "RA", "Dec", "Time", "Error"],
        "color": 'palevioletred',
        "label": "Possible GRB",
        "marker": "+"
    }

    return GCN_dict