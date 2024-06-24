# extinction code to edit 2012cg
import pandas as pd
import extinction

#calling in your file and reading it with pandas
file = 'your_file.dat'
data = pd.read_csv(file, sep='\s+')
data.columns = ['SN_Wavelength', 'SN_Flux']

# defining the values for wave and flux in the function
wave = data['SN_Wavelength'].values
flux = data['SN_Flux'].values

# redshift (or de-redden) the magnitude using the extinction code; if you're eyeballing it, use rv = 3.1, but mess around with ebv
rv = 3.1
ebv = 0.1
av = rv * ebv
mwf = extinction.apply(extinction.ccm89(wave, av, rv), flux)
