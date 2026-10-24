"""
temperature_arrays.py

REQUIRES: uvot_magnitudes.py in the same folder (or on the Python path), plus the
aggienova filters/ and spectra/ folders. Run:  python blackbody_colors.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")     
import matplotlib.pyplot as plt

from uvot_magnitudes import (FILTER_FILES, PARSEC_CM, blackbody_flux, find_repo_root, measure_magnitudes)

# ----------------------------------------------------------------------------
# SETTINGS -- edit these
# ----------------------------------------------------------------------------
TEMPERATURES = np.arange(3000, 40001, 500)   # Kelvin: 3000, 3500, ..., 40000
RADIUS_CM = 1e15                              # blackbody radius  [cm]
DISTANCE_MPC = 10.0                           # distance          [Mpc] 
WAVE = np.arange(100.0, 30000.0, 5.0)         # wavelength grid [Angstrom]; spans all six filters
OUTPUT_PNG = "blackbody_colors_vs_temperature.png"
OUTPUT_CSV = "blackbody_magnitudes_colors.csv"

repo = find_repo_root()
filter_names = list(FILTER_FILES)                 # ['UVW2','UVM2','UVW1','U','B','V']
distance_cm = DISTANCE_MPC * 1e6 * PARSEC_CM

mags = np.full((len(TEMPERATURES), len(filter_names)), np.nan)

for i, T in enumerate(TEMPERATURES):
    flux = blackbody_flux(WAVE, T, RADIUS_CM, distance_cm)     # Planck spectrum [erg/s/cm^2/A]
    result = measure_magnitudes(WAVE, flux, repo)              # dict of results per filter
    mags[i, :] = [result[f]["vega_mag"] for f in filter_names]

col = {name: mags[:, k] for k, name in enumerate(filter_names)}

m2_w1 = col["UVM2"] - col["UVW1"]
w1_b = col["UVW1"] - col["B"]
b_v = col["B"] - col["V"]

table = np.column_stack([TEMPERATURES, mags, m2_w1, w1_b, b_v])
header = "T_K," + ",".join(filter_names) + ",UVM2-UVW1,UVW1-B,B-V"
np.savetxt(OUTPUT_CSV, table, delimiter=",", header=header, comments="", fmt="%.4f")

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.plot(TEMPERATURES, m2_w1, color="tab:purple", lw=2, label="UVM2 $-$ UVW1  (m2$-$w1)")
ax.plot(TEMPERATURES, w1_b, color="tab:blue", lw=2, label="UVW1 $-$ B  (w1$-$b)")
ax.plot(TEMPERATURES, b_v, color="tab:green", lw=2, label="B $-$ V  (b$-$v)")
ax.set_xlabel("Blackbody temperature (K)")
ax.set_ylabel("Color (Vega magnitudes)")
ax.set_title("Swift/UVOT colors of a blackbody vs. temperature")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=200)

print(f"{'T [K]':>8}{'m2-w1':>9}{'w1-b':>9}{'b-v':>9}")
for T, a, b, c in list(zip(TEMPERATURES, m2_w1, w1_b, b_v))[::6]:
    print(f"{T:>8.0f}{a:>9.3f}{b:>9.3f}{c:>9.3f}")
print(f"\nSaved plot -> {OUTPUT_PNG}\nSaved table -> {OUTPUT_CSV}")
