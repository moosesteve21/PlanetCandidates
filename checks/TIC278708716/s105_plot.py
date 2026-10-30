"""Figure: the two S105 transits of TIC 278708716 in TESScut 3x3-pixel photometry, with the depth from the other
sectors marked."""
import numpy as np
import lightkurve as lk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P, T0, HALF, DEPTH = 17.21424, 3904.1943, 2.0 / 24, 2672e-6   # global fit (S28, S68, S95)
tpf = lk.search_tesscut("TIC 278708716", sector=105).download(cutout_size=15)
tpf = tpf[(tpf.quality == 0) & np.isfinite(tpf.flux.value).all(axis=(1, 2))]
t, img = tpf.time.value, tpf.flux.value
med = np.nanmedian(img, axis=0)
bkg = np.nanmedian(img[:, med < np.nanpercentile(med, 30)], axis=1)
yy, xx = np.indices(med.shape)
ap = (abs(yy - 7) <= 1) & (abs(xx - 8) <= 1)                  # target on pixel (8, 7)
f = img[:, ap].sum(1) - bkg * ap.sum()

fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
for ax, e, label in zip(axes, (18, 19), ("22 Jun 2026", "9 Jul 2026")):
    tc = T0 + e * P
    w = np.abs(t - tc) < 0.5
    oot = w & (np.abs(t - tc) > HALF + 0.05)
    intr = np.abs(t - tc) < HALF * 0.75
    r = f / np.polyval(np.polyfit(t[oot] - tc, f[oot], 1), t - tc) - 1
    d, sig = -np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum())
    h = (t[w] - tc) * 24
    ax.plot(h, r[w] * 1e3, ".", color="0.75", ms=3)
    bins = np.arange(-12, 12.01, 0.5)
    idx = np.digitize(h, bins)
    bh = [h[idx == i].mean() for i in range(1, len(bins)) if (idx == i).sum() > 3]
    bf = [r[w][idx == i].mean() * 1e3 for i in range(1, len(bins)) if (idx == i).sum() > 3]
    ax.plot(bh, bf, "o", color="k", ms=4, label="30-min bins")
    ax.axhline(-DEPTH * 1e3, color="tab:blue", ls="--", lw=1, label="2.67 ppt (S28, S68, S95 fit)")
    ax.axvspan(-HALF * 24, HALF * 24, color="tab:orange", alpha=0.12)
    ax.set_title(f"S105, {label} (BTJD {tc:.2f}): {d * 1e3:.1f} ± {sig * 1e3:.1f} ppt")
    ax.set_xlabel("hours from predicted mid-transit")
    ax.set_ylim(-8, 6)
axes[0].set_ylabel("relative flux (ppt)")
axes[0].legend(loc="lower left", fontsize=8)
fig.suptitle("TIC 278708716: TESScut 3×3-pixel photometry, quality-flagged cadences removed, linear baseline", fontsize=10)
fig.tight_layout()
fig.savefig("s105_transits.png", dpi=110)
