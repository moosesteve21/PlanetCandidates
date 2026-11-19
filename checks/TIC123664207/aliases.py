#!/usr/bin/env python3
"""aliases.py - TIC 123664207 (TOI-2493.01, PHT 4185323): which periods P = 237.13/k fit the three posted transits
(S33 2225.81, S98 4043.47, S107 4280.60 BTJD), and which of them the other TESS data rule out. For each surviving alias,
every predicted transit falling in data gets a box depth (T14 6.07 h, local linear baseline); a period is ruled out
when a transit with >= 50% coverage reads depth + 3 sigma below half the posted depth."""
import numpy as np, lightkurve as lk, json, sys
OUT = sys.argv[1]
T = np.array([2225.81, 4043.47, 4280.60]); DEP, T14 = 1835e-6, 6.07 / 24
sr = lk.search_lightcurve("TIC 123664207", author=["SPOC", "TESS-SPOC", "QLP"])
best = {}
for i, r in enumerate(sr):
    s = int(r.table["sequence_number"][0]); a = r.table["author"][0]; e = float(r.table["exptime"][0])
    rank = (["SPOC", "TESS-SPOC", "QLP"].index(a), e)
    if s not in best or rank < best[s][0]: best[s] = (rank, i, a)
data = []
for s in sorted(best):
    try:
        lc = sr[best[s][1]].download(quality_bitmask="default").remove_nans().normalize()
        data.append((s, best[s][2], lc.time.value, lc.flux.value))
    except Exception as ex:
        print(f"S{s}: download failed ({type(ex).__name__})")
print("sectors:", " ".join(f"S{s}({a[0]})" for s, a, *_ in data))
def depth(tc):
    for s, a, t, f in data:
        w = np.abs(t - tc) < T14 / 2 + 0.5
        if not w.any(): continue
        tt, ff = t[w], f[w]; inn = np.abs(tt - tc) < T14 / 2 * 0.8
        cad = np.median(np.diff(t)); cov = inn.sum() * cad / (0.8 * T14)
        if cov < 0.5 or (~inn).sum() < 10: return s, cov, None, None
        A = np.vstack([np.ones_like(tt), tt - tc, inn.astype(float)]).T
        c, *_ = np.linalg.lstsq(A, ff, rcond=None); r = ff - A @ c
        sig = np.std(r) * np.sqrt(1 / inn.sum() + 1 / (~inn).sum())
        return s, cov, -c[2], sig
    return None
# confirm the three posted transits
for tc in T:
    d = depth(tc); print(f"posted transit {tc}: " + (f"S{d[0]} depth {d[2]*1e6:.0f} +- {d[3]*1e6:.0f} ppm" if d and d[2] is not None else str(d)))
out = []
for k in range(1, 40):
    P = (T[2] - T[1]) / k
    m = (T[1] - T[0]) / P
    if abs(m - round(m)) * P > 1.0: continue          # rough match to S33; the refit below must fit all three
    # refit linear ephemeris through the three transits
    n = np.array([0, round(m), round(m) + k]); A = np.vstack([np.ones(3), n]).T
    t0, Pf = np.linalg.lstsq(A, T, rcond=None)[0]
    res = np.max(np.abs(T - (t0 + n * Pf))) * 24
    if res > 3: continue                               # all three within 3 h of a linear ephemeris
    tmin, tmax = min(t.min() for *_, t, f in data), max(t.max() for *_, t, f in data)
    kill, checked = [], 0
    for e in range(int(np.floor((tmin - t0) / Pf)), int(np.ceil((tmax - t0) / Pf)) + 1):
        tc = t0 + e * Pf
        if np.min(np.abs(T - tc)) < 0.5: continue
        d = depth(tc)
        if not d or d[2] is None: continue
        checked += 1
        if d[2] + 3 * d[3] < 0.5 * DEP: kill.append(f"S{d[0]}@{tc:.2f} ({d[2]*1e6:.0f}±{d[3]*1e6:.0f})")
        elif d[2] > 3 * d[3]: kill.append(f"DIP? S{d[0]}@{tc:.2f} ({d[2]*1e6:.0f}±{d[3]*1e6:.0f})")
    status = "ruled out" if any(not x.startswith("DIP") for x in kill) else ("SURVIVES" if checked else "untested")
    print(f"P = {Pf:8.4f} d (k={k}, fit resid {res:.1f} h): {checked} other epochs in data; {status}; {'; '.join(kill[:3])}")
    out.append(dict(k=k, P=Pf, checked=checked, status=status, notes=kill))
json.dump(out, open(f"{OUT}/aliases.json", "w"), indent=1)
