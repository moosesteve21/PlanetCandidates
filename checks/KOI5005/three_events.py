"""KOI-5005.01: the checks of events.py with Q4 left out (rabtsevich's question, Talk 2026-10-30): (1) the last three
events against stacks at random times; (2) a blind search of the light curve without Q4 for 3+ dips on a common
period of 200-500 d, upright and upside down, to see how the real signal ranks."""
import glob
import os
import numpy as np
import lightkurve as lk

KDIR = "kepler"
if not glob.glob(f"{KDIR}/**/*llc.fits", recursive=True):
    lk.search_lightcurve("KIC 3755522", author="Kepler", cadence="long").download_all(download_dir=KDIR)

P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
lcs = [lk.read(f, quality_bitmask="default") for f in sorted(glob.glob(f"{KDIR}/**/*llc.fits", recursive=True))]
lcs = [lc for lc in lcs if lc.quarter != 4]
rng = np.random.default_rng(1)


def depth(t, f, tc, win=1.0):
    """As events.py: quadratic baseline over +-win d, mean of the central 80% of the transit."""
    w = (np.abs(t - tc) < win) & np.isfinite(f) & np.isfinite(t)
    oot = w & (np.abs(t - tc) > DUR / 2 + 0.05)
    intr = w & (np.abs(t - tc) < 0.4 * DUR)
    if oot.sum() < 20 or intr.sum() < 4:
        return np.nan, np.nan
    c = np.polyfit(t[oot] - tc, f[oot], 2)
    r = f / np.polyval(c, t - tc) - 1
    return -np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum())


def flux(lc, col):
    x = lc[col]
    t = lc.time.value
    return t, np.where(np.ma.getmaskarray(getattr(x, "mask", np.zeros(len(t), bool))), np.nan,
                       np.asarray(getattr(x, "unmasked", x).value, float))


STEP = 0.02                                            # window spacing for the blind search, d
for col in ("pdcsap_flux", "sap_flux"):
    print(f"--- {col}, Q4 left out")
    events, pools = [], []
    for lc in lcs:
        t, f = flux(lc, col)
        for e in range(0, 6):
            tc = T0 + e * P
            if t.min() + 1 < tc < t.max() - 1:
                d, s = depth(t, f, tc)
                events.append((d, s)); pools.append((t, f, tc))
    d = np.array(events)
    wmean = np.sum(d[:, 0] / d[:, 1] ** 2) / np.sum(1 / d[:, 1] ** 2)
    werr = 1 / np.sqrt(np.sum(1 / d[:, 1] ** 2))
    print(f"   {len(d)} events: weighted mean {wmean * 1e6:.0f} +- {werr * 1e6:.0f} ppm")
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

    # blind search: box depth on a regular grid of times, then every (P, T0) with >= 3 windows in the data
    t0 = min(lc.time.value.min() for lc in lcs)
    t1 = max(lc.time.value.max() for lc in lcs)
    grid = np.arange(t0, t1, STEP)
    dg = np.full(len(grid), np.nan); sg = np.full(len(grid), np.nan)
    for lc in lcs:
        t, f = flux(lc, col)
        for i in np.where((grid > t.min() + 1) & (grid < t.max() - 1))[0]:
            dg[i], sg[i] = depth(t, f, grid[i])
    wgt = np.where(np.isfinite(dg), 1 / sg ** 2, 0.0)
    wd = np.where(np.isfinite(dg), dg / sg ** 2, 0.0)
    best = {+1: [], -1: []}                            # per period: best SNR of the stacked windows
    real = None
    periods = np.arange(200.0, 500.0, 0.01)
    for p in periods:
        nph = int(round(p / STEP))
        ncyc = int(np.ceil(len(grid) / nph))
        pad = ncyc * nph - len(grid)
        W = np.concatenate([wgt, np.zeros(pad)]).reshape(ncyc, nph)
        D = np.concatenate([wd, np.zeros(pad)]).reshape(ncyc, nph)
        n = (W > 0).sum(0)
        sw = W.sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = np.where(n >= 3, D.sum(0) / np.sqrt(sw), np.nan)
        for sgn in (+1, -1):
            best[sgn].append(np.nanmax(sgn * snr) if np.isfinite(snr).any() else np.nan)
        if abs(p - P) < 0.006:
            k = int(round(((T0 - grid[0]) % p) / STEP)) % nph
            real = np.nanmax(snr[max(k - 2, 0):k + 3])
    b_up, b_dn = np.array(best[+1]), np.array(best[-1])
    # independent peaks: best per 1-d period bin
    bins = (periods // 1).astype(int)
    up = np.array([np.nanmax(b_up[bins == b]) for b in np.unique(bins)])
    dn = np.array([np.nanmax(b_dn[bins == b]) for b in np.unique(bins)])
    print(f"   blind search 200-500 d (>= 3 windows): real signal SNR {real:.1f}")
    print(f"     upright: best {np.nanmax(up):.1f} at {periods[np.nanargmax(b_up)]:.2f} d; 1-d bins >= real "
          f"{np.sum(up >= real - 0.05)} of {len(up)}; next best away from the real period "
          f"{np.nanmax(up[np.abs(np.unique(bins) - P) > 2]):.1f}")
    print(f"     upside down: best {np.nanmax(dn):.1f} at {periods[np.nanargmax(b_dn)]:.2f} d; 1-d bins >= real "
          f"{np.sum(dn >= real - 0.05)} of {len(dn)}")
