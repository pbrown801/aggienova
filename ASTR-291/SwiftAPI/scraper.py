from bs4 import BeautifulSoup
import requests

url = "https://www.swift.psu.edu/toop/summary.php"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

"""
#searches for year button
years = doc.find("form")
for year in years:
    print(year)
"""

trs = doc.find_all("tr") #finds every tr tag

too = [] #empty list of objects
interests = []

for tr in trs[4:]: #iterate through each object of interest 
    tds = tr.contents #object's data (everything)
    data = []
    for td in tds[1:5]: #name, primary, right ascension, declination
        td = (td.string).strip()
        data.append(td)

        if td[:2] == "SN": #if it starts with 
            interests.append(td)

    too.append(data) #add that data to the object list

for to in too:
    #print(f"\n")
    print(to)

# for interest in interests:
#     print(f"\n")
#     print(interest)

# Starts with SN
# Starts with AT
# Starts with a year   ie 2022vqz
# Starts with ZTF
# Starts with iPTF
# Starts with PTF
# Starts with ASASSN
# Starts with DLT