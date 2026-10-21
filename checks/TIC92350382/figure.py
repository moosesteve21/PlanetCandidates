"""TIC 92350382: RaymondSmith's two signals folded in the independent TARS light curves (Boyle et al. 2026),
each transit window detrended with a straight line fitted outside the transit. Writes tars_folds.png."""
from glob import glob
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits

HERE = Path(__file__).parent
SIGNALS = [("Signal 1", 2.90370, 1328.1035, 1.66, 442), ("Signal 2", 7.36659, 1325.5444, 2.51, 638)]
data = []
for path in sorted(glob(str(HERE / "mastDownload/HLSP/hlsp_tars_*/*_lc.fits"))):
    with fits.open(path) as h:
        d = h[1].data
        t, f = np.asarray(d["TIME"], float), np.asarray(d["FLUX"], float)
        q = np.asarray(d["QUALITY"]) if "QUALITY" in d.names else np.zeros(len(t))
    ok = np.isfinite(t) & np.isfinite(f) & (q == 0)
    data.append((t[ok], f[ok] / np.median(f[ok])))
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
for ax, (name, P, T0, dur_h, rep) in zip(axes, SIGNALS):
    D = dur_h / 24
    xs, ys = [], []
    for t, f in data:
        for n in np.arange(np.ceil((t.min() - T0) / P), np.floor((t.max() - T0) / P) + 1):
            dt = t - (T0 + n * P)
            win = np.abs(dt) < 3 * D
            out = win & (np.abs(dt) > 0.75 * D)
            if (win & (np.abs(dt) < 0.5 * D)).sum() < 2 or out.sum() < 10:
                continue
            c = np.polyfit(dt[out], f[out], 1)
            xs.append(dt[win] * 24); ys.append((f[win] / np.polyval(c, dt[win]) - 1) * 1e6)
    x, y = np.concatenate(xs), np.concatenate(ys)
    edges = np.arange(-3 * dur_h, 3 * dur_h + 1e-9, dur_h / 4)
    idx = np.digitize(x, edges)
    xb = np.array([x[idx == i].mean() for i in range(1, len(edges)) if (idx == i).sum() > 2])
    yb = np.array([y[idx == i].mean() for i in range(1, len(edges)) if (idx == i).sum() > 2])
    eb = np.array([y[idx == i].std() / np.sqrt((idx == i).sum()) for i in range(1, len(edges)) if (idx == i).sum() > 2])
    ax.plot(x, y, ".", color="0.8", ms=2, zorder=1)
    ax.errorbar(xb, yb, eb, fmt="o", color="k", ms=4, zorder=3, label="TARS, binned")
    ax.plot([-3 * dur_h, -dur_h / 2, -dur_h / 2, dur_h / 2, dur_h / 2, 3 * dur_h], [0, 0, -rep, -rep, 0, 0],
            color="C3", lw=1.2, zorder=2, label=f"reported depth ({rep} ppm, SPOC)")
    ax.set_ylim(-4 * rep, 3 * rep)
    ax.set_title(f"{name}: P = {P} d ({len(xs)} TARS transits)", fontsize=10)
    ax.set_xlabel("hours from mid-transit"); ax.set_ylabel("relative flux (ppm)")
    ax.legend(loc="lower left", fontsize=8)
fig.suptitle("TIC 92350382 in the independent TARS light curves", fontsize=11)
fig.tight_layout()
fig.savefig(HERE / "tars_folds.png", dpi=130)
print("wrote", HERE / "tars_folds.png")
