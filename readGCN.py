from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
from astropy.time import Time
import astropy.units as u
import numpy as np

def readGCN(RA, DEC, ERR, RA1, RA2, start, stop, tel):
    
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
    
    sock = urlopen(htmlAddress)
    htmlSource = sock.read() 
    sock.close()
    parsed_html = BeautifulSoup(htmlSource, "lxml")

    table = parsed_html.body.find("table")
    rows = table.findAll('tr')

    triggerN = []
    burstDate = []
    burstTime = []
    RAs = []
    Decs = []
    Error = []

    for row in rows:
        cols = row.findAll("td")
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 1:
            triggerN.append(cols[trigInd])
            burstDate.append(cols[dateInd])
            burstTime.append(cols[timeInd])
            RAs.append(cols[raInd])
            Decs.append(cols[decInd])
            Error.append(cols[errorInd])
            
    for i in range(len(triggerN)):
        if((triggerN[i] == '') or (RAs[i] == '') or (Decs[i] == '') or (burstDate[i] == '') or \
           (burstTime[i] == '') or (Error[i] == '')):
            RAs[i] = 500
            Decs[i] = 500
            burstDate[i] = '00/6/6'
            burstTime[i] = '00:00:00'
        triggerN[i] = tel + ' ' + triggerN[i]
        burstTime[i] = '20' + burstDate[i] + ' ' + burstTime[i]
        burstTime[i] = burstTime[i].replace('/', '-')

    burstTime = Time(burstTime, format = 'iso', scale = 'utc')
    t1 = start - 300 * u.s
    t2 = stop + 300 * u.s
    
    triggerN = np.asarray(triggerN)
    burstTime = np.asarray(burstTime)
    RAs = np.asarray(RAs)
    Decs = np.asarray(Decs)
    Error = np.asarray(Error)
    
    RAs = RAs.astype('float')
    Decs = Decs.astype('float')
    
    RAs[RAs < RA1] += 360
    RAs[RAs > RA2] -= 360
    
    mask = (((RAs - RA) ** 2 + (Decs - DEC) ** 2) <= (ERR ** 2)) & (t1 < burstTime) & (burstTime < t2)
    
    triggerN = triggerN[mask]
    burstTime = burstTime[mask]
    RAs = RAs[mask]
    Decs = Decs[mask]
    Error = Error[mask]
        
    return triggerN, burstTime, RAs, Decs, Error