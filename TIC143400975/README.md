# TIC 143400975 (StKM 1-845)

A transit candidate on a K7 dwarf, probably on a near-grazing orbit, found in an independent BLS search of TESS light curves.

## Discovery

| | |
|---|---|
| Found | 2026-10-12, 15:40 (UK time), in search batch b009 (200 stars, run started 15:16) |
| Pipeline version | commit `b45761d` of the search code (unpublished) |
| Reviewed | 2026-10-12: SPOC DV check, per-transit fits, centroids, other pipelines, transit fit and density test, TRICERATOPS |

## Star

TIC 143400975 = StKM 1-845 = Gaia DR3 3830446413771545728; RA 154.84638, Dec −1.33093; K7 dwarf, T = 10.13, R* = 0.627 ± 0.019 R☉, M* = 0.610 M☉, Teff 3963 K; contamination ratio 0.0002; Gaia RUWE 1.16.

## Signal

| Parameter | Value |
|---|---|
| Period | 4.87876 ± 0.00001 d |
| Mid-transit | BTJD 1521.7362 ± 0.0029 (BJD 2458521.7362) |
| Depth | 640 ± 79 ppm |
| Duration | 0.85 ± 0.11 h (a central transit would last 2.33 h) |
| Geometry | near-grazing: b ≈ 0.96, Rp/R* ≈ 0.030 |
| Planet radius | ~2 R⊕ (poorly constrained when grazing) |
| Data | 21 transits: SPOC 2-min S35, S45, S46; TESS-SPOC S8, S72; QLP S89 |

## Vetting summary

- **Reductions:** the dip is in all five reductions used by the search. TARS gives 628 ± 121 ppm, with the dip in every sector.
- **Consistency:** 20 of 21 transits dip; odd and even transits agree; no secondary eclipse; the period is unambiguous (SDE 20.2).
- **Duration:** the short dip fits a grazing transit of the catalogued star. The best fit has ρ* 3.1 against 3.5 g/cm³, and fixing it at the catalogue value costs Δχ² = 0.1.
- **On target:** the centroid shift is consistent with zero, and the only plausible neighbour is excluded at 16σ.
- **TRICERATOPS:** FPP 0.39, NFPP 0.000, a "likely planet" but weaker than TIC 302453503 because of the V-shaped, grazing dip.
- **New:** not a TOI, CTOI or SPOC TCE.

## Timeline

| Date | Event |
|---|---|
| 2026-10-12 | Found in batch b009; reviewed |
| — | Talk post drafted, held back until the TIC 302453503 thread has had replies |

## Files

- `tic143400975_folded_odd_even.png`: folded light curve and odd/even comparison (from the search)
- `tic143400975_individual_transits.png`: each transit with the fitted model
- `pht_talk_post_draft.md`: the Talk post (not posted)
