# TIC 302453503 (L 642-3)

A ~1.2 R⊕ transit candidate on an M1.5 dwarf, found in an independent BLS search of TESS light curves.

## Discovery

| | |
|---|---|
| Found | 2026-10-12, 10:10 (UK time), in search batch b007 (100 stars, run started 09:43) |
| Pipeline version | commit `5fe68b3` of the search code (unpublished) |
| Reviewed | 2026-10-12: SPOC DV check, per-transit fits, centroids, other pipelines, transit fit, TRICERATOPS |

## Star

TIC 302453503 = L 642-3 = Gaia DR3 6815237513835256064; RA 322.56736, Dec −24.88804; M1.5 dwarf, T = 10.35, R* = 0.507 ± 0.015 R☉, M* = 0.505 M☉, Teff 3621 K; contamination ratio 0.0025; Gaia RUWE 1.14.

## Signal

| Parameter | Value |
|---|---|
| Period | 3.629156 ± 0.000005 d |
| Mid-transit | BJD_TDB 2460158.84281 ± 0.00158 |
| Depth | ~440 ppm (Rp/R* 0.0209) |
| Duration | ~1.6–1.7 h |
| Planet radius | ~1.16 R⊕ |
| Data | 29 transits: SPOC 2-min S1, S28; TESS-SPOC S68; QLP S92, S95 |

## Vetting summary

- **Reductions:** the dip is in all five reductions used by the search. TARS (an independent pipeline) gives 559 ± 91 ppm, with the dip in every sector.
- **Consistency:** 25 of 26 transits dip; odd and even transits agree; no secondary eclipse; the period is unambiguous.
- **Density:** the transit's stellar density, 5.0 g/cm³, matches the catalogued star's 5.5 (0.1σ).
- **On target:** the centroid shift is consistent with zero, and the brightest neighbours are excluded at more than 11σ.
- **TRICERATOPS:** FPP 0.04–0.06, NFPP ≤ 0.0003, a "likely planet". Validation is held back by the unresolved-companion scenarios; no high-resolution imaging exists.
- **New:** not a TOI, CTOI or SPOC TCE.

## Timeline

| Date | Event |
|---|---|
| 2026-10-12 | Found in batch b007; reviewed |
| 2026-10-12 | Posted to Planet Hunters TESS Talk: https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4153490 |
| — | Email to the Visual Survey Group (all three candidates, `../vsg_email_draft.md`) drafted, not sent |

## Files

- `tic302453503_folded_odd_even.png`: folded light curve and odd/even comparison (from the search)
- `tic302453503_individual_transits.png`: each transit with the fitted model
- The Talk post (the Visual Survey Group email, covering all three candidates, is in `vsg_email_draft.md` at the top of the repo)
