#!/usr/bin/env python3
"""oddeven_fig.py - figure for PHT 4185529 (TIC 88481081): per-transit depths (odd vs even epochs at P 1.730376 d),
and the folds of odd and even transits at 2P = 3.460752 d (primary and secondary eclipse of an EB), from SPOC PDCSAP
with a local linear baseline per transit. Usage (.venv): python oddeven_fig.py -> oddeven.png"""
import warnings; warnings.filterwarnings("ignore")
from pathlib import Path
import lightkurve as lk, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent; P, T0 = 1.730376, 4314.3121
rows = np.array([l.split()[:4] for l in (HERE / "per_transit.txt").read_text().splitlines()[1:] if l.startswith("S")])
n = rows[:, 1].astype(int); d = rows[:, 2].astype(float); e = rows[:, 3].astype(float)
X, Y, E = [], [], []
for f in sorted(HERE.rglob("*_lc.fits")):
    lc = lk.read(f); lc = lc[(lc.quality == 0) & np.isfinite(lc.flux.value)]
    t, y = lc.time.value, lc.flux.value / np.nanmedian(lc.flux.value)
    for k in range(int(np.ceil((t.min() - T0) / P)), int(np.floor((t.max() - T0) / P)) + 1):
        x = t - (T0 + k * P); w = np.abs(x) < 4 / 24; b = (np.abs(x) > 1.5 / 24) & w
        if b.sum() < 60: continue
        c = np.polyfit(x[b], y[b], 1); X.append(x[w] * 24); Y.append(y[w] / np.polyval(c, x[w])); E.append(np.full(w.sum(), k))
X, Y, E = map(np.concatenate, (X, Y, E))
fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
for par, col, lab in ((0, "C0", "even epochs"), (1, "C3", "odd epochs")):
    m = n % 2 == par; ax[0].errorbar(n[m], d[m], e[m], fmt="o", color=col, ms=4, label=f"{lab}: {np.average(d[m], weights=1/e[m]**2):.0f} ppm")
    mm = E % 2 == par; bins = np.linspace(-4, 4, 97); i = np.digitize(X[mm], bins)
    yb = [np.median(Y[mm][i == j]) if (i == j).sum() > 5 else np.nan for j in range(1, len(bins))]
    ax[1].plot(0.5 * (bins[1:] + bins[:-1]), (1 - np.array(yb)) * 1e6, "-", color=col, label=lab)
ax[0].set(xlabel="epoch (P = 1.730376 d)", ylabel="depth (ppm), local baseline", title="TIC 88481081, SPOC S105-S108: depth per transit")
ax[0].legend(); ax[1].invert_yaxis(); ax[1].legend()
ax[1].set(xlabel="hours from mid-eclipse", ylabel="flux deficit (ppm), 5-min medians", title="odd vs even transits = two eclipses at 2P = 3.4608 d")
fig.tight_layout(); fig.savefig(HERE / "oddeven.png", dpi=110)
