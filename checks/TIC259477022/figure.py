#!/usr/bin/env python3
"""figure.py - the public figure for the TIC 259477022 check (see NOTES.md).

Rows: SPOC 2-min PDCSAP, SPOC 2-min SAP (same file), TESS-SPOC FFI PDCSAP; columns: the S3 and S5 events.
Each panel: flux minus a cubic fitted outside +-6 h, in ppm, 2-min (or FFI) points grey, 30-min bins blue;
the reported 8 h window shaded; momentum dumps (quality bit 32) as dashed lines. The depth in +-4 h is printed.

Usage: .venv/bin/python investigations/tic259477022/figure.py [outfile]
"""
import sys
import warnings
from pathlib import Path

import lightkurve as lk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
TIC = "TIC 259477022"
EVENTS = [(3, 1393.63), (5, 1454.43)]
ROWS = [("SPOC", 120, "pdcsap_flux", "SPOC 2-min PDCSAP"),
        ("SPOC", 120, "sap_flux", "SPOC 2-min SAP (same file)"),
        ("TESS-SPOC", None, "pdcsap_flux", "TESS-SPOC FFI PDCSAP")]
HALF = 0.6       # days shown either side
IN_H = 4.0       # reported half-duration, hours


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "pdcsap_vs_sap.png"
    sr = lk.search_lightcurve(TIC, mission="TESS")
    fig, axs = plt.subplots(len(ROWS), len(EVENTS), figsize=(10, 8), sharex=True, sharey=True)
    for c, (sec, tc) in enumerate(EVENTS):
        for r, (author, exptime, col, label) in enumerate(ROWS):
            ss = sr[(sr.table["sequence_number"] == sec) & (sr.table["author"] == author)]
            if exptime:
                ss = ss[ss.table["exptime"].value == exptime]
            raw = ss[0].download(quality_bitmask="none")
            t = raw.time.value
            q = np.asarray(raw.quality.value).astype(int)
            f = np.asarray(raw[col].value, float)
            w = (np.abs(t - tc) < HALF) & ((q & lk.utils.TessQualityFlags.DEFAULT_BITMASK) == 0) & np.isfinite(f)
            x, y = (t[w] - tc) * 24, f[w] / np.nanmedian(f[w])
            oot = np.abs(x) > 6
            res = (y - np.polyval(np.polyfit(x[oot], y[oot], 3), x)) * 1e6
            inn = np.abs(x) < IN_H
            depth, err = -res[inn].mean(), res[oot].std() / np.sqrt(inn.sum())
            ax = axs[r, c]
            ax.plot(x, res, ".", ms=1.5, color="0.65")
            edges = np.arange(-HALF * 24, HALF * 24 + 0.01, 0.5)
            mid, yb = [], []
            for a, b in zip(edges[:-1], edges[1:]):
                m = (x >= a) & (x < b)
                if m.sum() >= 1:
                    mid.append((a + b) / 2)
                    yb.append(res[m].mean())
            ax.plot(mid, yb, "o", ms=3.5, color="C0")
            ax.axvspan(-IN_H, IN_H, color="C1", alpha=0.15)
            for d in t[(np.abs(t - tc) < HALF) & ((q & 32) != 0)]:
                ax.axvline((d - tc) * 24, color="k", ls="--", lw=0.8)
            ax.axhline(0, color="k", lw=0.4)
            ax.text(0.02, 0.05, f"depth in ±4 h: {depth:.0f} ± {err:.0f} ppm", transform=ax.transAxes, fontsize=8)
            ax.set_title(f"S{sec}, BTJD {tc}: {label}", fontsize=9)
            if c == 0:
                ax.set_ylabel("flux − cubic (ppm)")
            if r == len(ROWS) - 1:
                ax.set_xlabel("hours from reported mid-time")
    axs[0, 0].set_ylim(-5000, 3000)
    fig.suptitle(f"{TIC}: the reported dips appear in PDCSAP only\n"
                 "(shaded: reported 8 h event; dashed: momentum dump; blue: 30-min bins)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print("wrote", out)


if __name__ == "__main__":
    main()
