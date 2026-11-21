# TIC 147226218 (CD−43 9842)

A ~1.7 R⊕ transit candidate on an early K dwarf with a 3.87-day period, found in an
independent BLS search of TESS light curves.

## Status update (2026-11-21, current pipeline)

The search code has improved a lot since these candidates were first posted in October 2026. On 2026-11-21 we re-ran the star through the current version of KESTREL (the development version; it reaches the public KESTREL repository in the next code update), from the blind search through every vetting step. The original October record below is unchanged.

Our two criteria for calling a signal a candidate (from our methods paper, in preparation):
- **A:** the transit fit agrees with the star's density, the per-pixel depth map puts the dip on the target, and the dip appears in TARS light curves (an independent reduction) at ≥ 3σ against random phases.
- **B:** A, plus a TRICERATOPS false-positive probability (FPP) below 0.5 and a nearby-star FPP (NFPP) below 0.001.

| Check | Result (2026-11-21) |
|---|---|
| Blind search | Top signal again: P = 3.871562 d, 540 ppm, SNR 14.1, SDE 34.4, 19 transits in 4 sectors, odd/even 1.4σ |
| Transit fit | Consistent with the star: density 1.8 vs 3.7 g/cm³ (+1.7σ); Rp ≈ 1.7 R⊕ |
| Depth map | **Not detected:** no star in the field, the target included, fits clearly better than no dip (Δχ² 14.3) |
| Pixel centroid | Dimming centre 79″ from the target, flagged off-target |
| Neighbour | TIC 147226209 varies with an 11.7067 d period, three times the signal's period, and dims by 419 ± 198 ppm at the dip times (2.1σ) |
| Other reductions | QLP (two versions) and TESS-SPOC all show the dip |
| TARS | 590 ± 92 ppm over 12 transits; 6.0σ against random phases |
| TRICERATOPS | FPP 0.22 ± 0.01, **NFPP 0.14 ± 0.01** (1,366 field stars): "likely nearby false positive" |

**Verdict: fails criterion A. We no longer consider this a planet candidate on TIC 147226218.** The dip is real (it is in every reduction, including TARS), but the pixel data don't place it on the target, and the most likely source is a nearby star. This is consistent with the correction we posted on 2026-10-14, when our first pixel map was found to favour the target only weakly.

New figures: `2026-11-21_search_P3.8716.png` (periodogram, fold, odd/even), `2026-11-21_depth_map.png`.

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
