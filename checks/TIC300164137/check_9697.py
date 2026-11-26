#!/usr/bin/env python3
"""check_9697.py - sanity checks on the S96/S97 statements before posting (2026-11-26).
S96: where is the data gap, is it an orbit boundary (QLP orbitid), and does the time move if the baseline may step
across the gap? S97: is the swing in the background (sap_bkg), and is a dip at the prediction recovered with a
higher-order baseline?"""
import numpy as np, lightkurve as lk
T14, T12 = 11.75 / 24, 0.55 / 24
PRED = {96: 3914.3588, 97: 3963.9744}
def trap(t, tc):
    x = np.abs(t - tc); m = np.zeros_like(t)
    full = x <= T14 / 2 - T12; ing = (x > T14 / 2 - T12) & (x < T14 / 2)
    m[full] = 1; m[ing] = (T14 / 2 - x[ing]) / T12
    return -m
def scan(t, f, tp, base):
    best = None
    for dt in np.arange(-0.6, 0.6, 0.002):
        A = np.column_stack(base + [trap(t, tp + dt)])
        c, *_ = np.linalg.lstsq(A, f, rcond=None); chi = np.sum((f - A @ c) ** 2)
        if best is None or chi < best[0]: best = (chi, dt, c[-1])
    B = np.column_stack(base); c0, *_ = np.linalg.lstsq(B, f, rcond=None); chi0 = np.sum((f - B @ c0) ** 2)
    s2 = best[0] / (len(t) - len(base) - 2)
    return best[1] * 1440, best[2] * 1e6, (chi0 - best[0]) / s2
for s in (96, 97):
    lc = lk.search_lightcurve("TIC 300164137", sector=s, author="QLP")[0].download(quality_bitmask="none")
    tab = lc.to_table() if hasattr(lc, "to_table") else lc
    print(f"\nS{s}: columns with bkg/orbit: {[c for c in lc.colnames if 'bkg' in c.lower() or 'orbit' in c.lower()]}")
    t = lc.time.value; f = np.asarray(lc.flux.value, float); ok = np.isfinite(t) & np.isfinite(f); tp = PRED[s]
    g = np.where(np.diff(t[ok]) > 0.04)[0]
    for i in g:
        a, b = t[ok][i], t[ok][i + 1]
        if abs(a - tp) < 3 or abs(b - tp) < 3:
            ob = [int(np.asarray(lc["orbitid"].value)[ok][k]) for k in (i, i + 1)] if "orbitid" in lc.colnames else "n/a"
            print(f"  gap {a:.3f}-{b:.3f} ({(b-a)*24:.1f} h, {a-tp:+.3f} to {b-tp:+.3f} d from prediction), orbitid either side {ob}")
    w = ok & (np.abs(t - tp) < T14 / 2 + 1.1); tt = t[w]; ff = f[w] / np.nanmedian(f[w])
    one = np.ones_like(tt); x = tt - tp
    print("  single linear baseline:   dt {:+7.1f} min, depth {:6.0f} ppm, dchi2 {:6.1f}".format(*scan(tt, ff, tp, [one, x])))
    if s == 96 and len(g):
        ia = [i for i in g if abs(t[ok][i] - tp) < 1][0]; tg = t[ok][ia]
        after = (tt > tg).astype(float)
        print("  step allowed at the gap:  dt {:+7.1f} min, depth {:6.0f} ppm, dchi2 {:6.1f}".format(*scan(tt, ff, tp, [one, x, after])))
        print("  step + slope change:      dt {:+7.1f} min, depth {:6.0f} ppm, dchi2 {:6.1f}".format(*scan(tt, ff, tp, [one, x, after, after * x])))
    if s == 97:
        for d in (2, 3, 4, 5):
            print(f"  poly degree {d} baseline:  " + "dt {:+7.1f} min, depth {:6.0f} ppm, dchi2 {:6.1f}".format(*scan(tt, ff, tp, [x ** k for k in range(d + 1)])))
        for c in [c for c in lc.colnames if 'bkg' in c.lower()]:
            bk = np.asarray(lc[c].value, float)[w]
            print(f"  {c}: within +-1.35 d range {np.nanmin(bk):.1f} to {np.nanmax(bk):.1f}; corr with flux {np.corrcoef(bk[np.isfinite(bk)], ff[np.isfinite(bk)])[0,1]:+.2f}")
        ww = ok & (np.abs(t - tp) < 3); f3 = f[ww] / np.nanmedian(f[ww])
        print(f"  flux range within +-3 d: {f3.min():.3f} to {f3.max():.3f} ({(f3.max()-f3.min())*100:.1f}% peak to peak)")
# S96 step model: step size and time error (delta chi2 = 1, scaled by reduced chi2)
lc = lk.search_lightcurve("TIC 300164137", sector=96, author="QLP")[0].download(quality_bitmask="none")
t = lc.time.value; f = np.asarray(lc.flux.value, float); ok = np.isfinite(t) & np.isfinite(f); tp = PRED[96]
w = ok & (np.abs(t - tp) < T14 / 2 + 1.1); tt = t[w]; ff = f[w] / np.nanmedian(f[w]); x = tt - tp
after = (tt > 3914.3).astype(float); base = [np.ones_like(tt), x, after]
grid = np.arange(-0.6, 0.6, 0.001); chi = []; cs = []
for dt in grid:
    A = np.column_stack(base + [trap(tt, tp + dt)]); c, *_ = np.linalg.lstsq(A, ff, rcond=None)
    chi.append(np.sum((ff - A @ c) ** 2)); cs.append(c)
chi = np.array(chi); k = chi.argmin(); s2 = chi[k] / (len(tt) - 5); ins = grid[(chi - chi[k]) / s2 <= 1]
print(f"\nS96 step model: dt {grid[k]*1440:+.1f} min (+{(ins.max()-grid[k])*1440:.1f}/-{(grid[k]-ins.min())*1440:.1f}), "
      f"step {cs[k][2]*100:+.2f}%, depth {cs[k][3]*1e6:.0f} ppm")
