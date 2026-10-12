# Planet Hunters TESS Talk post (draft, not posted)

Prepared 2026-10-12; held back until the TIC 302453503 thread has had replies.

---


**Title:** TIC 143400975 (StKM 1-845): 4.88-day, near-grazing ~2 R⊕ candidate on a K7 dwarf, not a TOI or TCE

@researchers #possible-transits

Hi all. A second signal from my own BLS search of bright, low-contamination
dwarfs (the first was TIC 302453503 in this board). It isn't a TOI, a CTOI or a
SPOC TCE (no data-validation report on MAST). The transit is short for the star,
which I think means a near-grazing orbit; I'd value your view on that.

**The star**
- TIC 143400975 = StKM 1-845, Gaia DR3 3830446413771545728, RA 154.84638, Dec −1.33093
- K7 dwarf, T = 10.13; TIC R* = 0.627 ± 0.019 R☉, M* = 0.610 M☉, Teff 3963 K
- Contamination ratio 0.0002; Gaia RUWE 1.16

**The signal** (21 transits: SPOC 2-min S35, S45, S46; TESS-SPOC S8, S72; QLP S89)
- Period 4.87876 ± 0.00001 d; mid-transit BTJD 1521.7362 ± 0.0029
- Depth 640 ± 79 ppm; duration 0.85 ± 0.11 h (a central transit would last 2.33 h)
- Best fit: a near-grazing transit, b ≈ 0.96, Rp/R* ≈ 0.030, so Rp ≈ 2 R⊕
  (poorly constrained when grazing); SNR ≈ 9

**Checks**
- Independent pipelines: the dip is in all five reductions my search uses
  (SPOC PDCSAP and SAP, TESS-SPOC PDCSAP and SAP, QLP). **TARS, which my search
  never used, gives 628 ± 121 ppm over 22 transits, with the dip present in each of
  its five sectors.**
- Consistency: 20 of 21 transits dip; SNR 6.2 remains after removing the
  strongest ones. Odd and even transits agree (0.9σ); no secondary eclipse
  (−7 ± 58 ppm). The period is unambiguous: SDE 20.2, 10.6 above the best
  unrelated period. The model-shift test passes.
- Density and duration: a free-density fit (batman) gives ρ* = 3.1 g/cm³ with
  b = 0.96. Fixing ρ* at the catalogued star's 3.5 g/cm³ costs Δχ² = 0.1. So the
  short dip fits a grazing transit of the target itself. (An MCMC posterior
  spreads along the b–ρ* degeneracy, so its median density is much higher; the
  likelihood peaks at the catalogued value.)
- On target: the in-transit centroid shift from SPOC 2-min data is −5.5 ± 3.5 /
  −0.6 ± 4.4 mas, consistent with zero. The only neighbour bright enough to
  matter (TIC 143400977, T 13.9 at 93″, needing a 25% eclipse) would shift it by
  about 51 mas and is excluded at 16σ.
- TRICERATOPS: apertures for S35, S45, S46 and S72, folded light curve, 10⁶ draws,
  no contrast curve. **FPP = 0.39, NFPP = 0.000.** Transiting planet on the
  target 50%; the same with an unresolved companion diluting the dip 34%; a
  planet around an unresolved bound companion 10%; eclipsing binaries at twice
  the period about 5%.

**Limitations**
- Grazing geometry: the radius is uncertain, and V-shaped dips resemble
  eclipsing binaries, which is why the FPP is much higher than for TIC 302453503.
- No high-resolution imaging; close companions aren't excluded.
- Individual transits are weak; the detection rests on the stack. The pixel-level
  check can't localise a dip this shallow sector by sector.

**About the pipeline:** it's home-made and unpublished (written with AI
assistance). It recovers the 10 known planets I use as controls (pi Men c,
LHS 3844 b, TOI-700 b–e, TOI-270 b–d, WASP-18 b). Injection-recovery tests on
bright stars give 50% completeness at an expected SNR of 12.4 and 90% at 18.5.

Folded light curve, with odd and even transits compared:

![TIC 143400975 folded light curve and odd/even transits](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC143400975/tic143400975_folded_odd_even.png)

Each transit with the fitted model:

![TIC 143400975 individual transits](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC143400975/tic143400975_individual_transits.png)

Steve Price / moosehunter21
