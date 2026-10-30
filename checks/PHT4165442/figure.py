"""TIC 306990399 (TOI-5034), PHT Talk 4165442: the 4.705 d signal (HakimG) and the 13.375 d signal (SPOC TCE 2, sectors
1-96) folded in the independent TARS light curves (Boyle et al. 2026), each transit window detrended with a straight
line fitted outside the transit, with the transits of the other two signals (and TOI-5034.01, 8.704 d) masked.
The TARS files are downloaded from MAST into ~/.cache/kestrel-checks. Writes tars_folds.png."""
from glob import glob
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits
from astroquery.mast import Observations

HERE = Path(__file__).parent
CACHE = Path.home() / ".cache/kestrel-checks"
# name, P, T0 (BTJD), T14 (h), depth (ppm): KESTREL's global fits
SIGNALS = [("4.705 d signal", 4.70516, 1633.1298, 2.81, 1354), ("13.375 d signal (SPOC TCE 2)", 13.37537, 1631.5190, 4.05, 1752)]
TOI01 = (8.70397, 1637.28164, 3.75)

obs = Observations.query_criteria(target_name="306990399", provenance_name="TARS")
prods = Observations.get_product_list(obs)
prods = prods[[str(f).endswith("_lc.fits") and "tars" in str(f) for f in prods["productFilename"]]]
Observations.download_products(prods, download_dir=str(CACHE))
data = []
for path in sorted(glob(str(CACHE / "mastDownload/HLSP/hlsp_tars_*306990399*/*_lc.fits"))):
    with fits.open(path) as h:
        d = h[1].data
        t, f = np.asarray(d["TIME"], float), np.asarray(d["FLUX"], float)
        q = np.asarray(d["QUALITY"]) if "QUALITY" in d.names else np.zeros(len(t))
    ok = np.isfinite(t) & np.isfinite(f) & (q == 0)
    data.append((t[ok], f[ok] / np.median(f[ok])))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for k, (ax, (name, P, T0, dur_h, rep)) in enumerate(zip(axes, SIGNALS)):
    others = [s for j, s in enumerate(SIGNALS) if j != k] + [("", *TOI01, 0)]
    D = dur_h / 24
    xs, ys = [], []
    for t, f in data:
        m = np.ones(len(t), bool)
        for _, p, t0, dh, _ in others:
            m &= np.abs((t - t0 + p / 2) % p - p / 2) > 0.75 * dh / 24
        for n in np.arange(np.ceil((t.min() - T0) / P), np.floor((t.max() - T0) / P) + 1):
            dt = t - (T0 + n * P)
            win = m & (np.abs(dt) < 3 * D)
            out = win & (np.abs(dt) > 0.75 * D)
            if (win & (np.abs(dt) < 0.5 * D)).sum() < 2 or out.sum() < 10:
                continue
            c = np.polyfit(dt[out], f[out], 1)
            xs.append(dt[win] * 24); ys.append((f[win] / np.polyval(c, dt[win]) - 1) * 1e6)
    x, y = np.concatenate(xs), np.concatenate(ys)
    edges = np.arange(-3 * dur_h, 3 * dur_h + 1e-9, dur_h / 4)
    idx = np.digitize(x, edges)
    use = [i for i in range(1, len(edges)) if (idx == i).sum() > 2]
    xb = np.array([x[idx == i].mean() for i in use])
    yb = np.array([y[idx == i].mean() for i in use])
    eb = np.array([y[idx == i].std() / np.sqrt((idx == i).sum()) for i in use])
    ax.errorbar(xb, yb, eb, fmt="o", color="k", ms=4, zorder=3, label="TARS, binned")
    ax.plot([-3 * dur_h, -dur_h / 2, -dur_h / 2, dur_h / 2, dur_h / 2, 3 * dur_h], [0, 0, -rep, -rep, 0, 0],
            color="C3", lw=1.2, zorder=2, label=f"KESTREL fit depth ({rep} ppm)")
    ax.axhline(0, color="0.7", lw=0.8, zorder=1)
    ax.set_ylim(-2.5 * rep, 1.5 * rep)
    ax.set_title(f"{name}: P = {P} d ({len(xs)} TARS transits)", fontsize=10)
    ax.set_xlabel("hours from mid-transit"); ax.set_ylabel("relative flux (ppm)")
    ax.legend(loc="lower left", fontsize=8)
fig.suptitle("TIC 306990399 (TOI-5034) in the independent TARS light curves (other signals masked)", fontsize=11)
fig.tight_layout()
fig.savefig(HERE / "tars_folds.png", dpi=130)
print("wrote", HERE / "tars_folds.png")
