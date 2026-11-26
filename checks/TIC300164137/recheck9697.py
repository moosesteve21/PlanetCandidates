#!/usr/bin/env python3
"""recheck9697.py - S96 and S97 (same method as recheck.py; asked by gulpfumetti 2026-11-26) of TIC 300164137 re-measured after DagfinnExolab's comment (PHT 4185280, 2026-11-26).
Prediction for each epoch from a cubic fit to the 19 transits used in ttv.json. Each available light curve
(SPOC / TESS-SPOC / QLP, default and no quality mask) is measured with ttv.py's fixed-shape trapezoid, scanning
+-0.6 d around the prediction (ttv.py scanned +-1.5 d around a linear ephemeris, which let S68 lock onto systematics)."""
import json
import numpy as np, lightkurve as lk
TIC, P, T0 = 300164137, 49.662, 4013.591
T14, T12 = 11.75 / 24, 0.55 / 24
rows = json.load(open("ttv.json"))
good = [x for x in rows if not x["edge"] and x["depth_ppm"] > 800 and x["red_chi2"] < 2.5 and x["sector"] != 96]   # S96: transit in the orbit gap
n = np.array([x["n"] for x in good]); tc = np.array([x["tc"] for x in good]); e = np.array([x["err_min"] for x in good])
cf = np.polyfit(n, tc, 3, w=1 / e)
res = (tc - np.polyval(cf, n)) * 1440
print(f"cubic on {len(good)} transits: rms {np.std(res):.1f} min")

def trap(t, tc_, d):
    x = np.abs(t - tc_); f = np.zeros_like(t)
    full = x <= T14 / 2 - T12; ing = (x > T14 / 2 - T12) & (x < T14 / 2)
    f[full] = d; f[ing] = d * (T14 / 2 - x[ing]) / T12
    return 1 - f

def measure(t, f, fe, tp):
    w = np.abs(t - tp) < T14 / 2 + 1.1
    tt, ff, ee = t[w], f[w], fe[w]
    cov = (np.abs(tt - tp) < T14 / 2).sum() * np.median(np.diff(tt)) / T14 if len(tt) > 30 else 0
    if len(tt) < 30:
        return None
    grid = np.arange(-0.6, 0.6, 0.001); chi = []
    for dt in grid:
        m = trap(tt, tp + dt, 1.0) - 1
        A = np.vstack([np.ones_like(tt), tt - tp, m]).T / ee[:, None]
        c, *_ = np.linalg.lstsq(A, ff / ee, rcond=None)
        chi.append(np.sum((ff / ee - A @ c) ** 2))
    chi = np.array(chi); k = int(np.argmin(chi)); dof = len(tt) - 4; red = max(chi[k] / dof, 1)
    ins = grid[(chi - chi[k]) / red <= 1]; err = (ins.max() - ins.min()) / 2 if len(ins) > 1 else 0.001
    m = trap(tt, tp + grid[k], 1.0) - 1
    A = np.vstack([np.ones_like(tt), tt - tp, m]).T / ee[:, None]
    c, *_ = np.linalg.lstsq(A, ff / ee, rcond=None)
    # significance of the dip at the best time: chi2 without the transit term
    A0 = A[:, :2]; c0, *_ = np.linalg.lstsq(A0, ff / ee, rcond=None)
    dchi = (np.sum((ff / ee - A0 @ c0) ** 2) - chi[k]) / red
    return dict(tc=tp + grid[k], dt_min=grid[k] * 1440, err_min=err * 1440, depth=c[2] / c[0] * 1e6,
                red=chi[k] / dof, dchi2=dchi, cover=cov, edge=k in (0, len(grid) - 1))

out = []
for sec, ep in ((96, -2), (97, -1)):
    tp = np.polyval(cf, ep)
    print(f"\nS{sec} n={ep}: cubic prediction BTJD {tp:.4f}")
    for r in lk.search_lightcurve(f"TIC {TIC}", sector=sec, author=["SPOC", "TESS-SPOC", "QLP"]):
        a = r.table["author"][0]
        for qm in ("default", "none"):
            try:
                lc = r.download(quality_bitmask=qm).remove_nans().normalize()
            except Exception as ex:
                print(f"  {a} {qm}: download failed ({type(ex).__name__})"); continue
            t, f = lc.time.value, lc.flux.value
            fe = lc.flux_err.value if np.isfinite(lc.flux_err.value).any() else np.full_like(f, np.nanstd(f))
            ok = np.isfinite(t) & np.isfinite(f) & np.isfinite(fe)
            m = measure(t[ok], f[ok], fe[ok], tp)
            if m is None:
                print(f"  {a:9s} mask={qm:7s}: too few points near the prediction"); continue
            print(f"  {a:9s} mask={qm:7s}: tc {m['tc']:.4f}, {m['dt_min']:+6.1f} +- {m['err_min']:4.1f} min from prediction, "
                  f"depth {m['depth']:5.0f} ppm, dchi2 {m['dchi2']:6.1f}, redchi2 {m['red']:.2f}, in-transit coverage "
                  f"{m['cover']:.0%}{'  SCAN EDGE' if m['edge'] else ''}")
            out.append(dict(sector=sec, n=ep, author=str(a), mask=qm, pred=float(tp), **{k: float(v) for k, v in m.items()}))
json.dump(out, open("recheck9697.json", "w"), indent=1)
