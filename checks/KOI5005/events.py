"""KOI-5005.01 (KIC 3755522): per-event depths in Kepler long-cadence PDCSAP and SAP, and the four-event stack
against stacks at random times (same quarters, same method)."""
import glob
import numpy as np
import lightkurve as lk

if not glob.glob("kepler/**/*llc.fits", recursive=True):   # Kepler long-cadence light curves from MAST
    lk.search_lightcurve("KIC 3755522", author="Kepler", cadence="long").download_all(download_dir="kepler")

P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
files = sorted(glob.glob("kepler/**/*llc.fits", recursive=True))
lcs = [lk.read(f, quality_bitmask="default") for f in files]
rng = np.random.default_rng(1)


def depth(t, f, tc, win=1.0):
    """Box depth at tc: local quadratic baseline over +-win d (transit +-0.6*DUR... excluded), mean of the central
    80% of the transit."""
    w = (np.abs(t - tc) < win) & np.isfinite(f) & np.isfinite(t)
    oot = w & (np.abs(t - tc) > DUR / 2 + 0.05)
    intr = w & (np.abs(t - tc) < 0.4 * DUR)
    if oot.sum() < 20 or intr.sum() < 4:
        return np.nan, np.nan
    c = np.polyfit(t[oot] - tc, f[oot], 2)
    r = f / np.polyval(c, t - tc) - 1
    return -np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum())


for col in ("pdcsap_flux", "sap_flux"):
    print(f"--- {col}")
    events, pools = [], []
    for lc in lcs:
        x = lc[col]
        t = lc.time.value
        f = np.where(np.ma.getmaskarray(getattr(x, 'mask', np.zeros(len(t), bool))), np.nan,
                     np.asarray(getattr(x, 'unmasked', x).value, float))
        for e in range(0, 6):
            tc = T0 + e * P
            if t.min() + 1 < tc < t.max() - 1:
                d, s = depth(t, f, tc)
                print(f"   Q{lc.quarter} E{e} BKJD {tc:.2f}: {d * 1e6:5.0f} +- {s * 1e6:3.0f} ppm")
                events.append((d, s))
                pools.append((t, f, tc))
    d = np.array(events)
    wmean = np.sum(d[:, 0] / d[:, 1] ** 2) / np.sum(1 / d[:, 1] ** 2)
    werr = 1 / np.sqrt(np.sum(1 / d[:, 1] ** 2))
    chi2 = np.sum(((d[:, 0] - wmean) / d[:, 1]) ** 2)
    print(f"   weighted mean {wmean * 1e6:.0f} +- {werr * 1e6:.0f} ppm; chi2 {chi2:.1f} for {len(d) - 1} dof")
    # random stacks: each event's time replaced by a random time in the same quarter, away from transits
    stacks = []
    for _ in range(2000):
        vals = []
        for t, f, tc in pools:
            ok = np.isfinite(f)
            while True:
                x = rng.uniform(t[ok].min() + 1.2, t[ok].max() - 1.2)
                if abs(x - tc) > 1.2:
                    dd, ss = depth(t, f, x)
                    if np.isfinite(dd):
                        vals.append((dd, ss)); break
        v = np.array(vals)
        stacks.append(np.sum(v[:, 0] / v[:, 1] ** 2) / np.sum(1 / v[:, 1] ** 2))
    stacks = np.array(stacks)
    print(f"   random stacks: sd {stacks.std() * 1e6:.0f} ppm; real stack {wmean / stacks.std():.1f} sigma; "
          f"fraction >= real {np.mean(stacks >= wmean):.4f}; fraction <= -real (inverted) {np.mean(stacks <= -wmean):.4f}")
