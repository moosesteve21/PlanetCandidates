"""Figure: the four Kepler events of KOI-5005.01 (PDCSAP and SAP), quadratic baseline, 1-h bins."""
import glob
import numpy as np
import lightkurve as lk

if not glob.glob("kepler/**/*llc.fits", recursive=True):   # Kepler long-cadence light curves from MAST
    lk.search_lightcurve("KIC 3755522", author="Kepler", cadence="long").download_all(download_dir="kepler")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
lcs = [lk.read(f, quality_bitmask="default") for f in
       sorted(glob.glob("kepler/**/*llc.fits", recursive=True))]
fig, axes = plt.subplots(2, 4, figsize=(14, 6), sharey=True, sharex=True)
k = 0
for lc in lcs:
    t = lc.time.value
    for e in range(6):
        tc = T0 + e * P
        if not (t.min() + 1 < tc < t.max() - 1):
            continue
        for row, col in enumerate(("pdcsap_flux", "sap_flux")):
            x = lc[col]
            f = np.where(np.ma.getmaskarray(x.mask), np.nan, np.asarray(x.unmasked.value, float))
            w = (np.abs(t - tc) < 1.5) & np.isfinite(f) & np.isfinite(t)
            oot = w & (np.abs(t - tc) > DUR / 2 + 0.05) & (np.abs(t - tc) < 1.0)
            r = f / np.polyval(np.polyfit(t[oot] - tc, f[oot], 2), t - tc) - 1
            h = (t[w] - tc) * 24
            ax = axes[row, k]
            ax.plot(h, r[w] * 1e6, ".", color="0.7", ms=3)
            b = np.arange(-36, 36.1, 1.0)
            i = np.digitize(h, b)
            ax.plot([h[i == j].mean() for j in range(1, len(b)) if (i == j).sum() > 1],
                    [r[w][i == j].mean() * 1e6 for j in range(1, len(b)) if (i == j).sum() > 1], "ko", ms=3)
            ax.axvspan(-DUR * 12, DUR * 12, color="tab:orange", alpha=0.12)
            ax.axvline(-24, color="0.85", lw=0.5); ax.axvline(24, color="0.85", lw=0.5)
            ax.axhline(-204, color="tab:blue", ls="--", lw=0.8)
            if row == 0:
                ax.set_title(f"Q{lc.quarter}, E{e} (BKJD {tc:.2f})", fontsize=10)
        k += 1
axes[0, 0].set_ylabel("PDCSAP (ppm)"); axes[1, 0].set_ylabel("SAP (ppm)")
for ax in axes[1]:
    ax.set_xlabel("hours from predicted mid-transit")
axes[0, 0].set_ylim(-700, 500)
fig.suptitle("KOI-5005.01 (KIC 3755522): Kepler long cadence, quadratic baseline over ±1 d (shaded: 4.74 h; dashed: 204 ppm)", fontsize=10)
fig.tight_layout()
fig.savefig("events.png", dpi=100)
