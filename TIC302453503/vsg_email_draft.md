# Email to the Visual Survey Group (draft, not sent)

Prepared 2026-10-12. Bracketed parts are to be filled in before sending.

---


**Subject:** Independent TESS transit search: a 3.63-day, ~1.2 R⊕ candidate on L 642-3 (TIC 302453503)

Dear [name],

I'm an amateur astronomer running my own search of TESS light curves, and I'm
writing because the Visual Survey Group's work with independent searchers seems
the right home for what it's finding. ExoFOP now accepts community candidates
only once they are published, which I'm not in a position to do on my own.

My search runs a BLS search over TESS light curves (SPOC, TESS-SPOC and QLP)
of bright, low-contamination M and K dwarfs, ranked by how small a planet each
star allows. Every signal goes through automated vetting:

- odd/even and secondary-eclipse tests;
- duration against the star's limit;
- per-sector depth and timing;
- uniqueness tests (model-shift and an unrelated-period margin);
- catalogue cross-matches for known variables nearby;
- difference-image and centroid checks;
- a comparison across independent reductions.

I calibrated it on known planets and injected transits. So far it has searched
about 820 stars (about 1,300 once the current batch finishes; update before
sending), and this is the first candidate that
has passed everything I can check:

**TIC 302453503 (L 642-3)**, M1.5 dwarf, T = 10.35

- Period: 3.629156 ± 0.000005 d
- Epoch: BJD_TDB 2460158.84281 ± 0.00158
- Depth: ~440 ppm (Rp/R* 0.0209)
- Duration: ~1.6 h
- Rp ≈ 1.16 (+0.14/−0.08) R⊕; SNR ≈ 10; 29 transits in sectors 1, 28, 68, 92 and 95

**Evidence so far:**

- The dip is present in all five independent reductions.
- 25 of 26 transits dip, and odd and even transits agree.
- There is no secondary eclipse, and the duration fits a near-central transit
  of this star.
- The in-transit centroid shift is consistent with zero, which excludes the
  two brightest neighbours (68″ and 73″) at more than 11σ.
- Pipelines my search never used also show it: TARS gives 559 ± 91 ppm over
  28 transits, with the dip present in every sector.
- A physical transit fit gives a stellar density of 5.0 (+3.9/−4.2) g/cm³,
  consistent with the catalogued star (5.5).
- TRICERATOPS gives FPP = 0.055 and NFPP = 0.0003 (no contrast curve): a likely
  planet, held back from validation by the unresolved-companion scenarios.
- It isn't a TOI, a CTOI or a SPOC TCE.
- An unresolved companion within a few arcseconds isn't excluded, and
  high-resolution imaging would address it.

Would the group be willing to look at it, and, if it holds up, take it forward?
I'd also be glad to share future candidates and the details of how they were
vetted, if that would be useful. The code and the full vetting notes are
[available on request / at <repository URL>].

Thank you for your time.

Best regards,
[Your name]
[Contact details]

