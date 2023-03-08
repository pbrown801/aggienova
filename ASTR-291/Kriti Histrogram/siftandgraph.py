"""
Stefan Salaices, Kriti 

The purpose of this program is to sift through a list 
of objects and clean it up. We removed hashtags, duplicates,
looked for and assigned years for each object type.
"""

import matplotlib.pyplot as plt

with open('snlist.txt','r') as file:
    snlist = file.readlines()

strippedlines = [sn.strip() for sn in snlist] #removes spaces on each line

years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
years = [str(year) for year in years] 
newlist = [] #empty list we'll add objects that meet the criteria

for line in strippedlines: #go through doc
    try:

        if line.startswith("#"): #remove all commented lines
            print(f"Removed {line}")
            continue

        for year in years: #if it has a year clearly in it like "SN2020jf"
            if year in line:
                newlist.append(f"{year}, {line}") #adding to the list
                continue

        #special cases in which full years do not appear
        if "ASASSN-" in line: 
            year = line[7:9] #extract 2 digits of year "19, etc"
            year = int(year) + 2000
            newlist.append(f"{year}, {line}")  

        if "Gaia" in line:
            year = line[4:6]
            year = int(year) + 2000
            newlist.append(f"{year}, {line}") 

    except:
        print(f"{line} did not process")

cleanedlist = [*set(newlist)] #set kills duplicates, but I want it as a list
cleanedlist.sort()

with open("updatedlist.txt", "w") as nl: #write lines to other text file
    for line in cleanedlist:
        nl.write(line + "\n")

#extracting years and graphing
yearcountlist = []
for year in years:
    yearcount = 0 
    for line in cleanedlist:
        if line[:4] == str(year):
            yearcount += 1
    yearcountlist.append(yearcount)

plt.figure(figsize=(18, 14))
plt.bar(years, yearcountlist, color="slateblue", label="Count")
plt.title("Swift Observations")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend(loc="upper left")
plt.show()

#print(f"Removed {len(newlist) - len(cleanedlist)} duplicates.")