# PlanetCandidates

Discoveries from an independent search of TESS light curves, as submitted: transit
candidates posted for the community, and variable stars submitted to the AAVSO
International Variable Star Index (VSX). Each object has its own folder. Its README
records when and how it was found, its parameters, the vetting or analysis, and what
has been submitted where.

Only material that has been submitted, or is drafted for submission, is kept here.

[discovery_log.md](discovery_log.md) holds dated fingerprints (SHA-256 hashes) of candidates
found but not yet made public, so the date each was found can be checked later.

[Is it a planet?](guide/) is a write-up of lessons learned from signals that looked like
planets and weren't, with annotated examples from the search (a request for comments).

## Transit candidates

| Candidate | Found | Summary | Status |
|---|---|---|---|
| [TIC 147226218](TIC147226218/) (CD−43 9842) | 2026-10-13, batch b018 | P = 3.872 d, ~530 ppm, ~1.7 R⊕, K dwarf; TARS 5.9σ; pixel map favours the target (Δχ² ≈ 8–12); FPP 0.16 | [Posted to Planet Hunters TESS](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4155277) |
| [TIC 240488148](TIC240488148/) (TYC 3191-503-1) | 2026-10-12, batch b012 | P = 1.513 d, ~390 ppm, ~1.45 R⊕, K dwarf; TARS 9.2σ; on target by pixel map; FPP 0.11 | [Posted to Planet Hunters TESS](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4154549) |
| [TIC 302453503](TIC302453503/) (L 642-3) | 2026-10-12, batch b007 | P = 3.629 d, ~440 ppm, ~1.2 R⊕, M1.5 dwarf; TRICERATOPS FPP 0.04–0.06 | Posted to Planet Hunters TESS |

## Checks of community reports

Independent checks of candidates reported by others, with the figures linked from the replies.

| Star | Report | Result |
|---|---|---|
| [KOI-5005.01 (KIC 3755522)](checks/KOI5005/) | [PHT Talk, 2026-10-30](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4167529): Kepler 252 d, ~200 ppm, four dips; Kepler false positive (centroid offset); signal on the 2.4″ companion? | Four dips 179–239 ppm, consistent (χ² 3.6, 3 dof), 10.9σ against random times; only 3 other windows in four years dip ≥ 150 ppm. Centroid shifts point away from B in all four events (A χ² 20.1, B 0.5): on B, ~680 ppm, ~2.2 R⊕ |
| [TIC 278708716](checks/TIC278708716/) | [PHT Talk, 2026-10-30](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4167303): 17.214 d, ~2.5 ppt, ~4 h, K dwarf; is the 22 Jun 2026 (S105) transit too shallow? | 2672 ± 112 ppm over five transits (S28, S68, S95); TARS 10.5σ against random phases; in S105 TESScut photometry the 22 Jun transit is 2.1–2.6 ppt, within about 2σ of the rest; depth map puts the dip on the target (the 55″ neighbour 502 worse in Δχ²) |
| [TIC 306990399 (TOI-5034)](checks/PHT4165442/) | [PHT Talk, 2026-10-28](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4165442): second signal, 4.705 d | Recovered blind (third signal; 4.70516 d, TARS 7.5σ, on-target centroid). The blind search also finds 13.375 d (SPOC TCE 2, unpromoted): TARS 8.8σ, on target by centroid and depth map |
| [TIC 149628034](checks/TIC149628034/) | [PHT Talk, 2026-10-28](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4165512): ~1.4 R⊕, 6.767 d, K7 dwarf, unpromoted TCE | 425 ± 27 ppm over ~125 transits; TARS 9.0σ against random phases; on target by the SPOC centroid (TIC 149628035 at 21.6″ excluded at 7.0σ) and the depth map (40 sectors); imaging for anything closer |
| [TIC 121389437](checks/TIC121389437/) | [PHT Talk, 2026-10-26](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4163707): V-shaped dips, ~11.9 d, CTOI | Recovered blind at 11.8979 d (9 transits, 2.2 ppt, odd/even and sector depths consistent, grazing fit); depth map can't separate the target from TIC 121389438 at 5.2": S34 favours the neighbour strongly, S61/S88/S99 the target |
| [TOI-2940, 2954, 3157, 3207](checks/PHT4163752/) | [PHT Talk, 2026-10-26](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4163752): four TOIs listed without radii (no TIC stellar radius) | All four recovered at the TOI periods; all show eclipsing-binary signs (secondaries on 2940 and 3157, V shapes, odd/even 4.2σ on 3207, SPOC depth changes; Gaia RUWE 51.6 / 1.0 / 17.9 / 4.7) |
| [TIC 50717149](checks/TIC50717149/) | [PHT Talk, 2026-10-26](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4162521): possible ~0.4 d single transit in S99, F dwarf | A 0.4 d box at the event gives 87 ± 108 ppm (a 5 R⊕ planet would make ~1,400-2,700 ppm); a blind KESTREL search of S7, 34, 61, 88, 99 found no periodic signal |
| [TIC 302492175](checks/TIC302492175/) | [PHT Talk, 2026-09-03](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4126968): S32 event, P 41.6538 d, HD 35956 | One ~150 ppm, ~5 h event that ends at a momentum dump on a saturated star; the period is not supported (S98 predicted time flat) |
| [TIC 92350382](checks/TIC92350382/) | [PHT Talk, 2026-10-21](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4160105): 2.90 d, 442 ppm and 7.37 d, 638 ppm, M0.5 dwarf | Both in the independent TARS light curves (3.0σ and 5.6σ against random phases); depth map puts signal 1 on the target; the S1 single dip is a background artefact |
| [TIC 348760393](checks/TIC348760393/) | [PHT Talk, 2026-10-23](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4161335): 12.389 d, ~865–1240 ppm (~1.7 R⊕), M dwarf | Top peak of our search (SDE 17.8); in TARS at 5.3σ against random phases, and in TASOC, ELEANOR-LITE and TGLC; depth map puts it on the target (Δχ² ≥ 57 against catalogued neighbours to T 17.7); 14″ G≈19.7 neighbour untested (NFPP 0.0023, RUWE 1.25): needs imaging |
| [TIC 100796276](checks/TIC100796276/) | [PHT Talk, 2026-10-19](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4158970): 18.15 d, ~3.6 ppt, M dwarf | Independently recovered by KESTREL (single-star run): 18.15207 d, SNR 18, clean (replied on Talk 2026-10-20) |
| [TIC 254296688](checks/TIC254296688/) | [PHT Talk, 2026-10-19](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4159237): 0.64 d, ~90 ppm on an F2V star | Fold is a sinusoid, not a box; periodogram shows gamma Doradus frequency groups: pulsation (checked and replied on Talk 2026-10-20) |
| [TIC 277713012](checks/TIC277713012/) | [PHT Talk, 2026-10-19](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4158825): single ~5.5 h event (S89), possible event (S8) | S89 dip tracks a scattered-light rise in the SAP background; QLP and TARS flat; S8 is post-restart settling (checked and replied on Talk 2026-10-19; accepted by the reporter as a false positive, closed) |
| [TIC 259477022](checks/TIC259477022/) | [PHT Talk, 2026-10-17](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4157680): two ~2300 ppm, ~8 h events (S3, S5), P 60.8 or 30.4 d | Dips in SPOC 2-min PDCSAP only; SAP and TESS-SPOC FFI flat: most likely PDC artefacts (checked and replied on Talk 2026-10-18; accepted by the reporter, closed) |

## Variable stars (VSX)

Folders under [vsx/](vsx/) hold the submitted form data, the plots and light curve
uploaded to VSX, and a PDF of the full report.

| Star | Found | Summary | Status |
|---|---|---|---|
| [TIC 434331752](vsx/TIC434331752/) (ATO J093.6734+17.5725) | 2026-10-10 | Spotted star, P = 1.38477 d, V 13.53–13.57; second period 2.28 d in TESS | Submitted 2026-10-11; under VSX review |
