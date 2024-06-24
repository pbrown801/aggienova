import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_data(filename):
    # Read the file, skipping lines that start with #
    with open(filename, 'r') as file:
        lines = [line for line in file if not line.startswith('#')]
    
    from io import StringIO
    data_string = StringIO(''.join(lines))
    
    data = pd.read_csv(data_string, delim_whitespace=True,
                       names=['Filter', 'MJD', 'Mag', 'MagErr', '3SigMagLim', 'SatLim', 
                              'Rate', 'RateErr', 'Ap', 'Frametime', 'Exp', 'Telapse'])
    return data

def process_filter(data, filter_name):
    filter_data = data[data['Filter'] == filter_name]
    mjd = filter_data['MJD'].values
    mag = filter_data['Mag'].values
    mag_err = filter_data['MagErr'].values
    sig_mag_lim = filter_data['3SigMagLim'].values
    sat_lim = filter_data['SatLim'].values
    rate = filter_data['Rate'].values
    
    # Identify NULL magnitudes and replace with 3-sigma magnitude limits
    mag_null = np.isnan(mag)
    rate_null = np.isnan(rate)
    
    return mjd, mag, mag_err, sig_mag_lim, sat_lim, mag_null, rate_null

def plot_light_curve(data):
    plt.figure()
    
    filters = ['UVW2', 'UVM2', 'UVW1', 'U', 'B', 'V']
    colors = ['black', 'red', 'maroon', 'violet', 'blue', 'green']
    markers = ['o', 'v', '^', 'D', '*', 's']
    
    for filter_name, color, marker in zip(filters, colors, markers):
        mjd, mag, mag_err, sig_mag_lim, sat_lim, mag_null, rate_null = process_filter(data, filter_name)
        
        # Sort the data points by MJD
        sort_idx = np.argsort(mjd)
        mjd = mjd[sort_idx]
        mag = mag[sort_idx]
        mag_err = mag_err[sort_idx]
        sig_mag_lim = sig_mag_lim[sort_idx]
        sat_lim = sat_lim[sort_idx]
        mag_null = mag_null[sort_idx]
        rate_null = rate_null[sort_idx]
        
        # Plot detections and connect points
        plt.plot(mjd[~mag_null], mag[~mag_null], color=color, alpha=0.5)
        plt.errorbar(mjd[~mag_null], mag[~mag_null], yerr=mag_err[~mag_null], 
                     fmt=marker, color=color, label=filter_name)

        # Plot useful upper limits
        mag_null = np.logical_and(mag_null, ~rate_null)
        plt.scatter(mjd[mag_null], sig_mag_lim[mag_null], marker='v', color=color, s=100, alpha=0.5)
        
		# Plot saturation limits
        plt.scatter(mjd[rate_null], sat_lim[rate_null], marker='^', color=color, s=100, alpha=0.5)

    plt.gca().invert_yaxis()
    plt.xlabel('Modified Julian Date')
    plt.ylabel('Magnitude (AB)')
    plt.title('SN2022hrs Light Curve')
    plt.legend()

    plt.show()

filename = '../SOUSA/SN2022hrs_uvotB15.1.dat'
data = read_data(filename)
plot_light_curve(data)
