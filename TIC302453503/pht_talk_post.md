# Planet Hunters TESS Talk post (as published)

Posted 2026-10-12 12:13 UTC by moosehunter21 on the "Planets!" board:
https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4153490

The text below is the published post, unedited. One correction: "pi Men b" in the
pipeline paragraph should read "pi Men c" (the transiting planet).

---

**Title:** TIC 302453503 (L 642-3): 3.63-day, ~1.2 R⊕ candidate on an M dwarf, not a TOI or TCE

@researchers #possible-transits

Hi all. I run my own search of TESS light curves: a BLS search of bright,
low-contamination M and K dwarfs, with automated vetting. This is the strongest
signal it has found. It isn't a TOI, a CTOI or a SPOC TCE (no data-validation
report on MAST). I'd be grateful for your opinions, and for advice on taking it
further if it holds up.

**The star**
- TIC 302453503 = L 642-3, Gaia DR3 6815237513835256064, RA 322.56736, Dec −24.88804
- M1.5 dwarf, T = 10.35; TIC R* = 0.507 ± 0.015 R☉, M* = 0.505 M☉, Teff 3621 K
- Contamination ratio 0.0025; Gaia RUWE 1.14

**The signal** (29 transits: SPOC 2-min S1, S28; TESS-SPOC S68; QLP S92, S95)
- Period 3.629155 ± 0.000006 d; mid-transit BTJD 3158.8431 ± 0.0025 (BJD 2460158.8431)
- Depth ~440 ppm; Rp/R* 0.0209 (+0.0025/−0.0014); Rp ≈ 1.16 (+0.14/−0.08) R⊕
- Duration ~1.6 h; SNR ≈ 10

**Checks**
- Independent pipelines: the dip is in all five reductions my search uses
  (SPOC PDCSAP and SAP, TESS-SPOC PDCSAP and SAP, QLP). Pipelines it never used
  also show it: **TARS 559 ± 91 ppm over 28 transits, with the dip present in each
  of the five sectors**. GSFC-ELEANOR-LITE (S1 only) gives 699 ± 156 ppm,
  TASOC (S1) 312 ± 94 ppm, and TGLC (S1, noisier) 1355 ± 338 ppm.
- Consistency: 25 of 26 transits dip in the search's light curve; SNR 7 remains
  after removing the strongest ones. Odd and even transits agree; no secondary
  eclipse. The period stands well clear in the periodogram (SDE 13.7, 5.1 above
  the best unrelated period), and the model-shift test passes.
- Stellar density: a batman + emcee fit (circular, quadratic limb darkening with
  priors) gives ρ* = 5.0 (+3.9/−4.2) g/cm³ against 5.5 g/cm³ for the
  catalogued star (0.1σ). b = 0.57 ± 0.36, a/R* ≈ 15.
- On target: the in-transit centroid shift from SPOC 2-min data (16 transits) is
  +1.6 ± 2.8 / −1.6 ± 3.6 mas, consistent with zero. The two brightest
  neighbours (T 14.3 at 68″, T 15.1 at 73″) would shift it by 25–40 mas and are
  excluded at more than 11σ.
- TRICERATOPS: apertures for S1, S28 and S68, folded light curve, 10⁶ draws, no
  contrast curve. **FPP = 0.055, NFPP = 0.0003.** A 10⁵-draw run gave FPP 0.041.
  Transiting planet on the target 83%; a planet around an unresolved bound
  companion 12%; a planet on the target with an unresolved companion diluting the
  dip 5%. Nearby eclipsing binaries total below 0.1%.

**Limitations**
- Individual transits are weak (2–4σ each); the detection rests on the stack.
- No high-resolution imaging, so close companions aren't excluded. Those
  scenarios are what keeps the FPP above the validation threshold.
- About 440 ppm is too shallow for my own equipment and for ATLAS/ZTF-type
  surveys.

**About the pipeline:** it's home-made and unpublished (written with AI
assistance). It recovers the 10 known planets I use as controls (pi Men c,
LHS 3844 b, TOI-700 b–e, TOI-270 b–d, WASP-18 b). Injection-recovery tests on
these bright stars give 50% completeness at an expected SNR of 12.4 and 90% at
18.5. It has also turned up several eclipsing binaries and variables confirmed
in ZTF, ATLAS and ASAS-SN, one of which is now with VSX.

Folded light curve, with odd and even transits compared:

![TIC 302453503 folded light curve and odd/even transits](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC302453503/tic302453503_folded_odd_even.png)

Each transit with the fitted model:

![TIC 302453503 individual transits](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC302453503/tic302453503_individual_transits.png)

I'm happy to share the fit chains and scripts.

[Steve Price / moosehunter21]

