from swifttools.swift_too import Data, TOO
from swifttools.swift_too import ObsQuery
import astropy 
from astropy.time import Time

years = []
for i in range(5, 24):
    end = "-01-01 00:00:00"
    if i < 10:
        year = "200" + str(i) + end
    else:
        year = "20" + str(i) + end
    years.append(year)

example1 = "2006-01-01 00:00:00"
example2 = "2006-02-01 00:00:00"

query = ObsQuery(begin = example1, end = example2)

TOORequests(limit=20)

for entry in query.entries:
    name = entry.target_name
    id = entry.targetid
    ra = entry.ra_point
    
    dec = entry.dec_point
    
    print(name, ra, dec)