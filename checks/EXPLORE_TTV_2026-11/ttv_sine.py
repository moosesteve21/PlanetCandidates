#!/usr/bin/env python3
"""ttv_sine.py - preliminary TTV-cycle model: linear ephemeris plus one sinusoid, fitted to measured transit times.

  t_n = T0 + P n + a sin(2 pi t_n / Psup) + b cos(2 pi t_n / Psup)

For each trial super-period Psup on a grid, the four linear parameters are fitted by weighted least squares.
Transits are selected as in ttv_robust.py: ttv_remeasure marked them used, their depth is DEPTH_LO-DEPTH_HI times
the reference depth, and they lie within MAX_OC_H hours of the ExoFOP prediction.
The timing errors are scaled by sqrt(chi2_min / dof), so the best fit has reduced chi2 = 1.
Super-periods with scaled delta-chi2 < 4 are accepted. For each accepted model, the predicted O-C and its 1-sigma
error (from the scaled covariance) are evaluated. The prediction envelope is the minimum of (pred - 2 sigma) to the
maximum of (pred + 2 sigma) over the accepted models.
This is the simplest TTV shape, with no dynamics. With only ~1 cycle covered, treat it as a guide to where future
transits fall, not as a measured super-period.

Usage: python ttv_sine.py TRANSITS.csv REF_DEPTH_PPM [--start BTJD --end BTJD] [--out PREFIX]
Writes PREFIX_sine_fit.png, PREFIX_sine_scan.csv and PREFIX_sine_predictions.csv.
"""
import argparse
import csv

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DEPTH_LO, DEPTH_HI, MAX_OC_H = 0.5, 2.0, 24.0


def design(E, t, Ps):
    w = 2 * np.pi / Ps
    return np.vstack([np.ones_like(E), E, np.sin(w * t), np.cos(w * t)]).T


def fit(E, t, e, Ps):
    A = design(E, t, Ps) / e[:, None]
    c, *_ = np.linalg.lstsq(A, t / e, rcond=None)
    chi2 = float(np.sum((A @ c - t / e) ** 2))
    cov = np.linalg.inv(A.T @ A)
    return c, chi2, cov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transits"); ap.add_argument("ref_depth", type=float)
    ap.add_argument("--start", type=float, default=4406.5, help="prediction start, BTJD (default 2027-01-01)")
    ap.add_argument("--end", type=float, default=4771.5, help="prediction end, BTJD (default 2028-01-01)")
    ap.add_argument("--pmin", type=float, default=60.0); ap.add_argument("--pmax", type=float, default=3000.0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rows = [r for r in csv.DictReader(open(a.transits)) if r["used"] == "True"
            and abs(float(r["o_c_min"])) <= 60 * MAX_OC_H
            and DEPTH_LO * a.ref_depth <= float(r["depth_ppm"]) <= DEPTH_HI * a.ref_depth]
    toi = rows[0]["toi"]; out = a.out or a.transits.rsplit("_", 1)[0]
    E = np.array([int(r["epoch"]) for r in rows], float); t = np.array([float(r["t_mid"]) for r in rows])
    e = np.array([max(float(r["err_min"]), 1.0) for r in rows]) / 1440
    sec = [int(r["sector"]) for r in rows]
    n = len(t); dof = n - 4
    grid = np.linspace(a.pmin, a.pmax, 20000)
    scan = []
    for Ps in grid:
        c, chi2, _ = fit(E, t, e, Ps)
        scan.append((Ps, chi2, float(np.hypot(c[2], c[3]) * 24), float(c[1])))
    scan = np.array(scan)
    i0 = int(np.argmin(scan[:, 1])); chi2min = scan[i0, 1]
    s2 = max(chi2min / dof, 1.0)                                 # error scale factor squared
    ok = (scan[:, 1] - chi2min) / s2 < 4
    Pacc = scan[ok, 0]
    lin = np.linalg.lstsq(np.vstack([np.ones_like(E), E]).T / e[:, None], t / e, rcond=None)
    chi2lin = float(lin[1][0]) if len(lin[1]) else float("nan")
    # reference linear ephemeris for O-C: the best sinusoid model's T0 and P
    cb, _, _ = fit(E, t, e, scan[i0, 0]); T0, P = cb[0], cb[1]
    print(f"TOI-{toi}: {n} transits, sectors {sorted(set(sec))}, span {t.max() - t.min():.0f} d")
    print(f"straight line chi2 = {chi2lin:.0f} (dof {n - 2}); best sinusoid chi2 = {chi2min:.1f} (dof {dof}), "
          f"error scale x{np.sqrt(s2):.2f}")
    print(f"best Psup = {scan[i0, 0]:.0f} d, amplitude {scan[i0, 2]:.1f} h, mean P = {P:.6f} d, T0 = {T0:.5f} BTJD")
    print(f"accepted Psup (scaled delta-chi2 < 4): {Pacc.min():.0f}-{Pacc.max():.0f} d "
          f"(amplitudes {scan[ok, 2].min():.1f}-{scan[ok, 2].max():.1f} h)")
    with open(out + "_sine_scan.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Psup_d", "chi2", "amp_h", "P_d"]); w.writerows(np.round(scan, 6))

    # predictions: iterate t_n = T0 + P n + TTV(t_n) (the TTV is a small fraction of Psup)
    def predict(Ps, nn):
        c, _, cov = fit(E, t, e, Ps); cov = cov * s2
        tn = c[0] + c[1] * nn
        for _ in range(3):
            tn = design(nn, tn, Ps) @ c
        X = design(nn, tn, Ps)
        return tn, np.sqrt(np.einsum("ij,jk,ik->i", X, cov, X))

    nn = np.arange(np.ceil((a.start - T0) / P), np.floor((a.end - T0) / P) + 1)
    lo = np.full(len(nn), np.inf); hi = np.full(len(nn), -np.inf)
    for Ps in Pacc[:: max(1, len(Pacc) // 200)]:
        tn, sd = predict(Ps, nn); lo = np.minimum(lo, tn - 2 * sd); hi = np.maximum(hi, tn + 2 * sd)
    tb, sb = predict(scan[i0, 0], nn)
    with open(out + "_sine_predictions.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["epoch", "t_linear_btjd", "t_best_btjd", "best_minus_linear_h", "window_lo_btjd", "window_hi_btjd",
                    "window_width_h"])
        for k in range(len(nn)):
            w.writerow([int(nn[k]), round(T0 + P * nn[k], 4), round(tb[k], 4), round((tb[k] - T0 - P * nn[k]) * 24, 2),
                        round(lo[k], 4), round(hi[k], 4), round((hi[k] - lo[k]) * 24, 1)])
    print(f"{len(nn)} predicted transits {a.start:.1f}-{a.end:.1f} BTJD; window widths "
          f"{(hi - lo).min() * 24:.0f}-{(hi - lo).max() * 24:.0f} h; best-model O-C "
          f"{((tb - T0 - P * nn) * 24).min():+.1f} to {((tb - T0 - P * nn) * 24).max():+.1f} h")

    # plot: data, best model, envelope out to the end of the prediction span
    tt = np.linspace(t.min() - 50, a.end, 1500); ee = np.round((tt - T0) / P)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw=dict(width_ratios=[2.2, 1]))
    elo = np.full(len(tt), np.inf); ehi = np.full(len(tt), -np.inf)
    for Ps in Pacc[:: max(1, len(Pacc) // 100)]:
        c, _, cov = fit(E, t, e, Ps); X = design(ee, tt, Ps); m = X @ c
        sd = np.sqrt(np.einsum("ij,jk,ik->i", X, cov * s2, X))
        elo = np.minimum(elo, m - 2 * sd - T0 - P * ee); ehi = np.maximum(ehi, m + 2 * sd - T0 - P * ee)
    ax1.fill_between(tt, elo * 24, ehi * 24, color="C0", alpha=0.2, lw=0, label="accepted models, 2σ")
    ax1.plot(tt, (design(ee, tt, scan[i0, 0]) @ cb - T0 - P * ee) * 24, "C0", lw=1,
             label=f"best: Psup {scan[i0, 0]:.0f} d, ±{scan[i0, 2]:.1f} h")
    ax1.errorbar(t, (t - T0 - P * E) * 24, yerr=e * 24 * np.sqrt(s2), fmt="o", color="C3", ms=4, label="TESS transits")
    ax1.axvspan(a.start, a.end, color="0.9", zorder=0)
    ax1.set(xlabel="BTJD", ylabel="O−C (h)", title=f"TOI-{toi}: linear ephemeris + one sinusoid (preliminary)")
    ax1.legend(fontsize=7, loc="lower left")
    ax2.plot(scan[:, 0], (scan[:, 1] - chi2min) / s2, "k", lw=0.8); ax2.axhline(4, color="C3", lw=0.6, ls="--")
    ax2.set(yscale="symlog", ylim=(0, None), xlabel="super-period (d)", ylabel="scaled Δχ²", title="super-period scan")
    fig.tight_layout(); fig.savefig(out + "_sine_fit.png", dpi=110); plt.close(fig)


if __name__ == "__main__":
    main()
