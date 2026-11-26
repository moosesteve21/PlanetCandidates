#!/usr/bin/env python3
"""plot9697.py - QLP light curves of TIC 300164137 around the cubic predictions for S96 and S97 (2026-11-26)."""
import numpy as np, lightkurve as lk
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
P = {96: 3914.3588, 97: 3963.9744}; T14 = 11.75 / 24
fig, ax = plt.subplots(2, 1, figsize=(9, 6))
for a, (s, tp) in zip(ax, P.items()):
    lc = lk.search_lightcurve("TIC 300164137", sector=s, author="QLP")[0].download(quality_bitmask="none").remove_nans().normalize()
    t, f = lc.time.value, lc.flux.value; w = np.abs(t - tp) < 3
    print(f"S{s}: {w.sum()} points within 3 d; in +-T14/2: {(np.abs(t - tp) < T14 / 2).sum()}; "
          f"data range {t.min():.2f}-{t.max():.2f}; gaps >0.5 d: {[(round(t[i],2), round(t[i+1],2)) for i in np.where(np.diff(t) > 0.5)[0]]}")
    a.plot(t[w] - tp, f[w], ".", ms=2); a.axvspan(-T14 / 2, T14 / 2, color="0.9")
    a.set(title=f"S{s} QLP, prediction BTJD {tp:.3f}", xlabel="days from prediction", ylabel="flux")
fig.tight_layout(); fig.savefig("s96_97.png", dpi=110)
