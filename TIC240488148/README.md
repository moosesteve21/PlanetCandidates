# TIC 240488148 (TYC 3191-503-1)

A ~1.45 R⊕ transit candidate on a K dwarf with a 1.51-day period, found in an
independent BLS search of TESS light curves.

## Status update (2026-11-21, current pipeline)

The search code has improved a lot since these candidates were first posted in October 2026. On 2026-11-21 we re-ran the star through the current version of KESTREL (the development version; it reaches the public KESTREL repository in the next code update), from the blind search through every vetting step. The original October record below is unchanged.

Our two criteria for calling a signal a candidate (from our methods paper, in preparation):
- **A:** the transit fit agrees with the star's density, the per-pixel depth map puts the dip on the target, and the dip appears in TARS light curves (an independent reduction) at ≥ 3σ against random phases.
- **B:** A, plus a TRICERATOPS false-positive probability (FPP) below 0.5 and a nearby-star FPP (NFPP) below 0.001.

**Signal 1 (the one posted in October)**

| Check | Result (2026-11-21) |
|---|---|
| Blind search | Top signal again: P = 1.512524 d, 348 ppm, SNR 15.6, SDE 57.8, 73 transits in 6 sectors, odd/even 0.9σ |
| Transit fit | Consistent with the star: density 2.8 vs 3.2 g/cm³ (+0.3σ); b = 0.46, T14 1.5 h, Rp ≈ 1.35 R⊕ |
| Depth map | On target, Δχ² 22.4 |
| Other reductions | QLP (two versions) and TESS-SPOC all support it |
| TARS | 385 ± 42 ppm over 76 transits; 6.5σ against random phases |
| TRICERATOPS | FPP 0.062 ± 0.001, NFPP 0.0105 ± 0.0002 (798 field stars) |

**Verdict: meets A, fails B on NFPP** (0.010 against the 0.001 limit): in this crowded field TRICERATOPS can't exclude an eclipsing binary among the nearby stars. Ground photometry of the neighbours would settle that.

**Signal 2 (new: P = 3.6004 d)**

The current search keeps looking after the first signal and finds a second one on this star, which the October search didn't report. It is weaker, and we report it here because anyone re-testing this public star could find it too.

| Check | Result (2026-11-21) |
|---|---|
| Blind search | P = 3.600419 d, 341 ppm, SNR 8.3, SDE 15.6, 32 transits in 6 sectors, odd/even 0.1σ; not an alias of signal 1 (ratio 2.38) |
| Transit fit | Passes, but with tension: T14 0.9 h is short for this star, so the fitted density is 29 vs 3.2 g/cm³ (−2.4σ); Rp ≈ 1.4 R⊕ |
| Depth map | On target, Δχ² 29.5 |
| Other reductions | QLP (two versions) and TESS-SPOC all support it |
| TARS | 471 ± 78 ppm over 30 transits; 6.0σ against random phases |
| TRICERATOPS | FPP 0.32 ± 0.01, NFPP 0.0016 ± 0.0001 |

**Verdict: meets A, fails B** (NFPP 0.0016). The short duration is the main open question: an eccentric or grazing orbit, or a signal from something other than this star. Treat it as a weaker candidate than signal 1.

New figures: `2026-11-21_search_P1.5125.png` and `2026-11-21_search_P3.6004.png` (periodogram, fold, odd/even), `2026-11-21_depth_map_P1.5125.png` and `2026-11-21_depth_map_P3.6004.png`.

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
| 2026-10-13 | Posted to Planet Hunters TESS Talk: https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4154549 |
| 2026-10-12 | Found in batch b012; reviewed; Talk post drafted |

## Files

- `tic240488148_sector_folds.png`: the transit folded separately in each sector
- `tic240488148_pixel_depth_map.png`: in-transit flux deficit per pixel, six sectors
- `tic240488148_folded_odd_even.png`: the search's plot (periodogram, fold, odd/even)
- `pht_talk_post.md`: the Talk post as published
