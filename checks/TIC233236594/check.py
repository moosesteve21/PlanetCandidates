#!/usr/bin/env python
"""PHT 4188077 (mkmyers45, 2026-11-23): TIC 233236594, three single transits (S22, S74, S85), P ~282.48 d, TTVs?

1. Load one light curve per sector (SPOC 120 s, else TESS-SPOC, else QLP), normalise.
2. Find each transit: matched-filter scan (fixed trapezoid, T14 12.41 h, ingress 0.91 h, local cubic baseline over
   +-1.6 x T14) within +-2 d of the reported events; fit the mid-time, depth and its error.
3. Linear ephemeris through the three times: residuals and chi2 (the TTV claim).
4. Period aliases: for P/n (n = 1..80), every predicted epoch inside the data is tested with the same filter at the
   predicted time (+-3 h). The alias survives if no covered epoch rejects a dip of the observed depth at > 5 sigma.
Usage: .venv/bin/python investigations/pht_4188077/check.py
"""
import json
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
import lightkurve as lk  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

TIC = 233236594
T14 = 12.41 / 24
TING = 0.91 / 24
OUT = Path(__file__).resolve().parent
REPORTED = {"S85": 3620.9809}


def shape(t, tc):
    x = np.abs(t - tc); half = T14 / 2
    s = np.zeros_like(t); s[x <= half - TING] = 1
    m = (x > half - TING) & (x < half); s[m] = (half - x[m]) / TING
    return s


def fit(t, f, e, tc, relax=False):
    hw = 1.6 * T14
    m = np.abs(t - tc) <= hw
    if m.sum() < 15:
        return None
    tw, fw, ew = t[m], f[m], e[m]
    inn = np.sum(np.abs(tw - tc) < T14 / 2); left = np.sum(tw < tc - T14 / 2); right = np.sum(tw > tc + T14 / 2)
    cad = np.median(np.diff(tw)) if len(tw) > 1 else 1
    side = 0.3 * (hw - T14 / 2)
    if inn * cad < 0.6 * T14:
        return None
    if relax:   # an event at a sector edge: baseline on one side is enough (cubic reduced to linear)
        if max(left, right) * cad < side:
            return None
    elif left * cad < side or right * cad < side:
        return None
    dt = tw - tc; w = 1 / ew
    one_sided = relax and min(left, right) * cad < side
    cols = [np.ones_like(dt), dt] if one_sided else [np.ones_like(dt), dt, dt**2, dt**3]
    A = np.vstack(cols + [-shape(tw, tc)]).T
    c, *_ = np.linalg.lstsq(A * w[:, None], fw * w, rcond=None)
    r = (fw - A @ c) * w; chi = float(r @ r)
    cov = np.linalg.inv((A * w[:, None]).T @ (A * w[:, None]))
    s = max(chi / max(len(tw) - 5, 1), 1.0)
    A0 = A[:, :-1]; c0, *_ = np.linalg.lstsq(A0 * w[:, None], fw * w, rcond=None); r0 = (fw - A0 @ c0) * w
    return dict(chi2=chi, depth=float(c[-1]), depth_err=float(np.sqrt(cov[-1, -1] * s)),
                dchi2=(float(r0 @ r0) - chi) / s, scale=s, n=int(m.sum()))


def load():
    res = lk.search_lightcurve(f"TIC {TIC}", mission="TESS")
    tab = res.table; pick = {}
    for author, exp in [("SPOC", 120), ("TESS-SPOC", None), ("QLP", None)]:
        for j in range(len(res)):
            if np.ma.is_masked(tab["sequence_number"][j]):
                continue
            s = int(tab["sequence_number"][j])
            if str(tab["author"][j]) != author or s in pick or (exp and float(tab["exptime"][j]) != exp):
                continue
            pick[s] = j
    T, F, E, S = [], [], [], []
    for s, j in sorted(pick.items()):
        lc = res[j].download(quality_bitmask="default").remove_nans().normalize()
        t = np.asarray(lc.time.value, float); f = np.asarray(lc.flux.value, float); e = np.asarray(lc.flux_err.value, float)
        ok = np.isfinite(t) & np.isfinite(f) & np.isfinite(e) & (e > 0)
        T.append(t[ok]); F.append(f[ok]); E.append(e[ok]); S.append(np.full(ok.sum(), s))
        print(f"sector {s}: {tab['author'][j]} {float(tab['exptime'][j]):.0f} s, {ok.sum()} pts", flush=True)
    return np.concatenate(T), np.concatenate(F), np.concatenate(E), np.concatenate(S)


def best_time(t, f, e, guess, half=2.0, relax=False):
    grid = np.arange(guess - half, guess + half, 1 / 1440)
    vals = [(g, fit(t, f, e, g, relax)) for g in grid]
    vals = [(g, v) for g, v in vals if v and v["depth"] > 0]
    g, v = max(vals, key=lambda x: x[1]["dchi2"])
    d = np.array([x[1]["dchi2"] for x in vals]); gg = np.array([x[0] for x in vals])
    near = gg[(d >= v["dchi2"] - 1)]
    return g, v, max((near.max() - near.min()) / 2, 1 / 1440)


def main():
    t, f, e, s = load()
    o = np.argsort(t); t, f, e, s = t[o], f[o], e[o], s[o]
    # 1. find the three events: S85 reported; search S22 and S74 sectors for the deepest 12 h dip
    events = {}
    for sec in (22, 74, 85):
        m = s == sec
        ts = t[m]
        grid = np.arange(ts.min() + T14 / 2, ts.max() - T14 / 2, 10 / 1440)
        cand = [(g, fit(t, f, e, g, relax=True)) for g in grid]
        cand = [(g, v) for g, v in cand if v and v["depth"] > 0]
        g, v = max(cand, key=lambda x: x[1]["dchi2"])
        tc, v, err = best_time(t, f, e, g, half=0.3, relax=True)
        events[sec] = dict(t_mid=tc, err_h=err * 24, depth_ppm=v["depth"] * 1e6, depth_err_ppm=v["depth_err"] * 1e6,
                           dchi2=v["dchi2"])
        print(f"S{sec}: t_mid {tc:.4f} +- {err*24:.2f} h, depth {v['depth']*1e6:.0f} +- {v['depth_err']*1e6:.0f} ppm, "
              f"dchi2 {v['dchi2']:.0f}", flush=True)
    tm = np.array([events[k]["t_mid"] for k in (22, 74, 85)]); er = np.array([events[k]["err_h"] for k in (22, 74, 85)]) / 24
    # 2. ephemeris with integer epochs from the S74-S85 gap
    p0 = tm[2] - tm[1]
    n1 = round((tm[1] - tm[0]) / p0)
    E = np.array([0, n1, n1 + 1], float)
    A = np.vstack([np.ones(3), E]).T / er[:, None]
    (t0, P), *_ = np.linalg.lstsq(A, tm / er, rcond=None)
    oc = (tm - (t0 + P * E)) * 24
    chi2 = float(np.sum((oc / (er * 24)) ** 2))
    print(f"P = {P:.4f} d (epochs 0, {n1}, {n1+1}); O-C h {np.round(oc,2)}, errors h {np.round(er*24,2)}, chi2 {chi2:.1f} (1 dof)")
    # 3. aliases P/n
    depth = np.mean([events[k]["depth_ppm"] for k in events]) * 1e-6
    rows = []
    for n in range(1, 81):
        Pn = P / n
        kmin = int(np.floor((t.min() - t0) / Pn)) - 1; kmax = int(np.ceil((t.max() - t0) / Pn)) + 1
        covered, rejected, worst = 0, 0, None
        for k in range(kmin, kmax + 1):
            tc = t0 + k * Pn
            if any(abs(tc - x) < 1 for x in tm):
                continue
            best = None
            for d in np.arange(-3, 3.01, 0.5) / 24:   # allow +-3 h TTV
                v = fit(t, f, e, tc + d)
                if v is None:
                    continue
                # significance with which a dip of the observed depth is rejected
                z = (depth - v["depth"]) / v["depth_err"]
                best = z if best is None else min(best, z)
            if best is None:
                continue
            covered += 1
            if best > 5:
                rejected += 1
            worst = best if worst is None else max(worst, best)
        rows.append(dict(n=n, P=Pn, covered=covered, rejected=rejected, max_z=worst))
    allowed = [r for r in rows if r["rejected"] == 0]
    print("aliases allowed (no covered epoch rejects the dip at > 5 sigma):")
    for r in allowed:
        print(f"  n={r['n']:>2}  P={r['P']:.3f} d  covered epochs {r['covered']}")
    (OUT / "result.json").write_text(json.dumps(dict(events=events, P=P, t0=t0, epochs=E.tolist(), oc_h=oc.tolist(),
                                                     chi2=chi2, aliases=rows), indent=1, default=float) + "\n")
    # plot the three events
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.2), sharey=True)
    for ax, sec in zip(axes, (22, 74, 85)):
        tc = events[sec]["t_mid"]; m = np.abs(t - tc) < 1.2
        ax.plot((t[m] - tc) * 24, (f[m] - 1) * 1e6, ".", ms=2, color="0.6")
        b = np.arange(-28.8, 28.8, 1.0); idx = np.digitize((t[m] - tc) * 24, b)
        med = [np.median(f[m][idx == k]) if np.sum(idx == k) > 2 else np.nan for k in range(1, len(b))]
        ax.plot(b[:-1] + 0.5, (np.array(med) - 1) * 1e6, "-", color="C3")
        ax.set_title(f"S{sec}: {tc:.3f} BTJD, {events[sec]['depth_ppm']:.0f} ppm", fontsize=9)
        ax.set_xlabel("hours from fitted mid-time")
    axes[0].set_ylabel("ppm"); axes[0].set_ylim(-9000, 3000)
    fig.tight_layout(); fig.savefig(OUT / "events.png", dpi=110)


if __name__ == "__main__":
    main()
