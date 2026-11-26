#!/usr/bin/env python3
"""oc21.py - O-C of TIC 300164137 with S30 and S68 added (recheck.py, QLP, default mask) to the 19 transits of ttv.json."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = [x for x in json.load(open("ttv.json")) if not x["edge"] and x["depth_ppm"] > 800 and x["red_chi2"] < 2.5 and x["sector"] != 96]
add = [x for x in json.load(open("recheck.json")) if x["author"] == "QLP" and x["mask"] == "default"]
n = np.array([x["n"] for x in rows] + [x["n"] for x in add]); tc = np.array([x["tc"] for x in rows] + [x["tc"] for x in add])
e = np.array([x["err_min"] for x in rows] + [x["err_min"] for x in add])
new = np.r_[np.zeros(len(rows), bool), np.ones(len(add), bool)]
A = np.vstack([np.ones_like(n), n]).T.astype(float); W = 1 / e ** 2
p = np.linalg.solve(A.T @ (A * W[:, None]), A.T @ (W * tc)); oc = (tc - A @ p) * 1440
for deg in (2, 3, 4):
    cf = np.polyfit(n, tc, deg, w=1 / e); r = (tc - np.polyval(cf, n)) * 1440
    pr = [np.polyval(cf, k) for k in (8, 9, 10)]
    print(f"degree {deg}: chi2 {np.sum((r / e) ** 2):.0f} for {len(n) - deg - 1} dof, rms {np.std(r):.1f} min; "
          f"n=8,9,10 at BTJD {pr[0]:.2f}, {pr[1]:.2f}, {pr[2]:.2f}")
print(f"{len(n)} transits; linear P = {p[1]:.5f} d")
fig, ax = plt.subplots(figsize=(9, 4))
ax.errorbar(tc[~new], oc[~new], e[~new], fmt="o", ms=4, label="19 transits (2026-11-19)")
ax.errorbar(tc[new], oc[new], e[new], fmt="s", ms=6, color="C3", label="S30, S68 re-measured (2026-11-26)")
ax.axhline(0, color="k", lw=0.5); ax.legend(fontsize=8)
ax.set(xlabel="Mid-time (BTJD)", ylabel="O - C (min)", title=f"TIC 300164137: per-transit O-C vs linear P = {p[1]:.4f} d ({len(n)} transits)")
fig.tight_layout(); fig.savefig("oc21.png", dpi=120)
