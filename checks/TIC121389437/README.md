# TIC 121389437: KESTREL check of the 11.9 d dips (PHT Talk 2110/4163707)

Reported on Planet Hunters TESS by Datsk; pixel-level analyses in the thread by orionlee, mhuten and rabtsevich.
Star: F star, Teff 6549 K, R 2.56 R☉, Tmag 9.97. Neighbours discussed: TIC 121389438 (Tmag 13.6, 5.2" SW) and the
bright giant TIC 121389425 (Tmag 5.3).

- `kestrel_P11.898.png`: blind KESTREL search (development version), no period given. Only signal:
  P = 11.897887 d, depth 2153 ppm, SNR 61, 9 transits (S8, 34, 61, 88, 99); odd/even 0.6σ; secondary −38 ± 45 ppm;
  sector depths S34 2269, S61 1957, S88 (QLP) 2099, S99 2213 ppm. Five other reductions (QLP SAP, SPOC SAP,
  TESS-SPOC PDCSAP and SAP) show the same dip; no background change during transits.
- Transit fit: grazing (b ≈ 0.93, Rp/R★ ≈ 0.052, T14 ≈ 6.5 h); about 14.5 R⊕ if on the target.
- `depth_map.png`: per-pixel in-transit flux deficit (bottom row, deficit / error) from TESScut cutouts, fitted with a
  star image at each catalogued star's position. Δχ² relative to the best source:

  | Sectors | Better fit |
  |---|---|
  | S8 | TIC 121389438 by 9.6 |
  | S34 | TIC 121389438 by 205 |
  | S61 + S88 + S99 | TIC 121389437 (target) by ~212 combined |
  | all five | TIC 121389438 by 3.2 (a tie; the two are 0.25 px apart) |

  All other stars within 2.5′ fit far worse (Δχ² > 690). The bright giant dominates the cutouts (top right) in
  S8–S88.

Steve Price (moosehunter21), KESTREL, 2026-10-28.
