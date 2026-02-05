import swifttools
from swifttools.swift_too import Swift_ObsQuery
from swifttools.swift_too import Swift_TOO
#from swifttools.swift_too import Swift_ObsQuery
#from swifttools.swift_too import ObsQuery
from astropy.coordinates import SkyCoord
import astropy.units as u
import ast as a

too=Swift_TOO()

too.username = "anonymous"
too.shared_secret = "anonymous"

snlist = []
snfile = open('sn2025list.txt', 'w')
filename = 'template2025list.csv'
# CSV formatting: SNname,targetids,SNra,SNdec,template status

with open(filename, 'r') as f:
    file = f.read().split("\n")
    for k in range(len(file)):
        file[k] = file[k].split(",")
        if k != 0:
            c = SkyCoord(file[k][2] + " " + file[k][3], unit=(u.hourangle, u.deg))
            file[k][2] = c.ra.degree #SNra at line k turned into degrees
            file[k][3] = c.dec.degree #SNdec at line k turned into degrees
            name = file[k][0] #SNname at line k
            year = file[k][0][2:6] #4 digit year in the SNname at line k
            snfile.write(str(file[k]))
            snfile.write('\n')

snfile.close()

output = open('outputsn2025.csv', 'w')
# snlist.txt is basically just a txt file where each line is a list. I reformatted the data in the csv in the above
# and wrote it to the text file to make my life easier when checking if the code was wrong.
with open('sn2025list.txt', 'r') as f:
    file = f.read().split('\n')
    output.write(f'SNName,RA(deg),DEC(deg),observed,yearchecked\n')
    for k in range(len(file) - 1):
        obj = a.literal_eval(file[k])
        name = obj[0]
        year = obj[0][2:6]
        query = swifttools.swift_too.Swift_ObsQuery()
        query.ra, query.dec = float(obj[2]), float(obj[3])
        query.radius = 6 / 60  # 6 arcminutes
        query.username = "anonymous"

        if query.submit():
            print(f"Query succeeded for {obj[0]}")
        else:
            print(f"Query failed for {obj[0]}")
        listsn = str(query).split('\n')
        querylist = []
        for k in range(len(listsn)):
            if listsn[k].startswith("|"):
                c = listsn[k].split('|')
                for k in range(len(c)):
                    c[k] = c[k].strip()
                querylist.append(c)
        found = False
        for k in range(len(querylist)):
            if k != 0:
                if int(querylist[k][2][0:4]) >= int(year) + 1: # int(year) + number is the minimum year looking past.
                    found = True

                if int(querylist[k][2][0:4]) < int(year) : # int(year)is the minimum year looking before.
                    found = True

        print(f"{obj[0]} observed within year range boolean = {found}")
        output.write(f'{name},{float(obj[2])},{float(obj[3])},{found},{year}\n')

output.close()
print("closed")
