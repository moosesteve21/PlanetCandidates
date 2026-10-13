# Email to the Visual Survey Group (draft, not sent)

Prepared 2026-10-13, covering all three posted or drafted candidates; it replaces the
earlier single-candidate draft for TIC 302453503. To: Martti H. K. Kristiansen (VSG),
with the group's alternative contact in copy. Send once TIC 147226218 is posted, with
its thread link filled in.

---

**Subject:** Independent TESS transit search: three small-planet candidates on bright K and M dwarfs

Dear Martti Kristiansen,

I'm an amateur astronomer running my own search of TESS light curves, and I'm writing
because the Visual Survey Group's work with independent searchers seems the right home
for what it's finding. ExoFOP now accepts community candidates only once they are
published, which I'm not in a position to do on my own.

The search covers bright (T 8–11), low-contamination K and M dwarfs that TESS has
observed in only 1–6 sectors, ranked by how small a planet each star allows. It uses a
BLS search over SPOC, TESS-SPOC and QLP light curves. Every signal then goes through
automated vetting:
- odd/even and secondary-eclipse tests, duration against the star's limit, and
  per-sector depth and timing;
- uniqueness tests (model-shift, and a margin over unrelated periods);
- catalogue cross-matches for known variables nearby;
- pixel-level position checks and a comparison across independent reductions;
- for survivors, a physical transit fit (batman + emcee) with a stellar-density check,
  and TRICERATOPS.

It recovers the ten known planets I use as controls, and injection tests give 50%
completeness at an expected SNR of 12.4. So far it has searched about 4,600 stars.
These three candidates have passed everything I can check. None is a TOI, a CTOI or a
SPOC TCE.

**1. TIC 240488148 (TYC 3191-503-1)**, K dwarf, T = 10.17
- P = 1.5125120 ± 0.0000040 d; T0 = BJD_TDB 2458712.9421 ± 0.0040
- Depth ~390 ppm, duration 1.40 h; Rp ≈ 1.45 (+0.18/−0.08) R⊕
- 60 transits in six sectors (15, 16, 56, 76, 82, 83), the same depth in every sector
- Confirmed by TARS: 405 ± 44 ppm (9.2σ)
- Stellar density 3.3 g/cm³ against 3.2 catalogued
- On target by a per-pixel depth map (no 2-min data): neighbours worse by Δχ² ≥ 19.5
- FPP 0.11, NFPP 0.018
- https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4154549

**2. TIC 302453503 (L 642-3)**, M1.5 dwarf, T = 10.35
- P = 3.629156 ± 0.000005 d; T0 = BJD_TDB 2460158.84281 ± 0.00158
- Depth ~440 ppm, duration ~1.6 h; Rp ≈ 1.16 (+0.14/−0.08) R⊕
- 29 transits (sectors 1, 28, 68, 92, 95)
- Confirmed by TARS: 559 ± 91 ppm, present in every sector
- Density consistent (5.0 against 5.5 g/cm³)
- SPOC 2-min centroids exclude the brightest neighbours at more than 11σ
- FPP 0.055, NFPP 0.0003
- https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/talk/2110/4153490

**3. TIC 147226218 (CD−43 9842)**, early K dwarf at 77 pc, T = 10.29
- P = 3.871562 ± 0.000010 d; T0 = BJD_TDB 2459336.6807 ± 0.0031
- Depth ~530 ppm, duration 2.45 h; Rp ≈ 1.69 (+0.18/−0.09) R⊕
- About 20 transits in four sectors (38, 65, 102, 103)
- Confirmed by TARS: 505 ± 85 ppm (5.9σ)
- Density consistent (1.7σ)
- On target by a per-pixel depth map: neighbours worse by Δχ² ≥ 27.8
- FPP 0.16, NFPP 0.077
- [Talk thread link]

For all three, the remaining false-positive scenarios are mostly unresolved companions,
which high-resolution imaging would address. The individual transits are weak, so the
detections rest on the stacked data.

Plots, per-sector folds, pixel maps and discovery records for each candidate are at
https://github.com/moosesteve21/PlanetCandidates. The search code is public at
https://github.com/moosesteve21/PlanetFinder, and the full vetting notes are available on request.

Would the group be willing to look at them and, if they hold up, take them forward? I'd
also be glad to send future candidates, if that would be useful.

Thank you for your time.

Best regards,
Steve Price
(Zooniverse: moosehunter21; ORCID: https://orcid.org/0009-0004-6010-3869)
