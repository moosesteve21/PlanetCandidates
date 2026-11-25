#!/usr/bin/env python
"""PHT 4183497 (eldee / Lorenz, 2026-11-17): TIC 143901397, 2.929343 d, 173 ppm, 3.3 h. Is the source the
58.6" neighbour TIC 143901368 (G 14.0, would need a ~2.4% eclipse)?

1. Neighbour's own light curve: the TGLC S8 light curve of TIC 143901368 (the only sector with one), folded at
   the reported ephemeris. In-transit mean minus
   out-of-transit mean (local window +-3 T14), compared with the ~2.4% a source there would need.
2. KESTREL's depth map (depth_map.py): per-sector source fit over every star within 2.5' up to 5.5 mag
   fainter, with the neighbour always tested. Every TESScut sector (S110 included if released).
Usage: .venv/bin/python investigations/pht_4183497/check.py
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import lightkurve as lk  # noqa: E402

import depth_map as dm  # noqa: E402

OUT = Path(__file__).resolve().parent
TGT, NB = 143901397, 143901368
P, T0, T14 = 2.929343, 2459984.7636 - 2457000, 3.3 / 24
NEED = 0.024


def fold_depth(t, f):
    ph = ((t - T0 + P / 2) % P) - P / 2
    inn = np.abs(ph) < T14 / 2 * 0.8          # inner 80% of the transit
    out = (np.abs(ph) > T14) & (np.abs(ph) < 3 * T14)
    n_tr = len(np.unique(np.round((t[inn] - T0) / P)))
    d = np.mean(f[out]) - np.mean(f[inn])
    # error from the scatter of the out-of-transit points, scaled to the in-transit count
    e = np.std(f[out]) * np.sqrt(1 / inn.sum() + 1 / out.sum())
    return d, e, n_tr, ph, inn


def neighbour_lc():
    """TGLC S8 for the neighbour. Its PSF flux is empty (NaN) for this star, so the calibrated aperture flux is
    used (TGLC subtracts the modelled neighbours, the target included, before the aperture sum). Quality flags
    applied, 1-d running median removed, points beyond 5 x the MAD clipped."""
    res = lk.search_lightcurve(f"TIC {NB}", mission="TESS", author="TGLC")
    from astropy.io import fits
    lc = res[0].download(quality_bitmask="none")
    d = fits.getdata(lc.meta["FILENAME"], 1)
    q = (d["TESS_flags"] == 0) & (d["TGLC_flags"] == 0)
    t = np.asarray(d["time"], float)[q]; f = np.asarray(d["cal_aper_flux"], float)[q]
    ok = np.isfinite(t) & np.isfinite(f); t, f = t[ok], f[ok]
    f = f / np.array([np.median(f[np.abs(t - x) < 0.5]) for x in t])
    mad = 1.4826 * np.median(np.abs(f - 1)); keep = np.abs(f - 1) < 5 * mad
    n_clip = int((~keep).sum()); t, f = t[keep], f[keep]
    d, e, n, ph, inn = fold_depth(t, f)
    rng = np.random.default_rng(1); z = []
    for _ in range(300):                       # same measurement at random phases
        s0 = rng.uniform(0, P); p2 = ((t - T0 - s0 + P / 2) % P) - P / 2
        i2 = np.abs(p2) < T14 / 2 * 0.8; o2 = (np.abs(p2) > T14) & (np.abs(p2) < 3 * T14)
        if i2.sum() > 10:
            z.append(np.mean(f[o2]) - np.mean(f[i2]))
    row = dict(author="TGLC cal_aper_flux", sector=8, n_points=int(len(t)), n_clipped=n_clip, n_transits=n,
               n_in_transit=int(inn.sum()), depth=d, err=e, random_phase_sd=float(np.std(z)),
               robust_rms=float(mad), sigma_below_needed=float((NEED - d) / e))
    print(f"TGLC S8: {n} transits ({inn.sum()} points), depth {d*100:.2f} +- {e*100:.2f} % "
          f"(random phases sd {np.std(z)*100:.2f} %); a {NEED*100:.1f} % eclipse is excluded at "
          f"{(NEED-d)/e:.1f} sigma", flush=True)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3.2))
    m = np.abs(ph) < 0.5
    ax.plot(ph[m] * 24, (f[m] - 1) * 100, ".", ms=3, color="0.6")
    bb = np.arange(-12, 12.01, 1.0); idx = np.digitize(ph[m] * 24, bb)
    med = [np.mean(f[m][idx == k]) if np.sum(idx == k) > 2 else np.nan for k in range(1, len(bb))]
    ax.plot(bb[:-1] + 0.5, (np.array(med) - 1) * 100, "o-", ms=3, color="C0", label="1-h bins")
    ax.axhline(-NEED * 100, color="C3", ls="--", label="2.4% needed if this star were the source")
    ax.axvspan(-T14 * 12, T14 * 12, color="C1", alpha=0.1)
    ax.set_ylim(-8, 8); ax.set_xlabel("hours from predicted mid-transit"); ax.set_ylabel("flux − 1 (%)")
    ax.set_title(f"TIC {NB} (58\" neighbour), TGLC S8, folded at P = {P} d", fontsize=9)
    ax.legend(fontsize=7, loc="lower left"); fig.tight_layout(); fig.savefig(OUT / "neighbour_fold.png", dpi=110)
    return [row]


def main():
    print("== 1. neighbour's own light curves")
    lcs = neighbour_lc()
    print("== 2. depth map")
    res = dm.depth_map(TGT, P, T0, T14, extra=(NB,))
    dm.ranking(res)
    dm.plot(res, OUT / "depth_map.png")
    secs = [dict(sector=int(s[0]), n_transits=int(s[1]), best=s[2], target_minus_best=float(s[3]),
                 target_vs_nodip=float(s[4]),
                 neighbour_minus_target=float(s[5].get(str(NB), np.nan) - s[5][str(TGT)]))
            for s in res["sectors"]]
    for s in secs:
        print(s)
    tot = dict(target_vs_nodip=float(res["chi_null"] - res["chi"][str(TGT)]),
               neighbour_minus_target=float(res["chi"].get(str(NB), np.nan) - res["chi"][str(TGT)]),
               best=min(res["chi"], key=res["chi"].get))
    print("summed:", tot)
    (OUT / "result.json").write_text(json.dumps(dict(ephemeris=dict(P=P, T0_btjd=T0, T14_h=T14 * 24),
                                                     neighbour_lcs=lcs, depth_map_sectors=secs, depth_map_sum=tot),
                                                indent=1, default=float) + "\n")


if __name__ == "__main__":
    main()
