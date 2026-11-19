#!/usr/bin/env python3
"""per_transit.py - depth of each transit of TIC 88481081 from un-flattened SPOC PDCSAP, with a local linear baseline
(1.5-4 h either side of mid); odd/even from these; and the SAP_BKG level in vs out per transit.
Usage (.venv): python per_transit.py -> per_transit.txt"""
import warnings; warnings.filterwarnings("ignore")
from pathlib import Path
import lightkurve as lk, numpy as np
HERE = Path(__file__).resolve().parent; P, T0, H = 1.730376, 4314.3121, 1.58 / 24
out = []
def say(s): print(s); out.append(s)
rows = []
for fpath in sorted(HERE.rglob("*_lc.fits")):
    lc = lk.read(fpath); lc = lc[(lc.quality == 0) & np.isfinite(lc.flux.value)]
    t, f = lc.time.value, lc.flux.value / np.nanmedian(lc.flux.value); b = lc.sap_bkg.value
    for n in range(int(np.ceil((t.min() - T0) / P)), int(np.floor((t.max() - T0) / P)) + 1):
        tc = T0 + n * P; x = t - tc
        intr = np.abs(x) < 0.35 * H; base = (np.abs(x) > 1.5 / 24) & (np.abs(x) < 4 / 24)
        if intr.sum() < 15 or base.sum() < 60 or (x[base] < 0).sum() < 25 or (x[base] > 0).sum() < 25: continue
        c = np.polyfit(x[base], f[base], 1); r = f[base] - np.polyval(c, x[base])
        d = 1 - np.mean(f[intr] / np.polyval(c, x[intr])); de = np.std(r) / np.sqrt(intr.sum())
        rows.append((lc.sector, n, d, de, np.mean(b[intr]) - np.median(b[base]), np.median(b[base])))
say("sector epoch depth_ppm err bkg_in-out bkg_level (e-/s)")
for s, n, d, de, db, bl in rows: say(f"S{s} {n:5d} {d*1e6:7.0f} {de*1e6:5.0f} {db:7.1f} {bl:8.1f}")
R = np.array([(n, d, de) for s, n, d, de, *_ in rows])
w = 1 / R[:, 2] ** 2
for name, m in (("odd", R[:, 0] % 2 == 1), ("even", R[:, 0] % 2 == 0)):
    mu = np.sum(R[m, 1] * w[m]) / np.sum(w[m]); se = np.sqrt(1 / np.sum(w[m]))
    chi = np.sum((R[m, 1] - mu) ** 2 * w[m]) / (m.sum() - 1)
    say(f"{name}: {m.sum()} transits, {mu*1e6:.0f} ± {se*1e6:.0f} ppm (x sqrt(chi2r) {np.sqrt(max(chi,1))*se*1e6:.0f}), chi2r {chi:.2f}")
(HERE / "per_transit.txt").write_text("\n".join(out) + "\n")
