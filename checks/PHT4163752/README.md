# TOI-2940, 2954, 3157 and 3207: KESTREL checks (PHT Talk 2110/4163752, group 3)

These four TOIs were listed on Planet Hunters TESS as "raw" candidates. Their planet radius shows as 0 on ExoFOP
because the TIC has no stellar radius for them. We searched each blind with KESTREL (development version: full
period grid, v2 stopping rules and cleaning) using SPOC 2-min and QLP light curves, then vetted the signals.

| TOI | TIC | Period (d) | Depth, SPOC (ppt) | Secondary at phase 0.5 (ppm) | Odd/even | Gaia RUWE | KESTREL flags |
|---|---|---|---|---|---|---|---|
| 2940.01 | 5224772 | 4.59915 | 22-26 | 1635 ± 298 | 0.1σ | 51.6 | significant secondary |
| 2954.01 | 464328419 | 4.84012 | 23-27 | 7 ± 128 | 1.9σ | 1.0 | V-shaped; depth varies by sector |
| 3157.01 | 456962262 | 2.88227 | 38-79 | 5964 ± 696 | 2.8σ | 17.9 | V-shaped; significant secondary; depth varies by sector |
| 3207.01 | 320994166 | 4.09963 | 39-62 | 1030 ± 324 | 4.2σ | 4.7 | V-shaped; depth varies by sector |

- `*_kestrel.png`: KESTREL's standard plot (periodogram, fold, odd vs even transits).
- `*_check.png`: the fold over the whole orbit (inset: phase 0.5) and the transit depth in each sector (blue SPOC
  2-min, orange QLP FFI). Made by `figure.py` from the same light curves (1-day running median, eclipses masked).
- QLP depths are lower than SPOC's for all four; FFI apertures and dilution corrections differ, so compare SPOC
  sectors with each other.
- Further signals: TIC 456962262 at 1.0518 d (SNR 14, depth varies 1-21 ppt between sectors, missing in some);
  TIC 464328419 at 17.112 d (SNR 10, transits at data edges, ambiguous period). Both flagged.

Steve Price (moosehunter21), KESTREL, 2026-10-27.
