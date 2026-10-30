"""TIC 149628034: Alaa_Sr's 6.767 d signal (left) folded in the independent TARS light curves (Boyle et al. 2026),
each transit window detrended with a straight line fitted outside the transit; (right) the per-source depth map's
summed chi-square for each catalogued star against its distance from the target (depth_map.txt). The TARS files
are downloaded from MAST into ~/.cache/kestrel-checks. Writes tars_depthmap.png."""
import re
from glob import glob
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits
from astroquery.mast import Observations

HERE = Path(__file__).parent
CACHE = Path.home() / ".cache/kestrel-checks"
P, T0, DUR_H, REP = 6.767344, 2148.3466, 2.81, 447

obs = Observations.query_criteria(target_name="149628034", provenance_name="TARS")
prods = Observations.get_product_list(obs)
prods = prods[[str(f).endswith("_lc.fits") and "tars" in str(f) for f in prods["productFilename"]]]
Observations.download_products(prods, download_dir=str(CACHE))
data = []
for path in sorted(glob(str(CACHE / "mastDownload/HLSP/hlsp_tars_*149628034*/*_lc.fits"))):
    with fits.open(path) as h:
        d = h[1].data
        t, f = np.asarray(d["TIME"], float), np.asarray(d["FLUX"], float)
        q = np.asarray(d["QUALITY"]) if "QUALITY" in d.names else np.zeros(len(t))
    ok = np.isfinite(t) & np.isfinite(f) & (q == 0)
    data.append((t[ok], f[ok] / np.median(f[ok])))

fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4))
D = DUR_H / 24
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
edges = np.arange(-3 * DUR_H, 3 * DUR_H + 1e-9, DUR_H / 4)
idx = np.digitize(x, edges)
use = [i for i in range(1, len(edges)) if (idx == i).sum() > 2]
xb = np.array([x[idx == i].mean() for i in use])
yb = np.array([y[idx == i].mean() for i in use])
eb = np.array([y[idx == i].std() / np.sqrt((idx == i).sum()) for i in use])
ax.errorbar(xb, yb, eb, fmt="o", color="k", ms=4, zorder=3, label="TARS, binned")
ax.plot([-3 * DUR_H, -DUR_H / 2, -DUR_H / 2, DUR_H / 2, DUR_H / 2, 3 * DUR_H], [0, 0, -REP, -REP, 0, 0],
        color="C3", lw=1.2, zorder=2, label=f"reported depth ({REP} ppm)")
ax.axhline(0, color="0.7", lw=0.8, zorder=1)
ax.set_ylim(-3 * REP, 2 * REP)
ax.set_title(f"P = {P} d in TARS ({len(xs)} transits)", fontsize=10)
ax.set_xlabel("hours from mid-transit"); ax.set_ylabel("relative flux (ppm)")
ax.legend(loc="lower left", fontsize=8)

rows = []
for line in open(HERE / "depth_map.txt"):
    m = re.match(r"\s+TIC\s+(\d+)\s+T=\s*([\d.]+)\s+([\d.]+)\"\s+dchi2 =\s+([\d.]+)", line)
    if m:
        rows.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
nodip = float(re.search(r"no dip anywhere\s+dchi2 =\s+([\d.]+)", open(HERE / "depth_map.txt").read()).group(1))
r = np.array(rows)
sc = bx.scatter(r[:, 2], r[:, 3], c=r[:, 1], cmap="viridis_r", s=40, edgecolors="k", linewidths=0.4, zorder=3)
tgt = r[:, 0] == 149628034
bx.scatter(r[tgt, 2], r[tgt, 3], marker="*", s=220, color="gold", edgecolors="k", zorder=4, label="target")
for row in r:
    if row[0] == 149628035:
        bx.annotate(f"TIC 149628035\n(T {row[1]:.1f}, {row[2]:.0f}\")", (row[2], row[3]), xytext=(12, 4),
                    textcoords="offset points", fontsize=8)
bx.axhline(nodip, color="C3", ls="--", lw=1, label=f"no dip anywhere (Δχ² {nodip:.0f})")
bx.set_xlabel("distance from target (arcsec)"); bx.set_ylabel("Δχ² vs best source (lower = better)")
bx.set_title(f"Depth map, {len(rows)} sources, TESScut cutouts of 40 sectors", fontsize=10)
bx.legend(loc="lower right", fontsize=8)
fig.colorbar(sc, ax=bx, pad=0.02).set_label("TESS magnitude")
fig.suptitle("TIC 149628034: the 6.767 d dip in TARS, and where the depth map puts it", fontsize=11)
fig.tight_layout()
fig.savefig(HERE / "tars_depthmap.png", dpi=130)
print("wrote", HERE / "tars_depthmap.png")
