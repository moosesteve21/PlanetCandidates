# TIC 147226218 (CD−43 9842)

A ~1.7 R⊕ transit candidate on an early K dwarf with a 3.87-day period, found in an
independent BLS search of TESS light curves.

## Discovery

| | |
|---|---|
| Found | 2026-10-13, in search batch b018 (300 stars, run 14:34–15:52 UK time) |
| Pipeline version | commit `e859bb1` of the search code (unpublished; recorded at run time as `21b6e08`, the same code before an author-email rewrite) |
| Reviewed | 2026-10-13: per-transit fits, other pipelines (TARS), transit fit, TRICERATOPS, per-pixel depth map |

## Star

TIC 147226218 = CD−43 9842 = Gaia DR3 6000611238623937152; RA 230.61974, Dec −43.86789;
early K dwarf at 77 pc, T = 10.29, R* = 0.67 R☉, M* = 0.79 M☉, Teff 4843 K;
contamination ratio 0.095; Gaia RUWE 1.12.

## Signal

| Parameter | Value |
|---|---|
| Period | 3.871562 ± 0.000010 d |
| Mid-transit | BJD_TDB 2459336.6807 ± 0.0031 |
| Depth | ~530 ppm (Rp/R* 0.0231 +0.0024/−0.0013) |
| Duration | 2.45 ± 0.17 h |
| Planet radius | ~1.69 (+0.18/−0.09) R⊕ |
| Data | ~20 transits: TESS-SPOC FFI S38 (10 min), S65 (200 s); QLP S102, S103 (200 s) |

## Vetting summary

- **Every sector:** folded depths of 463–646 ppm in all four sectors; 18 of 18 transits dip.
- **Independent pipeline:** TARS gives 505 ± 85 ppm over 12 transits (5.9σ).
- **Consistency:** odd and even transits agree; no secondary eclipse; the period is
  unambiguous (SDE 34); the model-shift test passes.
- **Density:** 1.6 g/cm³ from the transit against 3.7 for the catalogued star (1.7σ).
- **Position (corrected 2026-10-14):** a per-pixel depth map over four TESScut sectors
  favours the target: it fits best in three sectors (S103 can't tell). The nearest
  neighbours are worse by Δχ² ≈ 8 (TIC 147219144, T 14.8, 16″) and ≈ 12 (TIC 147226219,
  T 14.4, 31″). The first version (in the Talk post) gave 27.8 and 35.2: it used smaller
  per-pixel errors, before each pixel's error got a floor from its out-of-transit
  scatter. The pixels alone don't rule out the 16″ neighbour, which would need a ~3%
  eclipse.
- **TRICERATOPS:** FPP 0.16, NFPP 0.077; mostly unresolved-companion scenarios.
- **New:** not a TOI, CTOI or SPOC TCE.

## Timeline

| Date | Event |
|---|---|
| 2026-10-14 | Pixel-map margins corrected (more conservative errors): Δχ² ≈ 8–12, not 27.8–35.2; follow-up in the Talk thread |
| 2026-10-14 | Posted to Planet Hunters TESS Talk: https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4155277 |
| 2026-10-13 | Found in batch b018; reviewed; Talk post drafted |

## Files

- `tic147226218_sector_folds.png`: the transit folded separately in each sector
- `tic147226218_pixel_depth_map.png`: in-transit flux deficit per pixel, four sectors (as posted)
- `tic147226218_pixel_depth_map_2026-10-14.png`: the same, rerun with the corrected errors
- `tic147226218_folded_odd_even.png`: the search's plot (periodogram, fold, odd/even)
- `pht_talk_post.md`: the Talk post as published
