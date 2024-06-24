import numpy as np
import matplotlib.pyplot as plt
from speccounts import *


#spectra_file_input = input("What spectra file do you want to use?:  (use full path) ")       # User inputs spectra file name including extension
#spectra_file_name = ('%s' % (spectra_file_input))                # Path is relative, might need to be changed for different computers 
spectra_file_name = '../spectra/SN2016ccj_hst_20160514.dat'

spectra_file_name = '../spectra/ptf11kly_20110910.obs.dat'

spectra_file_load = np.loadtxt(spectra_file_name)

#filter_file_input = input("What filter file do you want to use?: (use name in ../filters/) ")         # User inputs filter file name including extension
#filter_file_name = ('../filters/%s' % (filter_file_input))                  # Path is relative again, change as needed 
filter_file_name = ('../filters/UVW2_2010.txt')                  # Path is relative again, change as needed 
filter_file_load = np.loadtxt(filter_file_name)


wave,flux = np.loadtxt(spectra_file_name,dtype=float,usecols=(0,1),unpack=True)

specin_countsout(wave,flux)

#print('mag array')
#print(mag_array)

wavelength_spectra = []
flux_spectra = []
wavelength_filters = []
area_filters = []    

for i in range(0, len(spectra_file_load)):                                  # Reads in the data from the files, appends to empty lists above 
    wavelength_spectra.append(spectra_file_load[i][0])
for i in range(0,len(spectra_file_load)):
    flux_spectra.append(spectra_file_load[i][1])
for i in range(0, len(filter_file_load)):
    wavelength_filters.append(filter_file_load[i][0])
for i in range(0, len(filter_file_load)):
    area_filters.append(filter_file_load[i][1])

fig, axes = plt.subplots()                                                  # First plot, plots wavelength spectra against the flux 
plt.plot(wavelength_spectra, flux_spectra)
plt.xlim(1600,6000)                                                           # Limit is 20,000 so the graph is viewable 
plt.xlabel('wavelength spectra')
plt.ylabel('flux spectra')

fig, axes = plt.subplots()                                                  # Second plot, plots wavelength filters against the area filters 
plt.plot(wavelength_filters, area_filters)
plt.xlabel('wavelength_filters')
plt.ylabel('Filter Effective Area [cm^2]')

interpolated_data = np.interp(wavelength_filters, wavelength_spectra, flux_spectra)
ergs = np.array(interpolated_data) * np.array(area_filters)

integral = np.trapz(ergs, wavelength_filters)

ten_percent = (integral) * 0.1
fifty_percent = (integral) * 0.5
ninety_percent = (integral) * 0.9

ten_percent_y_vals = []
ten_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):                                 # Calculates 10% of the total area 
    if integral_test < ten_percent:
        ten_percent_y_vals.append(ergs[i])
        ten_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(ten_percent_y_vals, ten_percent_x_vals)
    else:
        break

fifty_percent_y_vals = []
fifty_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):                                 # Calculates 50% of the total area 
    if integral_test < fifty_percent:
        fifty_percent_y_vals.append(ergs[i])
        fifty_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(fifty_percent_y_vals, fifty_percent_x_vals)
    else:
        break
        
ninety_percent_y_vals = []
ninety_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):                                 # Calculates 90% of the total area 
    if integral_test < ninety_percent:
        ninety_percent_y_vals.append(ergs[i])
        ninety_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(ninety_percent_y_vals, ninety_percent_x_vals)
    else:
        break


fig, axes = plt.subplots()                                                  # Plots wavelength filters vs the interpolated data 
plt.plot(wavelength_filters, ergs)
plt.xlabel('wavelength_filters')
plt.ylabel('ergs/s/angstrom')

# Start pulling data from a second spectrum, not required for the file to work 
#spectra_file_input_2 = input("What is the second spectra file that you want to use? ")
spectra_file_input_2 = '../spectra/SN2022hrs_muv_20220426.3_10.dat'
spectra_file_name_2 = ('../spectra/%s' % (spectra_file_input_2))
spectra_file_load_2 = np.loadtxt(spectra_file_name_2)

wavelength_spectra_2 = []
flux_spectra_2 = []

for i in range(0, len(spectra_file_load_2)):
    wavelength_spectra_2.append(spectra_file_load_2[i][0])
for i in range(0,len(spectra_file_load_2)):
    flux_spectra_2.append(spectra_file_load_2[i][1])
    
interpolated_data_2 = np.interp(wavelength_filters, wavelength_spectra_2, flux_spectra_2)
ergs_2 = np.array(interpolated_data_2) * np.array(area_filters)

fig = plt.figure() 
ax=fig.add_subplot(111, label=1)
ax2=fig.add_subplot(111, label=2, frame_on=False)

ax.plot(wavelength_filters, ergs, color = 'C0', label=spectra_file_name)
ax.set_xlabel('wavelength_filter', color = 'C0')
ax.set_ylabel('ergs_1', color = 'C0')
ax.tick_params(axis='x', colors="C0")
ax.tick_params(axis='y', colors="C0")

ax2.plot(wavelength_filters, ergs_2, color = 'C3', label=spectra_file_name_2)
ax2.set_xlabel('wavelength_filter', color = 'C3')
ax2.set_ylabel('ergs_2', color = 'C3')
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='x', colors="C3")
ax2.tick_params(axis='y', colors="C3")

# mpatches not working  plot1_legend = mpatches.Patch(color='C0', label=spectra_file_input)
#plot2_legend = mpatches.Patch(color='C3', label=spectra_file_input_2)
# plt.legend(handles=[plot1_legend,plot2_legend])

plt.show()
