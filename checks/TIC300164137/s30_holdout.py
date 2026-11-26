#!/usr/bin/env python3
"""s30_holdout.py - is the S30 background control independent, and how sensitive is the 3x3 depth to the settings?
(2026-11-26, before replying to DagfinnExolab). s30_pixels.py checked the mean of the same faint pixels the background
plane was fitted to, which is close to zero by construction. Here the faint pixels are split in a checkerboard: the
plane is fitted to one half and the transit depth is measured in the other (held-out) half, both ways round. Then the
3x3 depth is repeated for sky-pixel fractions 20/30/40% and several windows."""
import numpy as np, lightkurve as lk
TC, T14, T12 = 2127.1586, 11.75 / 24, 0.55 / 24
tpf = lk.search_tesscut("TIC 300164137", sector=30).download(cutout_size=15, quality_bitmask="none")
t = tpf.time.value; F0 = tpf.flux.value.astype(float)
ok = np.isfinite(t) & np.all(np.isfinite(F0.reshape(len(t), -1)), axis=1); t, F0 = t[ok], F0[ok]
yy, xx = np.mgrid[:15, :15]; med0 = np.median(F0, axis=0)
def model(tt):
    x = np.abs(tt - TC); m = np.zeros_like(tt); full = x <= T14 / 2 - T12; ing = (x > T14 / 2 - T12) & (x < T14 / 2)
    m[full] = 1; m[ing] = (T14 / 2 - x[ing]) / T12; return m
def subtract(fitmask):
    G = np.vstack([np.ones(fitmask.sum()), xx[fitmask], yy[fitmask]]).T; F = F0.copy()
    for k in range(len(t)):
        c, *_ = np.linalg.lstsq(G, F0[k][fitmask], rcond=None); F[k] -= c[0] + c[1] * xx + c[2] * yy
    return F
def depth(y, pre, post):
    w = (t - TC > -pre) & (t - TC < post); tt, yy_ = t[w], y[w]
    A = np.vstack([np.ones_like(tt), tt - TC, -model(tt)]).T; c, *_ = np.linalg.lstsq(A, yy_, rcond=None)
    r = yy_ - A @ c; cov = np.linalg.inv(A.T @ A) * np.var(r, ddof=3); return c[2], np.sqrt(cov[2, 2])
faint = med0 < np.percentile(med0, 30); cb = (xx + yy) % 2 == 0
F = subtract(faint); med = np.median(F, axis=0)
cy = cx = 7; sub = med[6:9, 6:9]; j, i = np.unravel_index(np.argmax(sub), sub.shape); ty, tx = 6 + j, 6 + i
ap = np.zeros((15, 15), bool); ap[ty - 1:ty + 2, tx - 1:tx + 2] = True
PRE, POST = T14 / 2 + 0.6, T14 / 2 + 0.35
d, e = depth(F[:, faint].mean(axis=1), PRE, POST)
print(f"as posted (same pixels fitted and tested): faint-pixel mean depth {d:+.2f} +- {e:.2f} e/s/pixel")
for name, fit, test in (("fit black, test white", faint & cb, faint & ~cb), ("fit white, test black", faint & ~cb, faint & cb)):
    Fh = subtract(fit); d, e = depth(Fh[:, test].mean(axis=1), PRE, POST)
    da, ea = depth(Fh[:, ap].sum(axis=1), PRE, POST)
    print(f"{name}: held-out mean depth {d:+.2f} +- {e:.2f} e/s/pixel ({d/e:+.1f} sigma); "
          f"3x3 {da / np.median(Fh[:, ap].sum(axis=1)) * 1e6:.0f} ppm ({da/ea:.1f} sigma)")
# medium-brightness ring pixels (not used in the fit, >=4 px from target) as a second held-out control
ring = ~faint & (np.hypot(xx - tx, yy - ty) >= 4) & (med0 < np.percentile(med0, 70))
d, e = depth(F[:, ring].mean(axis=1), PRE, POST)
print(f"pixels 30-70th percentile, >=4 px from target (n={ring.sum()}, not in fit): mean depth {d:+.2f} +- {e:.2f} e/s/pixel; "
      f"target pixel loses {depth(F[:, ty, tx], PRE, POST)[0]:.1f} e/s")
print("\n3x3 depth (ppm) by sky fraction and window:")
for pc in (20, 30, 40):
    Fp = subtract(med0 < np.percentile(med0, pc)); s = Fp[:, ap].sum(axis=1); m0 = np.median(s)
    row = []
    for pre, post in ((0.6, 0.35), (0.85, 0.35), (0.4, 0.35), (0.6, 0.2), (0.6, 0.5)):
        da, ea = depth(s, T14 / 2 + pre, T14 / 2 + post); row.append(f"-{T14/2+pre:.2f}/+{T14/2+post:.2f} d: {da/m0*1e6:5.0f} ({da/ea:3.1f}s)")
    print(f"  sky {pc}% (n={(med0 < np.percentile(med0, pc)).sum()}): " + "; ".join(row))
