# TIC 88481081: check of a community report

**Report:** [Planet Hunters TESS Talk, 2026-11-19](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4185529)
(DAAN11): P ~1.730 d, depth ~0.4–0.5%, ~1.5 h, in S108 2-min data; possible hot Jupiter around an F star (T = 10.1).

**Checked 2026-11-19.** Data: SPOC 2-min PDCSAP for S105–S108 (S105–S107 were not in the report), plus TESScut for the depth map.

| Check | Result |
|---|---|
| Ephemeris (BLS, S105–S108) | P = 1.730376 d, T0 = 4314.3121 BTJD, T14 ~2.15 h; 44 transits measured |
| SPOC | TCEs in S105, S106 and S107 (1.7302–1.7304 d, 5,000–5,400 ppm, R ~15 R⊕); no TOI or CTOI |
| Odd vs even (local linear baseline per transit) | odd 4,351 ± 53 ppm, even 4,943 ± 74 ppm: **6.5σ** different, and even is deeper in S106, S107 and S108 separately (`per_transit.txt`) |
| Phase 0.5 at P | flat (−52 ± 28 ppm) |
| Depth map (each star's predicted image fitted to the in-transit deficit, `depth_map.png`) | best source **TIC 88481083** (T = 12.72, 20.7″ away); the target is worse by Δχ² = 1,507, and each of S105–S108 prefers the neighbour on its own (S97 FFIs too noisy to tell) |
| TIC 88481083 | Gaia DR3 5073603089619768704: same parallax (4.165 vs 4.197 mas) and proper motion as the target, so a bound companion ~5,000 au out. Gaia classes it **RS CVn** (VSX: RS, no period); Gaia RV error 5.8 km/s (target 0.35) |
| Depth needed on the neighbour | it gives ~8% of the combined T-band light, so the 4,350/4,940 ppm dips are ~5.3% and ~6.0% eclipses on it |

**Conclusion:** not a planet on the target. The odd/even difference makes the true period 2P = **3.46075 d**, with two
unequal eclipses, and the depth map puts the eclipses on the co-moving K-type companion TIC 88481083. That star is
already known to be variable (RS CVn class). The most likely explanation is an eclipsing binary in the companion,
so the system would be a hierarchical triple. The eclipse period isn't in VSX yet.

Files: `oddeven.png` (per-transit depths, and the odd and even folds), `depth_map.png`, `per_transit.txt`, and the scripts
(`lc_check.py`, `per_transit.py`, `oddeven_fig.py`; the depth map is KESTREL's `investigations/depth_map.py`).
