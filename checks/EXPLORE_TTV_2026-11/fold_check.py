import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
tic, P, T0, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]) - 2457000, sys.argv[4]
groups = [tuple(int(x) for x in g.split("-")) for g in sys.argv[5:]]
res = lk.search_lightcurve(f"TIC {tic}", mission="TESS", author="SPOC", exptime=120)
fig, axes = plt.subplots(len(groups), 1, figsize=(8, 2.6 * len(groups)), sharex=True)
for ax, (a, b) in zip(np.atleast_1d(axes), groups):
    ph_all, f_all = [], []
    for j in range(len(res)):
        s = int(res.table["sequence_number"][j])
        if not a <= s <= b: continue
        lc = res[j].download(quality_bitmask="default").remove_nans().normalize()
        lc = lc.flatten(window_length=1441)  # ~2 d at 2 min: keeps a 5 h dip
        t = lc.time.value; f = lc.flux.value
        ph = ((t - T0) / P + 0.5) % 1 - 0.5
        ph_all.append(ph * P * 24); f_all.append(f)
    ph = np.concatenate(ph_all); f = np.concatenate(f_all)
    bins = np.arange(-P * 12, P * 12, 0.5); idx = np.digitize(ph, bins)
    med = [np.median(f[idx == k]) if np.sum(idx == k) > 5 else np.nan for k in range(1, len(bins))]
    ax.plot(ph, (f - 1) * 1e6, ",", color="0.75")
    ax.plot(bins[:-1] + 0.25, (np.array(med) - 1) * 1e6, "-", color="C3")
    ax.set_ylim(-1500, 800); ax.axvline(0, color="k", lw=0.5); ax.set_ylabel("ppm"); ax.set_title(f"sectors {a}-{b}", fontsize=9)
ax.set_xlabel("hours from ExoFOP-predicted mid-transit")
fig.tight_layout(); fig.savefig(out, dpi=100)
