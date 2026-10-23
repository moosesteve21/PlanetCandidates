# PlanetCandidates

Discoveries from an independent search of TESS light curves, as submitted: transit
candidates posted for the community, and variable stars submitted to the AAVSO
International Variable Star Index (VSX). Each object has its own folder. Its README
records when and how it was found, its parameters, the vetting or analysis, and what
has been submitted where.

Only material that has been submitted, or is drafted for submission, is kept here.

[discovery_log.md](discovery_log.md) holds dated fingerprints (SHA-256 hashes) of candidates
found but not yet made public, so the date each was found can be checked later.

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
