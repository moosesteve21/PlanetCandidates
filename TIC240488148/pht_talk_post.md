# Planet Hunters TESS Talk post (as published)

Posted 2026-10-13 15:51 UTC by moosehunter21 on the "Planets!" board:
https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4154549

The text below is the post as prepared for publishing.

---

**Title:** TIC 240488148 (TYC 3191-503-1): 1.51-day, ~1.4 R⊕ candidate on a K dwarf, not a TOI or TCE

@researchers #possible-transits

Hi all. This is the second candidate from my own search of TESS light curves (the first
was L 642-3: https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4153490).
It's the strongest signal the search has found so far. It isn't a TOI, a CTOI or a SPOC
TCE (the star has no 2-min data). I'd be grateful for your opinions.

**The star**
- TIC 240488148 = TYC 3191-503-1, Gaia DR3 1967568881023980032, RA 323.62829, Dec +42.64403
- K dwarf, T = 10.17, G = 10.88; TIC R* = 0.67 R☉, M* = 0.69 M☉, Teff 4403 K
- Contamination ratio 0.09; Gaia RUWE 1.04, no sign of binarity in Gaia (RV scatter normal)

**The signal** (60 transits: TESS-SPOC FFI S15, S16 at 30 min; S56, S76, S82, S83 at 200 s)
- Period 1.5125120 ± 0.0000040 d; mid-transit BTJD 1712.9421 ± 0.0040 (BJD 2458712.9421)
- Depth ~390 ppm; Rp/R* 0.0198 (+0.0024/−0.0011); Rp ≈ 1.45 (+0.18/−0.08) R⊕
- Duration 1.40 ± 0.09 h; SNR ≈ 15

**Checks**
- **Every sector shows it:** the folded depth per sector is 356, 373, 422, 394, 433 and
  347 ppm (±48–72), and 52 of 54 transits dip in the search's light curve. SNR 10
  remains after removing the strongest transits. (Figure 1.)
- **Independent pipeline:** TARS, which my search never used, gives **405 ± 44 ppm over
  71 transits (9.2σ)**. In my own reduction check the QLP and TESS-SPOC SAP fluxes agree
  (393–408 ppm).
- **Shape and period:** odd and even transits agree (0.5σ); no secondary eclipse
  (7 ± 30 ppm). The period stands well clear in the periodogram (SDE 57, 43 above the
  best unrelated period), and the model-shift test passes.
- **Stellar density:** a batman + emcee fit (circular, quadratic limb darkening with
  priors) gives ρ* = 3.3 (+1.9/−2.6) g/cm³ against 3.2 g/cm³ for the catalogued star
  (0.0σ). b = 0.51 (+0.35/−0.38), a/R* ≈ 7.4.
- **On target:** with no 2-min data there are no SPOC centroids, so I mapped the
  in-transit flux deficit pixel by pixel in TESScut cutouts of all six sectors (12–18
  transits each). I then compared star-image models centred on each of the 31 stars
  within 2.5′. The target fits best. The nearest alternatives, TIC 240488110 (T 13.5,
  48″) and the two stars at 30″ (T 13.7, T 15.3), are worse by Δχ² = 19.5–26
  (roughly 4.4–5σ). (Figure 2.)
- **TRICERATOPS:** apertures for all six sectors, folded light curve, 10⁶ draws, no
  contrast curve. **FPP = 0.11, NFPP = 0.018.** Transiting planet on the target 73%; a
  planet around an unresolved bound companion 14%; a planet on the target diluted by an
  unresolved companion 9%; a diluted EB 2%. Nearby-star scenarios total about 1.7%.

**Limitations**
- Individual transits are weak (about 2σ each); the detection rests on the stack.
- The pixel test uses a Gaussian approximation to the TESS PSF, not the full PRF.
- No high-resolution imaging or spectroscopy, so close companions aren't excluded;
  those scenarios keep the FPP above the validation threshold.

**About the pipeline:** it's home-made and unpublished (written with AI assistance). It
recovers the 10 known planets I use as controls (pi Men c, LHS 3844 b, TOI-700 b–e,
TOI-270 b–d, WASP-18 b). Injection-recovery tests give 50% completeness at an expected
SNR of 12.4 and 90% at 18.5.

Figure 1: the transit folded separately in each sector (15-minute bins; red: the fitted
depth and duration):

![TIC 240488148 folded per sector](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC240488148/tic240488148_sector_folds.png)

Figure 2: the in-transit flux deficit per pixel in each sector (top: the images; bottom:
the deficit; gold star: the target):

![TIC 240488148 per-pixel transit depth](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC240488148/tic240488148_pixel_depth_map.png)

The search's own plot (periodogram, fold, odd/even):

![TIC 240488148 search plot](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC240488148/tic240488148_folded_odd_even.png)

I'm happy to share the fit chains and scripts.

[Steve Price / moosehunter21]
