"""
Stefan Salaices, Kevin Lee
Supernova Type Pie Chart
Extracting data from a provided CSV file into a pie chart.
"""


import csv
import matplotlib.pyplot as plt
import numpy as np

with open("NewSwiftSNweblist.csv", "r") as data: # csv reader
    rows = csv.reader(data, delimiter = ",") 

    
    Ia = []
    Ib = []
    Ic = []

    for row in rows:
        for item in row:
            name = row[0]
            SNtype = row[3]

        if (SNtype == "Ia"):
            Ia.append(name)

        if (SNtype == "Ib"):
            Ib.append(name)

        if (SNtype == "Ic"):
            Ic.append(name)

    #charting
    lIa = len(Ia)
    lIb = len(Ib)
    lIc = len(Ic)
    total = lIa + lIb + lIc

    y = np.array([lIa/total, lIb/total, lIc/total])
    mylabels = ["Ia", "Ib", "Ic"]
    myexplode = [.2, 0, 0]
    plt.pie(y, labels = mylabels, explode = myexplode, shadow = True)
    plt.show() 

print(f"Ia: {len(Ia)}\nIb: {len(Ib)}\nIc: {len(Ic)}")