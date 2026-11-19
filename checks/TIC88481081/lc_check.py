#!/usr/bin/env python3
"""lc_check.py - independent check of DAAN11's TIC 88481081 (PHT 4185529): P ~1.730 d, ~0.45%, ~1.5 h, T0 ~4314.30.
SPOC 2-min S105-S108: BLS on the stitched PDCSAP, then per-sector depth, odd/even, secondary at phase 0.5,
SAP vs PDCSAP depth, flux-weighted centroid shift in transit, background in transit.
Usage (.venv): python lc_check.py  -> lc_check.png, lc_check.txt here
"""
import warnings; warnings.filterwarnings("ignore")
from pathlib import Path
import lightkurve as lk, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.timeseries import BoxLeastSquares
HERE = Path(__file__).resolve().parent; out = []
def say(s=""): print(s, flush=True); out.append(s)
sr = lk.search_lightcurve("TIC 88481081", author="SPOC", exptime=120)
lcs = sr.download_all(download_dir=str(HERE))
t, f, e, sap, cx, cy, bk, sec = [], [], [], [], [], [], [], []
for lc in lcs:
    m = (lc.quality == 0) & np.isfinite(lc.flux.value) & np.isfinite(lc.sap_flux.value)
    l = lc[m]; s = l.sector
    fl = l.flatten(window_length=721)          # ~1 d window
    sp = lk.LightCurve(time=l.time, flux=l.sap_flux.value / np.nanmedian(l.sap_flux.value)).flatten(window_length=721)
    t.append(l.time.value); f.append(fl.flux.value); e.append(fl.flux_err.value); sap.append(sp.flux.value)
    cx.append(l.mom_centr1.value - np.nanmedian(l.mom_centr1.value)); cy.append(l.mom_centr2.value - np.nanmedian(l.mom_centr2.value))
    bk.append(l.sap_bkg.value); sec.append(np.full(len(l), s))
    say(f"S{s}: {len(l)} good cadences, CROWDSAP {l.meta.get('CROWDSAP')}, FLFRCSAP {l.meta.get('FLFRCSAP')}")
t, f, e, sap, cx, cy, bk, sec = map(np.concatenate, (t, f, e, sap, cx, cy, bk, sec))
bls = BoxLeastSquares(t, f, e)
P = np.exp(np.linspace(np.log(0.5), np.log(15), 200000))
res = bls.power(P, [0.04, 0.06, 0.08, 0.1])
i = np.argmax(res.power); per, t0, dur = res.period[i], res.transit_time[i], res.duration[i]
say(f"BLS best: P {per:.5f} d, T0 {t0:.4f}, dur {dur*24:.2f} h, depth {res.depth[i]*1e6:.0f} ppm, SNR {res.depth_snr[i]:.1f}")
# refine on fine grid near the peak
Pf = np.linspace(per*0.999, per*1.001, 4001); r2 = bls.power(Pf, np.linspace(0.03, 0.12, 19))
j = np.argmax(r2.power); per, t0, dur = r2.period[j], r2.transit_time[j], r2.duration[j]
n0 = np.round((4314.30 - t0) / per); t0 = t0 + n0 * per
say(f"refined: P {per:.6f} d, T0 {t0:.4f} BTJD, dur {dur*24:.2f} h, depth {r2.depth[j]*1e6:.0f} ppm, SNR {r2.depth_snr[j]:.1f}")
# second peak check (half / double)
for k in (0.5, 2):
    s = bls.compute_stats(per * k, dur, t0); say(f"  at {k}xP: depth {s['depth'][0]*1e6:.0f} ± {s['depth'][1]*1e6:.0f} ppm")
ph = ((t - t0) / per + 0.5) % 1 - 0.5
intr = np.abs(ph * per) < dur * 0.35; oot = (np.abs(ph * per) > dur) & (np.abs(ph * per) < 3 * dur)
def dep(x, m): return (np.median(x[oot & m]) - np.mean(x[intr & m])) * 1e6, np.std(x[oot & m]) / np.sqrt((intr & m).sum()) * 1e6
for s in np.unique(sec):
    d, de = dep(f, sec == s); say(f"  S{s}: depth {d:.0f} ± {de:.0f} ppm ({(intr & (sec == s)).sum()} in-transit pts)")
n = np.round((t - t0) / per).astype(int)
do, deo = dep(f, n % 2 == 1); dv, dev = dep(f, n % 2 == 0)
say(f"odd {do:.0f} ± {deo:.0f}, even {dv:.0f} ± {dev:.0f} ppm: diff {(do-dv)/np.hypot(deo,dev):.1f} sigma")
d1, d1e = dep(f, np.ones_like(f, bool)); ds, dse = dep(sap, np.ones_like(f, bool))
say(f"PDCSAP {d1:.0f} ± {d1e:.0f} ppm, SAP {ds:.0f} ± {dse:.0f} ppm")
ph2 = ((t - t0) / per) % 1 - 0.5
sm = np.abs(ph2 * per) < dur * 0.35; so = (np.abs(ph2 * per) > dur) & (np.abs(ph2 * per) < 3 * dur)
say(f"secondary at phase 0.5: {(np.median(f[so]) - np.mean(f[sm]))*1e6:.0f} ± {np.std(f[so])/np.sqrt(sm.sum())*1e6:.0f} ppm")
for name, c in (("col", cx), ("row", cy)):
    g = np.isfinite(c); d = np.nanmean(c[intr & g]) - np.nanmedian(c[oot & g]); de = np.nanstd(c[oot & g]) / np.sqrt((intr & g).sum())
    say(f"centroid {name} shift in transit: {d*1e3:.2f} ± {de*1e3:.2f} mpx ({d/de:.1f} sigma)")
g = np.isfinite(bk); say(f"background in - out: {np.nanmean(bk[intr & g]) - np.nanmedian(bk[oot & g]):.2f} e-/s")
# shape: V vs U, binned fold
fig, ax = plt.subplots(2, 1, figsize=(9, 7))
m = np.abs(ph * per * 24) < 4
ax[0].plot(ph[m] * per * 24, f[m], ",", color="0.6")
bins = np.linspace(-4, 4, 81); idx = np.digitize(ph[m] * per * 24, bins)
bm = [np.mean(f[m][idx == k]) if (idx == k).sum() else np.nan for k in range(1, len(bins))]
ax[0].plot(0.5 * (bins[1:] + bins[:-1]), bm, "o-", color="C3", ms=3)
ax[0].set(xlabel="hours from mid-transit", ylabel="PDCSAP (flattened)", title=f"TIC 88481081 SPOC S105-S108, P {per:.5f} d")
ax[0].set_ylim(1 - 2.2 * max(d1, 1000) / 1e6, 1 + 0.002)
m2 = np.abs(ph2 * per * 24) < 4
idx2 = np.digitize(ph2[m2] * per * 24, bins)
bm2 = [np.mean(f[m2][idx2 == k]) if (idx2 == k).sum() else np.nan for k in range(1, len(bins))]
ax[1].plot(ph2[m2] * per * 24, f[m2], ",", color="0.6"); ax[1].plot(0.5 * (bins[1:] + bins[:-1]), bm2, "o-", color="C0", ms=3)
ax[1].set(xlabel="hours from phase 0.5", ylabel="PDCSAP", title="phase 0.5 (secondary eclipse?)"); ax[1].set_ylim(ax[0].get_ylim())
fig.tight_layout(); fig.savefig(HERE / "lc_check.png", dpi=110)
(HERE / "lc_check.txt").write_text("\n".join(out) + "\n")
