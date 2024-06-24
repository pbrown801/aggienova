# extinction code to edit 2012cg

# calling in the filters
Vdata = pd.read_csv('V_P08.txt', delim_whitespace=True, comment='#')
Vdata.columns = ['Wavelength', 'Area']

Bdata = pd.read_csv('B_P08.txt', delim_whitespace=True, comment='#')
Bdata.columns = ['Wavelength', 'Area']

Udata = pd.read_csv('U_P08.txt', delim_whitespace=True, comment='#')
Udata.columns = ['Wavelength', 'Area']

M2data = pd.read_csv('UVM2_B11.txt', delim_whitespace=True, comment='#')
M2data.columns = ['Wavelength', 'Area']

W1data = pd.read_csv('UVW1_B11.txt', delim_whitespace=True, comment='#')
W1data.columns = ['Wavelength', 'Area']

W2data = pd.read_csv('UVW2_B11.txt', delim_whitespace=True, comment='#')
W2data.columns = ['Wavelength', 'Area']

# defining the filter(s)
SWIFT_UVOT_V = Filter(Vdata.Wavelength, Vdata.Area, name='SWIFT_UVOT_V', dtype='photon', unit='Angstrom')
SWIFT_UVOT_B = Filter(Bdata.Wavelength, Bdata.Area, name='SWIFT_UVOT_B', dtype='photon', unit='Angstrom')
SWIFT_UVOT_U = Filter(Udata.Wavelength, Udata.Area, name='SWIFT_UVOT_U', dtype='photon', unit='Angstrom')
SWIFT_UVOT_M2 = Filter(M2data.Wavelength, M2data.Area, name='SWIFT_UVOT_M2', dtype='photon', unit='Angstrom')
SWIFT_UVOT_W1 = Filter(W1data.Wavelength, W1data.Area, name='SWIFT_UVOT_W1', dtype='photon', unit='Angstrom')
SWIFT_UVOT_W2 = Filter(W2data.Wavelength, W2data.Area, name='SWIFT_UVOT_W2', dtype='photon', unit='Angstrom')


# calculating the filter magnitudes
def kfun(wave, flux):
    f_v = SWIFT_UVOT_V.get_flux(wave, flux)
    f_v = -2.5 * np.log10(f_v) - SWIFT_UVOT_V.Vega_zero_mag

    f_b = SWIFT_UVOT_B.get_flux(wave, flux)
    f_b = -2.5 * np.log10(f_b) - SWIFT_UVOT_B.Vega_zero_mag

    f_u = SWIFT_UVOT_U.get_flux(wave, flux)
    f_u = -2.5 * np.log10(f_u) - SWIFT_UVOT_U.Vega_zero_mag

    f_m2 = SWIFT_UVOT_M2.get_flux(wave, flux)
    f_m2 = -2.5 * np.log10(f_m2) - SWIFT_UVOT_M2.Vega_zero_mag

    f_w1 = SWIFT_UVOT_W1.get_flux(wave, flux)
    f_w1 = -2.5 * np.log10(f_w1) - SWIFT_UVOT_W1.Vega_zero_mag

    f_w2 = SWIFT_UVOT_W2.get_flux(wave, flux)
    f_w2 = -2.5 * np.log10(f_w2) - SWIFT_UVOT_W2.Vega_zero_mag

    return np.array([f_v, f_b, f_u, f_m2, f_w1, f_w2])


# defining the values for wave and flux in the function
wave = data['SN_Wavelength'].values
flux = data['SN_Flux'].values

# defining the values for wave and flux in the function
wave = data['SN_Wavelength'].values
flux = data['SN_Flux'].values

mag = kfun(wave, flux)
print(mag)

# redshift (or de-redden) the magnitude using the extinction code, ebv=1, rv=3.1, so that av=3.1
rv = 3.1
ebv = 0.1
av = rv * ebv
mwf = extinction.apply(extinction.ccm89(wave, av, rv), flux)
