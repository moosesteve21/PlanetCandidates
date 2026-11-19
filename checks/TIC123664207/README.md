# TIC 123664207 (TOI-2493.01): period alias check of a community report

**Report:** [Planet Hunters TESS Talk, 2026-11-19](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2112/4185323)
(mkmyers45): transits in S33 (BTJD 2225.81), S98 (4043.47) and S107 (4280.60), giving P = 79.03 d; ~1.8 ppt, T14 6.07 h.

**Checked 2026-11-19** with `aliases.py`. The S98–S107 gap (237.13 d) fixes P = 237.13/k. Every k up to 39 (P ≥ 6.08 d)
was tested against the S33 transit, then against every other predicted transit in the TESS data. Data: S6 (TESS-SPOC),
S33, S87, S98, S107, S108 (SPOC). Box depth over the central 80% of T14 with a local linear baseline. A period counts as ruled out
when a predicted transit with ≥ 50% coverage reads depth + 3σ below half the posted depth. Per-alias details are in `aliases.json`.

| Result | |
|---|---|
| Posted transits (our box depths) | S33 1,613 ± 194, S98 1,363 ± 207, S107 1,377 ± 209 ppm |
| Periods that fit all three (within 0.5 h) | 79.030 d / k for k = 1…13 (79.03, 39.51, 26.34, … 6.08 d) |
| Ruled out | all but 79.03 d: each shorter alias predicts 2–22 more transits in S6/S33/S87/S98, and they are flat |
| 79.03 d | no other predicted transit falls in the data, consistent with the three posted events |
| Linear ephemeris | T0 = 2225.808 BTJD, P = 79.0297 d (residuals ≤ 0.5 h) |
| Next transits | BTJD ~4438.64 (2027-02-02 ~03 UTC), ~4517.67 (2027-04-22 ~04 UTC); ±1 h or so |
