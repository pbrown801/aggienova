import matplotlib.pyplot as plt
import numpy as np

snname = 'sn name' # the name of the SN you are fitting the light curve for
path = '' # wherever you want
filename = 'sn name_uvotB15.1.dat'
savename = 'sn name_pylightcurve.jpg'
data = open(filename, 'r')

# putting in the data, note: in the open brackets you put in the numbers provided in the .dat file
# data for the UVW2 filter
uvw2mjd = []
uvw2mag = []
uvw2magerr = []

# data for the UVM2 filter
uvm2mjd = []
uvm2mag = []
uvm2magerr = []

# data for the UVW1 filter
uvw1mjd = []
uvw1mag = []
uvw1magerr =[]

#data for the U filter
umjd = []
umag = []
umagerr =[]

#data for the B filter
bmjd = []
bmag = []
bmagerr = []

#data for the V filter
vmjd = []
vmag = []
vmagerr = []

# reading the data from the file
lines = np.genfromtxt(data, dtype=[('filter', 'S4'), ('mjd', float), ('mag', float), ('maggerr', float)], usecols=(0, 1, 2, 3), unpack=True, autostrip=True)

mjd = lines[1]
mag = lines[2]
magerr = lines[3]
filters = lines[0]

# filtering out the nulls in the data so that the code doesn't crash
filterslist = []
mjdlist = []
maglist = []
magerrlist = []

for i in range(len(filters)):
  if not np.isnan(mag[i]):
    filterslist.append(filters[i])
    maglist.append(mag[i])
    magerrlist.append(magerr[i])
    mjdlist.append(mjd[i])

filters = np.array(filterslist)
mjd = np.array(mjdlist)
mag = np.array(maglist)
magerr = np.array(magerrlist)

#creating the plot
fig, ax = plt.subplots(figsize=(10, 6))

#plotting data
ax.plot(uvw2mjd, uvw2mag, linestyle='-', marker='o', label='UVW2', color='xkcd:black')
ax.plot(uvw1mjd, uvw1mag, linestyle='-', marker='v', label='UVW2', color='r')
ax.plot(uvm2mjd, uvm2mag, linestyle='-', marker='*', label='UVW2', color='xkcd:maroon')
ax.plot(umjd, umag, linestyle='-', marker='D', label='UVW2', color='xkcd:violet')
ax.plot(bmjd, bmag, linestyle='-', marker='s', label='UVW2', color='xkcd:b')
ax.plot(vmjd, vmag, linestyle='-', marker='^', label='UVW2', color='xkcd:g')

ax.set_title(f'sn name')
ax.set_xlabel('Modern Julian Date')
ax.invert_yaxis() # the lower the magnitude number is the brighter the object is
ax.legend()

# displaying the figure (good luck!)
plt.show()
