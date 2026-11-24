#!/usr/bin/env python
"""Re-measure transit times of TOIs from TESS light curves, independently of any timing library.

Written 2026-11-24 to check the TTV candidates in an EXPLORE report (TOI-1287.01, -475.01, -6973.01, -2556.01,
-2892.01), which used the LcTools TOI timing library. Here every time is measured from the light curves.

Method
- Light curves: lightkurve, one per sector, preferring SPOC 120 s, then TESS-SPOC, then QLP (PDCSAP/KSPSAP flux,
  default quality mask). Times are BTJD (BJD_TDB - 2457000).
- Transit shape: a symmetric trapezoid with the ExoFOP duration T14 and an ingress/egress of INGRESS_FRAC x T14,
  fixed for every transit. Only the mid-time, the depth and a local cubic baseline are fitted. A fixed shape is
  enough for timing: a wrong ingress shape moves the time of a symmetric transit by much less than its error.
- Per transit: a matched-filter scan over the WHOLE orbit (trial mid-times every STEP across +-P/2 of the predicted
  time), so a transit is found wherever it is. At each trial the data within +-HW of the trial time are fitted with
  a cubic baseline + depth x shape (linear least squares) and, separately, with the cubic alone; the detection
  statistic is dchi2 = chi2(cubic) - chi2(cubic + transit), counted only for positive depths and when the window
  covers >= 70% of the transit and >= 50% of each side. The best trial is refined by a parabola. The 1-sigma error
  is where dchi2 falls by 1 from its peak (after scaling by the local reduced chi2 when > 1). A transit is used
  when its peak dchi2 >= MIN_DCHI2. dchi2_pred is the best value within +-1 h of the ExoFOP prediction.
- Per sector: the dchi2 scans of all transits in the sector are summed for a common offset (like a per-sector
  ephemeris, which is close to what the timing library provides), so shallow transits add up.
- Ephemeris: weighted linear fit to the per-transit times. Report O-C, chi2/dof, and the half peak-to-peak O-C of
  the per-sector times.

Usage: .venv/bin/python investigations/ttv_remeasure.py OUTDIR TOI:TIC:P_d:T0_bjd:T14_h [...]
"""
import csv
import json
import sys
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
import lightkurve as lk  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

STEP = 2.0 / 1440     # d, grid step of trial mid-times
INGRESS_FRAC = 0.15
MIN_DCHI2 = 25.0      # per-transit detection threshold (~5 sigma)
PREF = [("SPOC", 120), ("TESS-SPOC", None), ("QLP", None)]


def trapezoid(t, tc, t14):
    x = np.abs(t - tc)
    ting = INGRESS_FRAC * t14
    half = t14 / 2
    s = np.zeros_like(t)
    s[x <= half - ting] = 1.0
    m = (x > half - ting) & (x < half)
    s[m] = (half - x[m]) / ting
    return s


def fit_at(t, f, w, tc, t14, t_ref):
    """Linear LSQ: f = cubic(t - t_ref) - depth * shape. Returns chi2, depth."""
    dt = t - t_ref
    A = np.vstack([np.ones_like(dt), dt, dt**2, dt**3, -trapezoid(t, tc, t14)]).T
    Aw = A * w[:, None]
    coef, *_ = np.linalg.lstsq(Aw, f * w, rcond=None)
    r = (f - A @ coef) * w
    return float(r @ r), float(coef[-1])


def chi2_null(t, f, w, t_ref):
    dt = t - t_ref
    A = np.vstack([np.ones_like(dt), dt, dt**2, dt**3]).T
    coef, *_ = np.linalg.lstsq(A * w[:, None], f * w, rcond=None)
    r = (f - A @ coef) * w
    return float(r @ r)


def refine(grid, chi2):
    i = int(np.argmin(chi2))
    best = grid[i]
    if 0 < i < len(grid) - 1:
        a, b, c = chi2[i - 1], chi2[i], chi2[i + 1]
        den = a - 2 * b + c
        if den > 0:
            best = grid[i] + 0.5 * STEP * (a - c) / den
    return best, i


def error_from(grid, chi2, i, scale):
    c = chi2 / scale
    lvl = c[i] + 1.0
    lo = i
    while lo > 0 and c[lo] < lvl:
        lo -= 1
    hi = i
    while hi < len(c) - 1 and c[hi] < lvl:
        hi += 1
    return max((grid[hi] - grid[lo]) / 2, STEP / 2)


def load(tic):
    res = lk.search_lightcurve(f"TIC {tic}", mission="TESS")
    tab = res.table
    chosen = {}
    for author, exptime in PREF:
        for j in range(len(res)):
            if np.ma.is_masked(tab["sequence_number"][j]) or np.ma.is_masked(tab["exptime"][j]):
                continue
            a = str(tab["author"][j]); s = int(tab["sequence_number"][j]); e = float(tab["exptime"][j])
            if a != author or (exptime and e != exptime) or s in chosen:
                continue
            if author == "SPOC" and e != 120:
                continue
            chosen[s] = j
    out = []
    for s, j in sorted(chosen.items()):
        try:
            lc = res[j].download(quality_bitmask="default")
        except Exception as ex:  # noqa: BLE001
            print(f"  sector {s}: download failed ({ex})", flush=True)
            continue
        lc = lc.remove_nans().normalize()
        t = np.asarray(lc.time.value, float); f = np.asarray(lc.flux.value, float)
        e = np.asarray(lc.flux_err.value, float)
        ok = np.isfinite(t) & np.isfinite(f) & np.isfinite(e) & (e > 0)
        out.append((s, str(tab["author"][j]), float(tab["exptime"][j]), t[ok], f[ok], e[ok]))
        print(f"  sector {s}: {tab['author'][j]} {tab['exptime'][j]:.0f} s, {ok.sum()} points", flush=True)
    return out


def scan(t, f, e, mid, P, t14, cad):
    """dchi2 at every trial offset in [-P/2, P/2) around mid; NaN where coverage is poor."""
    hw = 1.5 * t14 + 0.1
    offs = np.arange(-P / 2, P / 2, STEP)
    out = np.full(len(offs), np.nan); depth = np.full(len(offs), np.nan); scl = np.ones(len(offs))
    m_all = np.abs(t - mid) <= P / 2 + hw
    t, f, e = t[m_all], f[m_all], e[m_all]
    if len(t) < 20:
        return offs, out, depth, scl
    order = np.argsort(t); t, f, e = t[order], f[order], e[order]
    for k, d in enumerate(offs):
        tc = mid + d
        lo, hi = np.searchsorted(t, [tc - hw, tc + hw])
        if hi - lo < 15:
            continue
        tw, fw, ew = t[lo:hi], f[lo:hi], e[lo:hi]
        inn = np.sum(np.abs(tw - tc) < t14 / 2) * cad / t14
        left = np.sum((tw < tc - t14 / 2)) * cad / (hw - t14 / 2)
        right = np.sum((tw > tc + t14 / 2)) * cad / (hw - t14 / 2)
        if inn < 0.7 or left < 0.5 or right < 0.5:
            continue
        w = 1 / ew
        c1, dep = fit_at(tw, fw, w, tc, t14, tc)
        c0 = chi2_null(tw, fw, w, tc)
        s_ = max(c1 / max(len(tw) - 5, 1), 1.0)
        if dep > 0:
            out[k] = (c0 - c1) / s_
        else:
            out[k] = 0.0
        depth[k] = dep; scl[k] = s_
    return offs, out, depth, scl


def peak(offs, d):
    if not np.any(np.isfinite(d)):
        return np.nan, np.nan, np.nan, -1
    i = int(np.nanargmax(d)); best = offs[i]
    if 0 < i < len(d) - 1 and np.isfinite(d[i - 1]) and np.isfinite(d[i + 1]):
        a, b, c = d[i - 1], d[i], d[i + 1]
        den = a - 2 * b + c
        if den < 0:
            best = offs[i] + 0.5 * STEP * (a - c) / den
    lo = i
    while lo > 0 and np.isfinite(d[lo]) and d[lo] > d[i] - 1:
        lo -= 1
    hi = i
    while hi < len(d) - 1 and np.isfinite(d[hi]) and d[hi] > d[i] - 1:
        hi += 1
    err = max((offs[hi] - offs[lo]) / 2, STEP / 2)
    return best, float(d[i]), err, i


def analyse(toi, tic, P, T0, t14h, outdir):
    t14 = t14h / 24
    T0 = T0 - 2457000.0
    print(f"TOI-{toi} (TIC {tic}): P {P} d, T0 {T0:.4f} BTJD, T14 {t14h} h", flush=True)
    secs = load(tic)
    rows, sector_rows = [], []
    for s, author, exptime, t, f, e in secs:
        cad = np.median(np.diff(t))
        n0, n1 = int(np.ceil((t.min() - T0) / P - 0.5)), int(np.floor((t.max() - T0) / P + 0.5))
        sector_sum = None; n_used = 0
        for n in range(n0, n1 + 1):
            mid = T0 + n * P
            offs, d, dep, scl = scan(t, f, e, mid, P, t14, cad)
            if not np.any(np.isfinite(d)):
                continue
            best, dmax, err, i = peak(offs, d)
            near = np.abs(offs) <= 1 / 24
            dpred = float(np.nanmax(d[near])) if np.any(np.isfinite(d[near])) else np.nan
            used = bool(dmax >= MIN_DCHI2)
            rows.append(dict(toi=toi, sector=s, author=author, epoch=n, t_pred=mid, t_mid=mid + best,
                             o_c_min=best * 1440, err_min=err * 1440, depth_ppm=dep[i] * 1e6,
                             dchi2=dmax, dchi2_pred=dpred, used=used,
                             coverage=float(np.mean(np.isfinite(d)))))
            dd = np.where(np.isfinite(d), d, 0.0)
            sector_sum = dd if sector_sum is None else sector_sum + dd
            n_used += 1
        if n_used:
            best, dmax, err, i = peak(offs, sector_sum)
            near = np.abs(offs) <= 1 / 24
            sector_rows.append(dict(toi=toi, sector=s, author=author, n_transits=n_used,
                                    o_c_min=best * 1440, err_min=err * 1440, dchi2=dmax,
                                    dchi2_pred=float(np.max(sector_sum[near])),
                                    t_ref=T0 + round((np.median(t) - T0) / P) * P))
    # weighted linear ephemeris from used per-transit times
    u = [r for r in rows if r["used"]]
    summary = dict(toi=toi, tic=tic, P_exofop=P, T14_h=t14h, n_windows=len(rows), n_used=len(u),
                   sectors=[r["sector"] for r in sector_rows])
    if len(u) >= 3:
        E = np.array([r["epoch"] for r in u], float); tm = np.array([r["t_mid"] for r in u])
        sg = np.array([r["err_min"] for r in u]) / 1440
        A = np.vstack([np.ones_like(E), E]).T / sg[:, None]
        (t0f, pf), *_ = np.linalg.lstsq(A, tm / sg, rcond=None)
        cov = np.linalg.inv(A.T @ A)
        oc = (tm - (t0f + pf * E)) * 1440
        chi2 = float(np.sum((oc / (sg * 1440)) ** 2))
        for r, o in zip(u, oc):
            r["o_c_refit_min"] = o
        summary.update(P_fit=pf, P_fit_err=float(np.sqrt(cov[1, 1])), T0_fit_btjd=t0f,
                       chi2=chi2, dof=len(u) - 2, rms_oc_min=float(np.std(oc)),
                       median_err_min=float(np.median(sg) * 1440), max_abs_oc_min=float(np.max(np.abs(oc))))
        # per-sector O-C relative to the refitted ephemeris
        for r in sector_rows:
            n = round((r["t_ref"] - t0f) / pf)
            r["o_c_refit_min"] = ((r["t_ref"] + r["o_c_min"] / 1440) - (t0f + pf * n)) * 1440
        so = np.array([r["o_c_refit_min"] for r in sector_rows if r["dchi2"] >= MIN_DCHI2])
        summary.update(sector_half_ptp_min=float((so.max() - so.min()) / 2) if len(so) else None)
    out = Path(outdir)
    with open(out / f"TOI{toi}_transits.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=sorted({k for r in rows for k in r}))
        wr.writeheader(); wr.writerows(rows)
    with open(out / f"TOI{toi}_sectors.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=sorted({k for r in sector_rows for k in r}))
        wr.writeheader(); wr.writerows(sector_rows)
    (out / f"TOI{toi}_summary.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")
    # plot
    fig, ax = plt.subplots(figsize=(8, 4))
    if len(u) >= 3:
        ax.errorbar([r["t_mid"] for r in u], [r["o_c_refit_min"] / 60 for r in u],
                    [r["err_min"] / 60 for r in u], fmt="o", ms=3, color="0.5", label="per transit")
        sr = [r for r in sector_rows if r["dchi2"] >= MIN_DCHI2]
        ax.errorbar([r["t_ref"] for r in sr], [r["o_c_refit_min"] / 60 for r in sr],
                    [r["err_min"] / 60 for r in sr], fmt="s", ms=5, color="C3", label="per sector")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("BTJD"); ax.set_ylabel("O - C (h)")
    ax.set_title(f"TOI-{toi} (TIC {tic}): re-measured from light curves, P = {summary.get('P_fit', P):.6f} d")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / f"TOI{toi}_oc.png", dpi=120); plt.close(fig)
    print(json.dumps(summary, default=float), flush=True)


def main():
    outdir = sys.argv[1]
    Path(outdir).mkdir(parents=True, exist_ok=True)
    for spec in sys.argv[2:]:
        toi, tic, P, T0, t14 = spec.split(":")
        try:
            analyse(toi, int(tic), float(P), float(T0), float(t14), outdir)
        except Exception as ex:  # noqa: BLE001
            print(f"TOI-{toi}: FAILED {ex!r}", flush=True)


if __name__ == "__main__":
    main()
