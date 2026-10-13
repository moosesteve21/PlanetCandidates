# Planet Hunters TESS Talk post (draft)

For the "Planets!" board. Not yet posted. The image links work once the repo is pushed.

---

**Title:** TIC 147226218 (CD−43 9842): 3.87-day, ~1.7 R⊕ candidate on a K dwarf, not a TOI or TCE

@researchers #possible-transits

Hi all. Another candidate from my own search of TESS light curves. My earlier posts are
on L 642-3 (https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4153490)
and TIC 240488148 (https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4154549).
It isn't a TOI, a CTOI or a SPOC TCE (the star has no 2-min data). I'd be grateful for
your opinions.

**The star**
- TIC 147226218 = CD−43 9842, Gaia DR3 6000611238623937152, RA 230.61974, Dec −43.86789
- Early K dwarf at 77 pc (parallax 12.9 mas), T = 10.29, V = 11.17, Gaia BP−RP 1.17
- TIC R* = 0.67 ± 0.04 R☉, M* = 0.79 M☉, Teff 4843 ± 123 K (SIMBAD's older "G5" type
  doesn't fit the Gaia colour)
- Contamination ratio 0.095; Gaia RUWE 1.12, no sign of binarity in Gaia

**The signal** (19–20 transits: TESS-SPOC FFI S38 at 10 min, S65 at 200 s; QLP S102, S103 at 200 s)
- Period 3.871562 ± 0.000010 d; mid-transit BTJD 2336.6807 ± 0.0031 (BJD 2459336.6807)
- Depth ~530 ppm; Rp/R* 0.0231 (+0.0024/−0.0013); Rp ≈ 1.69 (+0.18/−0.09) R⊕
- Duration 2.45 ± 0.17 h; SNR ≈ 14

**Checks**
- **Every sector shows it:** the folded depth per sector is 646, 548, 595 and 463 ppm
  (±77–86), and 18 of 18 transits dip in the search's light curve. SNR 10 remains after
  removing the strongest transits. (Figure 1.)
- **Independent pipeline:** TARS, which my search never used, gives **505 ± 85 ppm over
  12 transits (5.9σ)**. QLP's SAP and detrended fluxes agree (414–651 ppm).
- **Shape and period:** odd and even transits agree (1.4σ); no secondary eclipse
  (−12 ± 42 ppm). The period stands well clear in the periodogram (SDE 34, 24 above the
  best unrelated period), and the model-shift test passes.
- **Stellar density:** a batman + emcee fit (circular, quadratic limb darkening with
  priors) gives ρ* = 1.6 (+0.8/−1.3) g/cm³ against 3.7 g/cm³ for the catalogued star
  (consistent, 1.7σ). b = 0.50 (+0.35/−0.33), a/R* ≈ 11.
- **On target:** with no 2-min data there are no SPOC centroids, so I mapped the in-transit
  flux deficit pixel by pixel in TESScut cutouts of all four sectors (5–7 transits each).
  I then compared star-image models centred on each of the 38 stars within 2.5′. The
  target fits best in every sector. The nearest alternatives, TIC 147219144 (T 14.8, 16″)
  and TIC 147226219 (T 14.4, 31″), are worse by Δχ² = 27.8 and 35.2 (roughly 5σ).
  (Figure 2; the S102 and S103 maps are noisier than S38 and S65.)
- **TRICERATOPS:** apertures for S38 and S65, folded light curve, 10⁶ draws, no contrast
  curve. **FPP = 0.16, NFPP = 0.077.** Transiting planet on the target 63%; a planet
  around an unresolved bound companion 17%; a planet on the target diluted by an
  unresolved companion 7%; a diluted EB 4%. Nearby EBs total about 4%, though the pixel
  map argues against those.

**Limitations**
- Individual transits are weak (about 3σ each); the detection rests on the stack.
- Fewer transits than I'd like (about 20, in four sectors), and the pixel test uses a
  Gaussian approximation to the TESS PSF, not the full PRF.
- No high-resolution imaging or spectroscopy, so close companions aren't excluded; those
  scenarios keep the FPP above the validation threshold.

**About the pipeline:** it's home-made and unpublished (written with AI assistance). It
recovers the 10 known planets I use as controls (pi Men c, LHS 3844 b, TOI-700 b–e,
TOI-270 b–d, WASP-18 b). Injection-recovery tests give 50% completeness at an expected
SNR of 12.4 and 90% at 18.5.

Figure 1: the transit folded separately in each sector (15-minute bins; red: the fitted
depth and duration):

![TIC 147226218 folded per sector](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC147226218/tic147226218_sector_folds.png)

Figure 2: the in-transit flux deficit per pixel in each sector (top: the images; bottom:
the deficit; gold star: the target):

![TIC 147226218 per-pixel transit depth](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC147226218/tic147226218_pixel_depth_map.png)

The search's own plot (periodogram, fold, odd/even):

![TIC 147226218 search plot](https://raw.githubusercontent.com/moosesteve21/PlanetCandidates/main/TIC147226218/tic147226218_folded_odd_even.png)

I'm happy to share the fit chains and scripts.

[Steve Price / moosehunter21]
