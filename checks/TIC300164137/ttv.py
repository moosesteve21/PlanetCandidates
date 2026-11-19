#!/usr/bin/env python3
"""ttv.py - per-transit mid-times for TIC 300164137 (PHT 4185280): fixed-shape trapezoid, free mid-time and depth
scale, local linear baseline; chi2 scan over +-0.6 d; error from delta-chi2 = 1 (scaled by reduced chi2 if > 1)."""
import sys, json
import numpy as np, lightkurve as lk
TIC, P, T0 = 300164137, 49.662, 4013.591
T14, T12 = 11.75 / 24, 0.55 / 24
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
sr = lk.search_lightcurve(f"TIC {TIC}", author=["SPOC", "TESS-SPOC", "QLP"])
best = {}
for i, r in enumerate(sr):
    s = int(r.table["sequence_number"][0]); a = r.table["author"][0]; e = float(r.table["exptime"][0])
    rank = (["SPOC", "TESS-SPOC", "QLP"].index(a), e)
    if s not in best or rank < best[s][0]: best[s] = (rank, i, a)
def trap(t, tc, d):
    x = np.abs(t - tc); f = np.zeros_like(t)
    full = x <= T14 / 2 - T12; ing = (x > T14 / 2 - T12) & (x < T14 / 2)
    f[full] = d; f[ing] = d * (T14 / 2 - x[ing]) / T12
    return 1 - f
rows = []
for s in sorted(best):
    _, i, a = best[s]
    try:
        lc = sr[i].download(quality_bitmask="default").remove_nans().normalize()
    except Exception as ex:
        print(f"S{s} {a}: download failed ({type(ex).__name__})"); continue
    t, f = lc.time.value, lc.flux.value
    fe = lc.flux_err.value if np.isfinite(lc.flux_err.value).any() else np.full_like(f, np.nanstd(f))
    ok = np.isfinite(t) & np.isfinite(f) & np.isfinite(fe); t, f, fe = t[ok], f[ok], fe[ok]
    n0, n1 = int(np.ceil((t.min() - T0) / P)), int(np.floor((t.max() - T0) / P))
    for n in range(n0, n1 + 1):
        tp = T0 + n * P
        w = np.abs(t - tp) < T14 / 2 + 1.5 + 0.5
        if w.sum() < 30: continue
        tt, ff, ee = t[w], f[w], fe[w]
        inside = np.abs(tt - tp) < T14 / 2 + 0.6
        if (np.abs(tt - tp) < T14 / 2).sum() < 0.5 * T14 / np.median(np.diff(tt)):   # need half the transit covered
            print(f"S{s} n={n}: transit poorly covered, skipped"); continue
        grid = np.arange(-1.5, 1.5, 0.002); chi = []
        for dt in grid:
            m = trap(tt, tp + dt, 1.0) - 1      # shape (negative inside)
            A = np.vstack([np.ones_like(tt), tt - tp, m]).T / ee[:, None]
            c, *_ = np.linalg.lstsq(A, ff / ee, rcond=None)
            chi.append(np.sum((ff / ee - A @ c) ** 2))
        chi = np.array(chi); k = int(np.argmin(chi)); dof = len(tt) - 4
        red = max(chi[k] / dof, 1.0)
        dc = (chi - chi[k]) / red
        inside1 = grid[dc <= 1]
        err = (inside1.max() - inside1.min()) / 2 if len(inside1) > 1 else 0.002
        m = trap(tt, tp + grid[k], 1.0) - 1
        A = np.vstack([np.ones_like(tt), tt - tp, m]).T / ee[:, None]
        c, *_ = np.linalg.lstsq(A, ff / ee, rcond=None); depth = c[2] / c[0] * 1e6
        edge = k in (0, len(grid) - 1)
        rows.append(dict(sector=int(s), author=str(a), n=int(n), tc=float(tp + grid[k]), oc_min=float(grid[k] * 1440),
                         err_min=float(err * 1440), depth_ppm=float(depth), red_chi2=float(chi[k] / dof), edge=bool(edge)))
        print(f"S{s:3d} {a:9s} n={n:4d} tc={tp+grid[k]:.4f} O-C {grid[k]*1440:+7.1f} +- {err*1440:5.1f} min  "
              f"depth {depth:6.0f} ppm  redchi2 {chi[k]/dof:.2f}{'  AT SCAN EDGE' if edge else ''}")
json.dump(rows, open(f"{OUT}/ttv.json", "w"), indent=1)
# linear ephemeris refit and a sinusoid search on O-C
r = [x for x in rows if not x["edge"] and x["depth_ppm"] > 800 and x["red_chi2"] < 2.5]
n = np.array([x["n"] for x in r]); tc = np.array([x["tc"] for x in r]); e = np.array([x["err_min"] for x in r]) / 1440
W = 1 / e ** 2; A = np.vstack([np.ones_like(n), n]).T
cov = np.linalg.inv(A.T @ (A * W[:, None])); p = cov @ (A.T @ (W * tc))
oc = (tc - A @ p) * 1440; chi_lin = np.sum((oc / (e * 1440)) ** 2)
print(f"\nlinear ephemeris ({len(r)} transits): P = {p[1]:.5f} +- {np.sqrt(cov[1,1]):.5f} d, T0 = {p[0]:.4f} +- {np.sqrt(cov[0,0]):.4f}")
print(f"O-C rms {np.std(oc):.1f} min; chi2 {chi_lin:.1f} for {len(r)-2} dof (p-value tests a constant period)")
from scipy.stats import chi2 as C
print(f"p(constant period) = {C.sf(chi_lin, len(r)-2):.2e}")
best_s = None
for Pt in np.linspace(3 * P, 2.5 * (n.max() - n.min()) * P, 3000):
    ph = 2 * np.pi * (tc - p[0]) / Pt
    B = np.vstack([np.ones_like(n), n, np.sin(ph), np.cos(ph)]).T
    cB = np.linalg.lstsq(B * np.sqrt(W)[:, None], tc * np.sqrt(W), rcond=None)[0]
    ch = np.sum(((tc - B @ cB) / e) ** 2)
    if best_s is None or ch < best_s[0]: best_s = (ch, Pt, np.hypot(cB[2], cB[3]) * 1440)
print(f"best sinusoid: super-period {best_s[1]:.0f} d, semi-amplitude {best_s[2]:.1f} min, chi2 {best_s[0]:.1f} "
      f"for {len(r)-4} dof (vs {chi_lin:.1f} linear)")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 4))
ax.errorbar(tc - 2457000 if tc[0] > 2e6 else tc, oc, e * 1440, fmt="o", ms=4)
ax.axhline(0, color="k", lw=0.5); ax.set(xlabel="Mid-time (BTJD)", ylabel="O - C (min)",
       title=f"TIC {TIC}: per-transit O-C vs linear P = {p[1]:.4f} d")
fig.tight_layout(); fig.savefig(f"{OUT}/oc.png", dpi=120)
