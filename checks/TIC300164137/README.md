# TIC 300164137: transit timing check of a community report

**Report:** [Planet Hunters TESS Talk, 2026-11-18](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4185280)
(mkmyers45): ~2.2 ppt, 11.75 h transits every ~49.66 d on a T = 11.75 F subgiant (1.97 R☉), with possible TTVs. orionlee
noted strong TTVs and on-target dips.

**Checked 2026-11-19** with `ttv.py`: one fixed trapezoid shape (T14 11.75 h, ingress 0.55 h) fitted to each transit
separately, with a free mid-time, depth and local linear baseline. Mid-times come from a ±1.5 d scan; errors from Δχ² = 1,
scaled by the reduced χ² when above 1. The best light curve per sector (SPOC, then TESS-SPOC, then QLP). Results are in `ttv.json`.

| Result | |
|---|---|
| Transits timed | 19, S1 to S98 (2,682 d); errors 4–29 min |
| Left out | S96 (transit in the orbit gap), S30 (no dip), S68 and S97 (systematics: reduced χ² 3.5 and 32) |
| O−C against P = 49.66 d | smooth arch, −750 min (S1) → +440 min (S28–S66) → −590 min (S98): ~20 h peak to peak (figure) |
| Constant period | ruled out: χ² 82,893 for 17 dof (quadratic 708/16, cubic 40/15, rms ~13 min) |
| TTV super-period | > ~5,000 d; less than one cycle covered |
| Depths | steady, ~1.8–2.4 ppt |
| Light-travel time | can't explain ±10 h (would need a ~70 AU reflex orbit within the span: hundreds of M☉), so dynamical |
| QLP TCE period 264.121 d | 5.32 × 49.66 d, not an alias: the TTV threw off the period search |
| Next windows (O−C polynomials, degree 2–4; ±4 h at best) | BTJD ~4410.4 (2027-01-04), ~4460.0 (2027-02-23), ~4509.6 (2027-04-14); Dec −66° |

![O-C](oc.png)
