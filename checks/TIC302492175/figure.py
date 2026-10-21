"""TIC 302492175 (HD 35956): the Sector 32 event (BTJD 2179.40) in three reductions, with the momentum dump that ends it, and the Sector 98 time the
41.6538 d period predicts (BTJD 4012.17). Each panel: flux relative to a line fitted 4-12 h either side, 30-min bins."""
import warnings, numpy as np; warnings.filterwarnings("ignore")
import lightkurve as lk
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
HERE = Path(__file__).parent
def panel(ax, t, f, tc, title, color):
    dt = (t - tc) * 24; w = np.abs(dt) < 14; base = w & (np.abs(dt) > 4)
    c = np.polyfit(dt[base], f[base], 1); r = (f[w] / np.polyval(c, dt[w]) - 1) * 1e6; x = dt[w]
    ax.plot(x, r, ".", color="0.82", ms=2)
    e = np.arange(-14, 14.01, 0.5); i = np.digitize(x, e)
    xb = [x[i == k].mean() for k in range(1, len(e)) if (i == k).sum() > 2]
    yb = [r[i == k].mean() for k in range(1, len(e)) if (i == k).sum() > 2]
    eb = [r[i == k].std() / np.sqrt((i == k).sum()) for k in range(1, len(e)) if (i == k).sum() > 2]
    ax.errorbar(xb, yb, eb, fmt="o", ms=3.5, color=color)
    ax.axvspan(-2.5, 2.5, color="C1", alpha=0.08); ax.axhline(0, color="0.5", lw=0.7)
    ax.set_ylim(-600, 400); ax.set_title(title, fontsize=9); ax.set_xlabel("hours from BTJD %.2f" % tc)
    if abs(tc - 2179.40) < 0.01:                     # the Sector 32 momentum dump (quality bit 32) at BTJD 2179.491
        ax.axvline((2179.491 - tc) * 24, color="C3", lw=1.2, ls="--")
        ax.text((2179.491 - tc) * 24 + 0.4, 330, "momentum\ndump", color="C3", fontsize=8, va="top")
sr32 = lk.search_lightcurve("TIC 302492175", sector=32); sr98 = lk.search_lightcurve("TIC 302492175", sector=98)
spoc = sr32[(sr32.table["author"] == "SPOC") & (sr32.table["exptime"] == 120)][0].download(download_dir=str(HERE))
tspoc = sr32[sr32.table["author"] == "TESS-SPOC"][0].download(download_dir=str(HERE))
s98 = sr98[(sr98.table["author"] == "SPOC") & (sr98.table["exptime"] == 120)][0].download(download_dir=str(HERE))
fig, axes = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
def tf(lc, col):
    t = np.asarray(lc.time.value, float); f = np.asarray(lc[col].value, float); ok = np.isfinite(f); return t[ok], f[ok]
panel(axes[0], *tf(spoc, "pdcsap_flux"), 2179.40, "S32 SPOC 2-min, PDCSAP", "k")
panel(axes[1], *tf(spoc, "sap_flux"), 2179.40, "S32 SPOC 2-min, SAP (raw)", "C0")
panel(axes[2], *tf(tspoc, "pdcsap_flux"), 2179.40, "S32 TESS-SPOC 10-min (separate reduction)", "C2")
panel(axes[3], *tf(s98, "pdcsap_flux"), 4012.17, "S98 SPOC 2-min: predicted by P = 41.6538 d", "C3")
axes[0].set_ylabel("relative flux (ppm)")
fig.suptitle("TIC 302492175 (HD 35956): the Sector 32 event in three reductions, and where a 41.65 d period points", fontsize=11)
fig.tight_layout(); fig.savefig(HERE / "event_s32.png", dpi=120); print("wrote", HERE / "event_s32.png")
