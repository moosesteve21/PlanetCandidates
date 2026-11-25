#!/usr/bin/env python
"""Robust summary of ttv_remeasure.py output: keep only transits that are this TOI's own, then refit.

ttv_remeasure.py scans the whole orbit around each predicted transit and takes the strongest dip. In a multi-planet
system, or with systematics, a window without this planet's transit locks onto another dip (TOI-216: the genuine
transits are ~14 ppt and within +-15 h, the strays 2-7 ppt and ~200 h off). Here a transit is kept only if:
  - ttv_remeasure marked it used (dchi2 above its threshold), and
  - its depth is within DEPTH_LO-DEPTH_HI x the TOI's ExoFOP depth (--toi-table; else the median depth of the
    strongest half of the transits, which fails in a multi-planet system where the other planet is deeper: TOI-2525),
  - and it survives iterative removal of single outliers (the worst residual is dropped while it exceeds
    CLIP_MAD x the robust scatter and CLIP_MIN_H hours; a real TTV moves whole sectors together, so it survives).
Then a weighted straight-line ephemeris is fitted to the kept times, and the per-sector mean O-C after that refit is
reported; A = half the peak-to-peak range of the per-sector means (comparable with a visit-binned amplitude).

  - optionally (--max-oc-h H), it lies within H hours of the ExoFOP prediction: stray dips sit hundreds of hours
    off while real TTVs here are hours, so H = 24 removes strays (not for systems with larger published TTVs).
Usage: .venv/bin/python investigations/ttv_robust.py OUTDIR [--toi-table EXOFOP.csv] [--max-oc-h H] [TOI ...]
Writes OUTDIR/robust_summary.csv and OUTDIR/TOI*_robust_oc.png.
"""
import csv
import glob
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DEPTH_LO, DEPTH_HI = 0.5, 2.0
CLIP_MAD, CLIP_MIN_H = 5.0, 3.0


def analyse(path, exo_depth=None, max_oc_h=None):
    rows = [r for r in csv.DictReader(open(path)) if r["used"] == "True"]
    if max_oc_h:
        rows = [r for r in rows if abs(float(r["o_c_min"])) <= 60 * max_oc_h]
    if len(rows) < 3:
        return None
    toi = rows[0]["toi"]
    d = np.array([float(r["depth_ppm"]) for r in rows]); x2 = np.array([float(r["dchi2"]) for r in rows])
    ref = exo_depth if exo_depth else np.median(d[x2 >= np.median(x2)])
    keep = [r for r, dd in zip(rows, d) if DEPTH_LO * ref <= dd <= DEPTH_HI * ref]
    if len(keep) < 3:
        return dict(toi=toi, n_used=len(rows), n_kept=len(keep), ref_depth_ppm=round(ref))
    E = np.array([int(r["epoch"]) for r in keep], float)
    t = np.array([float(r["t_mid"]) for r in keep])
    e = np.array([max(float(r["err_min"]), 1.0) for r in keep]) / 1440
    sec = np.array([int(r["sector"]) for r in keep])
    n_clip = 0
    while True:
        A = np.vstack([np.ones_like(E), E]).T
        w = 1 / e
        (t0, P), *_ = np.linalg.lstsq(A * w[:, None], t * w, rcond=None)
        oc = (t - (t0 + P * E)) * 24                                 # hours
        r = np.abs(oc - np.median(oc)); mad = 1.4826 * np.median(r)
        j = int(np.argmax(r))
        if len(t) <= 4 or r[j] <= max(CLIP_MAD * mad, CLIP_MIN_H):
            break
        E, t, e, sec = np.delete(E, j), np.delete(t, j), np.delete(e, j), np.delete(sec, j); n_clip += 1
    keep = keep[:len(t)]
    chi2 = float(np.sum((oc / (e * 24)) ** 2))
    means = {}
    for s in np.unique(sec):
        m = sec == s
        ww = 1 / e[m] ** 2
        means[int(s)] = (float(np.sum(oc[m] * ww) / np.sum(ww)), float(np.mean(t[m])))
    mv = np.array([v[0] for v in means.values()])
    amp = float((mv.max() - mv.min()) / 2) if len(mv) > 1 else float("nan")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.errorbar(t, oc, yerr=e * 24, fmt=".", color="0.6", ms=4, label="transits (kept)")
    ax.plot([v[1] for v in means.values()], mv, "s", color="C3", ms=5, label="sector means")
    ax.axhline(0, color="k", lw=0.5)
    ax.set(xlabel="BTJD", ylabel="O-C (h)", title=f"TOI-{toi}: P = {P:.6f} d, A = {amp:.2f} h ({len(t)} transits)")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(Path(path).parent / f"TOI{toi}_robust_oc.png", dpi=110)
    plt.close(fig)
    return dict(toi=toi, n_used=len(rows), n_kept=len(t), n_clipped=n_clip, ref_depth_ppm=round(ref), P_fit=round(float(P), 7),
                T0_fit_btjd=round(float(t0), 5), n_sectors=len(means), A_h=round(amp, 2),
                rms_oc_h=round(float(np.sqrt(np.mean(oc ** 2))), 2), median_err_min=round(float(np.median(e)) * 1440, 1),
                chi2_dof=round(chi2 / max(len(keep) - 2, 1), 1),
                sector_means_h=" ".join(f"S{s}:{v[0]:+.2f}" for s, v in means.items()))


def main():
    args = sys.argv[1:]
    out = Path(args.pop(0)); depths = {}
    if args[:1] == ["--toi-table"]:
        args.pop(0)
        depths = {r["TOI"]: float(r["Depth (ppm)"]) for r in csv.DictReader(open(args.pop(0))) if r["Depth (ppm)"]}
    max_oc = None
    if args[:1] == ["--max-oc-h"]:
        args.pop(0); max_oc = float(args.pop(0))
    only = set(args)
    res = []
    for p in sorted(glob.glob(str(out / "TOI*_transits.csv"))):
        toi = Path(p).name[3:].split("_")[0]
        if only and toi not in only:
            continue
        r = analyse(p, depths.get(toi), max_oc)
        if r:
            r["max_oc_h"] = max_oc
        if r:
            res.append(r); print(r)
    keys = sorted({k for r in res for k in r}, key=lambda k: list(res[0]).index(k) if k in res[0] else 99)
    name = "robust_summary.csv" if not max_oc else f"robust_summary_maxoc{max_oc:g}h.csv"
    with open(out / name, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(res)


if __name__ == "__main__":
    main()
