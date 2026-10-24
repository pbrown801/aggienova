'''
blackbody_specphot.py
 
Place this file in the aggienova/pythoncode/ directory alongside specin_countsout.py.
Run from that directory so that relative paths to ../filters/ and ../spectra/ resolve correctly.
 
Usage:
    python blackbody_specphot.py
 
Output:
    - Blackbody spectrum plot
    - UVOT synthetic counts and Vega magnitudes printed to terminal
'''
 
import numpy as np
import matplotlib.pyplot as plt
from specin_countsout import specin_countsout
 
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
h = 6.62607015e-27    # erg s
c = 2.99792458e10     # cm/s
k = 1.380649e-16      # erg/K
 
# ---------------------------------------------------------------------------
# User input
# ---------------------------------------------------------------------------
T = float(input("Enter temperature in Kelvin: "))
 
# ---------------------------------------------------------------------------
# Blackbody spectrum
# Wavelength range chosen to cover all 6 UVOT filters
# ---------------------------------------------------------------------------
l_a = np.linspace(100, 30000, 10000)   # wavelength in Angstrom
l_cm = l_a * 1e-8                      # convert to cm for Planck formula
 
exponent = h * c / (l_cm * k * T)
# Planck function in erg/s/cm^2/cm/sr, multiplied by pi for hemispherical flux
flux_per_cm = np.pi * (2 * h * c**2 / l_cm**5) / (np.exp(exponent) - 1)
 
# Conversion
flux = flux_per_cm * 1e-8              # erg/s/cm^2/Ang
 
# ---------------------------------------------------------------------------
# Plot the blackbody spectrum
# ---------------------------------------------------------------------------
plt.figure(figsize=(9, 6))
plt.plot(l_a, flux, color='darkorange')
plt.xlabel("Wavelength (Å)")
plt.ylabel(r"Flux density (erg s$^{-1}$ cm$^{-2}$ Å$^{-1}$)")
plt.title(f"Blackbody Spectrum at T = {T:.0f} K")
plt.grid(alpha=0.3)
 
# Mark the UVOT filter effective wavelengths for reference
filter_names      = ['UVW2', 'UVM2', 'UVW1', 'U',    'B',    'V'   ]
filter_eff_waves  = [2030,   2231,   2634,   3501,   4329,   5402  ]
for w, name in zip(filter_eff_waves, filter_names):
    plt.axvline(w, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
    plt.text(w + 30, plt.ylim()[1] * 0.95, name, fontsize=7,
             color='gray', rotation=90, va='top')
 
plt.tight_layout()
plt.savefig("blackbody_spectrum.png", dpi=150)
plt.show()
 
# ---------------------------------------------------------------------------
# Synthetic photometry via specin_countsout
# Passes the blackbody (l_a, flux) directly
# ---------------------------------------------------------------------------
counts, mags = specin_countsout(l_a, flux)
wien = 2.898e7 / T

# ---------------------------------------------------------------------------
# Print results (delete)
# ---------------------------------------------------------------------------
print(f"\nBlackbody T = {T:.0f} K  —  Synthetic UVOT Photometry")
print(f"{'Filter':<8} {'Counts':>15}   {'Vega Mag':>9}")
print("-" * 38)
for name, cnt, mag in zip(filter_names, counts, mags):
    print(f"{name:<8} {cnt:>15.4e}   {mag:>9.4f}")
 
# Wien peak for reference
print(f"\nWien peak wavelength : {wien:.0f} Å")
print(f"Bolometric flux (σT⁴): {5.670374419e-5 * T**4:.4e} erg/s/cm²")
