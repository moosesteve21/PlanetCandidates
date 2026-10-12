# TIC 240488148 (TYC 3191-503-1)

A ~1.45 R⊕ transit candidate on a K dwarf with a 1.51-day period, found in an
independent BLS search of TESS light curves.

## Discovery

| | |
|---|---|
| Found | 2026-10-12, in search batch b012 (500 stars, run 20:56–23:32 UK time) |
| Pipeline version | commit `93b3f14` of the search code (unpublished) |
| Reviewed | 2026-10-12: per-transit fits, other pipelines (TARS), transit fit, TRICERATOPS, per-pixel depth map |

## Star

TIC 240488148 = TYC 3191-503-1 = Gaia DR3 1967568881023980032; RA 323.62829,
Dec +42.64403; K dwarf, T = 10.17, R* = 0.67 R☉, M* = 0.69 M☉, Teff 4403 K;
contamination ratio 0.09; Gaia RUWE 1.04.

## Signal

| Parameter | Value |
|---|---|
| Period | 1.5125120 ± 0.0000040 d |
| Mid-transit | BJD_TDB 2458712.9421 ± 0.0040 |
| Depth | ~390 ppm (Rp/R* 0.0198 +0.0024/−0.0011) |
| Duration | 1.40 ± 0.09 h |
| Planet radius | ~1.45 (+0.18/−0.08) R⊕ |
| Data | 60 transits: TESS-SPOC FFI S15, S16 (30 min), S56, S76, S82, S83 (200 s) |

## Vetting summary

- **Every sector:** folded depths of 347–433 ppm in all six sectors; 52 of 54 transits dip.
- **Independent pipeline:** TARS gives 405 ± 44 ppm over 71 transits (9.2σ).
- **Consistency:** odd and even transits agree (0.5σ); no secondary eclipse; the period
  is unambiguous (SDE 57); the model-shift test passes.
- **Density:** 3.3 g/cm³ from the transit against 3.2 for the catalogued star (0.0σ).
- **On target:** no 2-min data, so a per-pixel depth map over six TESScut sectors stands
  in for centroids. The target fits best; the nearest neighbours are worse by Δχ² 19.5–26.
- **TRICERATOPS:** FPP 0.11, NFPP 0.018; mostly unresolved-companion scenarios, which
  need high-resolution imaging.
- **New:** not a TOI, CTOI or SPOC TCE.

## Timeline

| Date | Event |
|---|---|
| 2026-10-12 | Found in batch b012; reviewed; Talk post drafted |

## Files

- `tic240488148_sector_folds.png`: the transit folded separately in each sector
- `tic240488148_pixel_depth_map.png`: in-transit flux deficit per pixel, six sectors
- `tic240488148_folded_odd_even.png`: the search's plot (periodogram, fold, odd/even)
- `pht_talk_post_draft.md`: the Talk post draft
