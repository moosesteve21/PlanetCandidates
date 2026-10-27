#!/usr/bin/env python3
"""figure.py - check figures for the four "raw" TOIs of PHT thread 4163752 (group 3; results/pht_group3_tois).
Per star: (a) the light curve folded over the whole orbit, binned, with phase 0.5 marked, so a secondary eclipse shows;
(b) the transit depth in each sector as the vetting measured it (enriched.csv sector_depths_ppm), SPOC 2-min and QLP
FFI apart. Light curves are the files the run used (prefetch.jsonl), detrended here by a 1-day running median with
the eclipses masked.
Usage: .venv/bin/python investigations/pht4163752/figure.py [--out ~/candidates/checks/PHT4163752]
"""
import argparse
import json
import re
import warnings
from pathlib import Path

import lightkurve as lk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results" / "pht_group3_tois"
TOI = {"TIC 5224772": "TOI-2940.01", "TIC 464328419": "TOI-2954.01", "TIC 456962262": "TOI-3157.01",
       "TIC 320994166": "TOI-3207.01"}


def detrended(files, P, T0, D):
    ts, fs = [], []
    for f in files:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lc = lk.read(f).remove_nans().normalize()
        lc = lc[lc.quality == 0] if "quality" in lc.columns else lc
        t, y = lc.time.value, np.asarray(lc.flux.value, dtype=float)
        ph = ((t - T0) / P + 0.25) % 1 - 0.25
        ecl = (np.abs(ph) < D / P) | (np.abs(ph - 0.5) < D / P)        # eclipse windows, 2 durations wide
        s = pd.Series(np.where(ecl, np.nan, y), index=pd.to_timedelta(t, unit="D"))
        trend = s.rolling("1D", center=True, min_periods=10).median().to_numpy()
        ok = np.isfinite(trend)
        ts.append(t[ok]), fs.append(y[ok] / trend[ok])
    return np.concatenate(ts), np.concatenate(fs)


def binned(ph, y, n=200):
    edges = np.linspace(-0.25, 0.75, n + 1)
    i = np.digitize(ph, edges) - 1
    m = np.array([np.median(y[i == k]) if np.sum(i == k) > 3 else np.nan for k in range(n)])
    e = np.array([1.2533 * np.std(y[i == k]) / np.sqrt(np.sum(i == k)) if np.sum(i == k) > 3 else np.nan
                  for k in range(n)])
    return (edges[:-1] + edges[1:]) / 2, m, e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path.home() / "candidates" / "checks" / "PHT4163752"))
    a = ap.parse_args()
    out = Path(a.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    files = {}
    for line in open(RUN / "prefetch.jsonl"):
        r = json.loads(line)
        files[r["star"]] = r["files"]
    en = pd.read_csv(RUN / "enriched.csv")
    for star, toi in TOI.items():
        c = en[en.target == star].sort_values("snr", ascending=False).iloc[0]   # the TOI signal
        P, T0, D = c.period_d, c.t0_btjd, c.duration_h / 24
        t, y = detrended(files[star], P, T0, D)
        ph = ((t - T0) / P + 0.25) % 1 - 0.25
        x, m, e = binned(ph, y)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1.6, 1]))
        ax1.plot(ph, (y - 1) * 1e3, ".", ms=1, color="0.75", rasterized=True)
        ax1.errorbar(x, (m - 1) * 1e3, (e * 1e3), fmt="o-", ms=2.5, lw=1, color="C3", label="binned")
        ax1.axvline(0.5, ls="--", color="C0", lw=1, label="phase 0.5")
        lo = np.nanmin(m - 1) * 1e3
        ax1.set_ylim(lo * 1.25, -lo * 0.25)
        ax1.set_xlabel("Orbital phase")
        ax1.set_ylabel("Relative flux (ppt)")
        ax1.set_title(f"Folded over the whole orbit, P = {P:.5f} d")
        ax1.legend(loc="lower right", fontsize=8)
        sec = str(c.secondary_ppm)
        ins = ax1.inset_axes([0.33, 0.06, 0.34, 0.42])
        w = (np.abs(x - 0.5) < 0.12)
        ins.errorbar(x[w], (m[w] - 1) * 1e3, e[w] * 1e3, fmt="o-", ms=2, lw=0.8, color="C3")
        ins.axvline(0.5, ls="--", color="C0", lw=0.8)
        ins.axhline(0, color="0.5", lw=0.6)
        ins.set_title(f"around phase 0.5: secondary {sec} ppm", fontsize=8)
        ins.tick_params(labelsize=7)
        rows = [re.match(r"(\d+)(\(QLP\))?=(-?\d+)\+-(\d+)", s).groups() for s in str(c.sector_depths_ppm).split(";")]
        rows = sorted(rows, key=lambda r: int(r[0]))
        lab = [f"S{r[0]}" for r in rows]
        dep = np.array([float(r[2]) for r in rows]) / 1e3
        err = np.array([float(r[3]) for r in rows]) / 1e3
        col = ["C1" if r[1] else "C0" for r in rows]
        ax2.bar(range(len(rows)), dep, yerr=err, color=col, capsize=3)
        ax2.set_xticks(range(len(rows)), lab, fontsize=8)
        ax2.set_ylabel("Transit depth (ppt)")
        ax2.set_title("Depth by sector (blue SPOC 2-min, orange QLP FFI)")
        fig.suptitle(f"{toi} ({star}): odd/even {c.odd_even_sigma:.1f} sigma, Gaia RUWE {c.gaia_ruwe:.1f}; "
                     f"KESTREL flags: {c['flags'].replace(';', ', ')}", fontsize=10)
        fig.tight_layout()
        f = out / f"{toi}_{star.replace(' ', '')}_check.png"
        fig.savefig(f, dpi=110)
        plt.close(fig)
        print(f)


if __name__ == "__main__":
    main()
