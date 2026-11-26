#!/usr/bin/env python3
"""s30_pixels.py - is the S30 dip of TIC 300164137 on the target or scattered light? (PHT 4185280, 2026-11-26)
TESScut 15x15 FFI cutout of Sector 30 (no quality mask: every cadence in the window is flagged for scattered light).
For each pixel: the transit depth at the fixed S30 time (recheck.py's QLP time) and shape, with a local linear
baseline over +-1.1 d, as a fraction of that pixel's median flux and in electrons. A transit on the target should
lose most electrons in the target's brightest pixels with the same fractional depth there; scattered light makes
background pixels (far from any star) dip as well, and by a similar number of electrons."""
import json
import numpy as np, lightkurve as lk
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
TC, T14, T12 = 2127.1586, 11.75 / 24, 0.55 / 24
tpf = lk.search_tesscut("TIC 300164137", sector=30).download(cutout_size=15, quality_bitmask="none")
t = tpf.time.value; F = tpf.flux.value.astype(float)
ok = np.isfinite(t) & np.all(np.isfinite(F.reshape(len(t), -1)), axis=1)
t, F = t[ok], F[ok]
# scattered light: subtract each image's background, the median of the faintest 30% of pixels (by median flux)
med0 = np.median(F, axis=0); bgmask = med0 < np.percentile(med0, 30)
yy, xx = np.mgrid[:F.shape[1], :F.shape[2]]
G = np.vstack([np.ones(bgmask.sum()), xx[bgmask], yy[bgmask]]).T
bgts = np.zeros(len(t))
for k in range(len(t)):      # a sloping plane per image, fitted to the faint pixels (scattered light has a gradient)
    c, *_ = np.linalg.lstsq(G, F[k][bgmask], rcond=None)
    F[k] -= c[0] + c[1] * xx + c[2] * yy; bgts[k] = c[0] + c[1] * 7 + c[2] * 7
print(f"background subtracted: sloping plane fitted to {bgmask.sum()} faint pixels per image, range {bgts.min():.0f} to {bgts.max():.0f} e/s")
print(f"cadences {len(t)}, median flux {np.nanmedian(F):.1f} e/s (non-zero check)")
w = (t - TC > -(T14 / 2 + 0.6)) & (t - TC < T14 / 2 + 0.35)   # stops before the scattered-light rise at +0.75 d
tt, FF = t[w], F[w]
x = np.abs(tt - TC); m = np.zeros_like(tt)
full = x <= T14 / 2 - T12; ing = (x > T14 / 2 - T12) & (x < T14 / 2)
m[full] = 1; m[ing] = (T14 / 2 - x[ing]) / T12
A = np.vstack([np.ones_like(tt), tt - TC, -m]).T
ny, nx = FF.shape[1:]
dep_e = np.zeros((ny, nx)); dep_f = np.zeros((ny, nx)); sig = np.zeros((ny, nx))
med = np.median(F, axis=0)
for j in range(ny):
    for i in range(nx):
        y = FF[:, j, i]
        c, res, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = y - A @ c; s = np.std(r)
        cov = np.linalg.inv(A.T @ A) * s ** 2
        dep_e[j, i] = c[2]; dep_f[j, i] = c[2] / med[j, i]; sig[j, i] = c[2] / np.sqrt(cov[2, 2])
# target pixel: the brightest pixel nearest the cutout centre
cy, cx = ny // 2, nx // 2
sub = med[cy - 1:cy + 2, cx - 1:cx + 2]; jj, ii = np.unravel_index(np.argmax(sub), sub.shape); ty, tx = cy - 1 + jj, cx - 1 + ii
bright = med > np.percentile(med, 95)
bg = med < np.percentile(med, 30)
print(f"target pixel ({tx},{ty}): median {med[ty, tx]:.0f} e/s, depth {dep_f[ty, tx]*1e6:.0f} ppm ({dep_e[ty, tx]:.1f} e/s, {sig[ty, tx]:.1f} sigma)")
ap = np.zeros_like(med, bool); ap[ty - 1:ty + 2, tx - 1:tx + 2] = True
print(f"3x3 on target: depth {dep_e[ap].sum() / med[ap].sum()*1e6:.0f} ppm of the summed flux ({dep_e[ap].sum():.1f} e/s)")
print(f"background pixels (faintest 30%, n={bg.sum()}): mean depth {dep_e[bg].mean():+.2f} e/s per pixel "
      f"(scatter {dep_e[bg].std():.2f}); median background flux {med[bg].mean():.1f} e/s")
iy, ix = np.unravel_index(np.argmax(dep_e), dep_e.shape)
print(f"largest electron loss at pixel ({ix},{iy}), {dep_e[iy, ix]:.1f} e/s, {sig[iy, ix]:.1f} sigma; "
      f"distance from target pixel {np.hypot(ix - tx, iy - ty):.1f} px")
# light-curve check of the background: sum of background pixels around the transit
bsum = FF[:, bg].mean(axis=1)
cb, *_ = np.linalg.lstsq(A, bsum, rcond=None)
print(f"mean background pixel during transit: {cb[2]:+.2f} e/s (positive = a dip like the target's)")
json.dump(dict(target_px=[int(tx), int(ty)], target_depth_ppm=float(dep_f[ty, tx] * 1e6),
               ap3x3_ppm=float(dep_e[ap].sum() / med[ap].sum() * 1e6), bg_mean_e=float(dep_e[bg].mean()),
               max_loss_px=[int(ix), int(iy)]), open("s30_pixels.json", "w"), indent=1)
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
for a_, im, ti in ((ax[0], np.log10(np.clip(med, 1, None)), "log median flux"), (ax[1], dep_e, "depth (e/s)"),
                   (ax[2], sig, "depth significance (sigma)")):
    h = a_.imshow(im, origin="lower", cmap="viridis"); plt.colorbar(h, ax=a_); a_.set_title(ti)
    a_.plot(tx, ty, "r+", ms=12)
fig.suptitle("TIC 300164137 S30: per-pixel transit depth at BTJD 2127.1586 (TESScut, no quality mask, sloping background subtracted, window -0.85 to +0.6 d)")
fig.tight_layout(); fig.savefig("s30_pixels.png", dpi=110)
tt0 = tt - TC
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(tt0, FF[:, ap].sum(axis=1) / np.median(FF[:, ap].sum(axis=1)), ".", ms=3, label="3x3 on target")
ax.plot(tt0, bsum / np.median(bsum) - 0.02, ".", ms=3, label="mean background pixel (offset -0.02)")
ax.axvspan(-T14 / 2, T14 / 2, color="0.9"); ax.set(xlabel="days from S30 transit", ylabel="relative flux"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig("s30_lc.png", dpi=110)
