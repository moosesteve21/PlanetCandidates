"""KOI-5005.01: which windows make the strongest upside-down peaks of three_events.py's blind search (PDCSAP, Q4 out),
and the same search scored by each chain's third-strongest window. Run three_events.py first (it downloads the data)."""
import glob
import numpy as np
import lightkurve as lk

KDIR = "kepler"
P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
lcs = [lk.read(f, quality_bitmask="default") for f in sorted(glob.glob(f"{KDIR}/**/*llc.fits", recursive=True))]
lcs = [lc for lc in lcs if lc.quarter != 4]


def depth(t, f, tc, win=1.0):
    w = (np.abs(t - tc) < win) & np.isfinite(f) & np.isfinite(t)
    oot = w & (np.abs(t - tc) > DUR / 2 + 0.05)
    intr = w & (np.abs(t - tc) < 0.4 * DUR)
    if oot.sum() < 20 or intr.sum() < 4:
        return np.nan, np.nan
    c = np.polyfit(t[oot] - tc, f[oot], 2)
    r = f / np.polyval(c, t - tc) - 1
    return -np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum())


STEP = 0.02
t0 = min(lc.time.value.min() for lc in lcs); t1 = max(lc.time.value.max() for lc in lcs)
grid = np.arange(t0, t1, STEP)
dg = np.full(len(grid), np.nan); sg = np.full(len(grid), np.nan); qg = np.zeros(len(grid), int)
for lc in lcs:
    t = lc.time.value; x = lc["pdcsap_flux"]
    f = np.where(np.ma.getmaskarray(x.mask), np.nan, np.asarray(x.unmasked.value, float))
    for i in np.where((grid > t.min() + 1) & (grid < t.max() - 1))[0]:
        dg[i], sg[i] = depth(t, f, grid[i]); qg[i] = lc.quarter
z = dg / sg
peaks = []
for p in np.arange(200.0, 500.0, 0.01):
    nph = int(round(p / STEP)); ncyc = int(np.ceil(len(grid) / nph)); pad = ncyc * nph - len(grid)
    W = np.concatenate([np.where(np.isfinite(dg), 1 / sg ** 2, 0), np.zeros(pad)]).reshape(ncyc, nph)
    D = np.concatenate([np.where(np.isfinite(dg), dg / sg ** 2, 0), np.zeros(pad)]).reshape(ncyc, nph)
    n = (W > 0).sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        snr = np.where(n >= 3, -D.sum(0) / np.sqrt(W.sum(0)), np.nan)
    k = np.nanargmax(snr); peaks.append((snr[k], p, k))
peaks.sort(reverse=True)
seen = []
for s, p, k in peaks:
    if any(abs(p - q) < 1 for q in seen):
        continue
    seen.append(p)
    idx = [k + c * int(round(p / STEP)) for c in range(20) if k + c * int(round(p / STEP)) < len(grid)]
    idx = [i for i in idx if np.isfinite(dg[i])]
    print(f"inverted SNR {s:.1f} at P {p:.2f} d: windows " + ", ".join(
        f"Q{qg[i]} BKJD {grid[i]:.2f} ({-dg[i] * 1e6:+.0f} ppm, {-z[i]:+.1f} sig)" for i in idx))
    if len(seen) == 6:
        break

# fairer score: the third-strongest single window of the chain (all three must be strong on their own)
print("\nscore = third-strongest window (sigma), 200-500 d, best per 1-d period bin")
zz = np.where(np.isfinite(z), z, np.nan)
res = {+1: {}, -1: {}}
for p in np.arange(200.0, 500.0, 0.01):
    nph = int(round(p / STEP)); ncyc = int(np.ceil(len(grid) / nph)); pad = ncyc * nph - len(grid)
    Z = np.concatenate([zz, np.full(pad, np.nan)]).reshape(ncyc, nph)
    for sgn in (+1, -1):
        s = np.sort(np.where(np.isfinite(Z), sgn * Z, -np.inf), axis=0)[::-1]
        third = s[2] if ncyc >= 3 else np.full(nph, -np.inf)
        k = int(np.argmax(third)); b = int(p)
        if third[k] > res[sgn].get(b, (-np.inf,))[0]:
            res[sgn][b] = (third[k], p)
for sgn, name in ((+1, "upright"), (-1, "upside down")):
    v = sorted(res[sgn].values(), reverse=True)
    real = res[+1][int(P)][0] if sgn == +1 else None
    print(f"  {name}: top " + ", ".join(f"{a:.1f} at {p:.2f} d" for a, p in v[:4]))
r = res[+1][int(P)][0]
for sgn, name in ((+1, "upright"), (-1, "upside down")):
    n = sum(1 for b, (a, p) in res[sgn].items() if a >= r and not (sgn == 1 and b == int(P)))
    print(f"  {name}: other 1-d bins with third window >= real ({r:.1f} sigma): {n} of 300")
