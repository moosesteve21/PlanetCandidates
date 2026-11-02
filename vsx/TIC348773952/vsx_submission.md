# VSX submission: TIC 348773952 (BD-13 1046)

Prepared 2026-10-14. Saved as a VSX **draft** (the earlier submission, TIC 434331752, is still
awaiting review; VSX takes one at a time). This folder goes to PlanetCandidates `vsx/TIC348773952/`
as the last step before the draft is submitted.

## Form fields

| Field | Entry |
|---|---|
| Novice discovery | unticked (full analysis) |
| Position (J2000.0) | 05 00 38.19 -13 43 08.4 (Gaia DR3, J2000 epoch 2000 as computed by VizieR; then Spot check) |
| Primary name | BD-13 1046 (then Check name) |
| Other names | 2MASS J05003818-1343082 / TYC 5329-1207-1 / GSC 05329-01207 / TIC 348773952 / Gaia DR3 2987862104761137280 (one per line) |
| Standard variable type | EA |
| Spectral type | blank (no spectrum; TIC Teff 4912 K) |
| Maximum magnitude | = 10.47, passband V (APASS DR9; Tycho-2 VT 10.48) |
| Minimum magnitude | 0.151, "Minimum is amplitude" ticked, passband: custom "TESS" (shows as "10.47 V (0.151) TESS", as in approved BMAM-V929) |
| Period | 5.078277 (days) |
| Epoch | 2459990.018 (HJD; the manual asks for no excessive decimals, ±0.0002 d measured) |
| Rise/eclipse duration | 2.1 (%) |
| Supporting file 1 | `tic348773952_vsx_figure.png`; title "TESS light curve"; description below |
| Supporting file 2 | `tic348773952_tess_s32.txt`; title "TESS S32 photometry"; description below |
| Discoverer | Steve Price |
| Reference name / bibcode | TESS / 2014SPIE.9143E..20R (as the VSX FAQ gives). The manual: one reference per save, so save the draft and add 2023A&A...674A..34G (Gaia DR3 SB1 orbit) next |
| Remarks | see below |
| Revision comment | Initial submission. Type, period, epoch and amplitudes from TESS data. Max. from APASS DR9. Gaia DR3 position. |

**Remarks** (facts about the star only, per the VSX moderators' guidance; format copied from
approved entries such as BMAM-V929):

Spectroscopic binary (2023A&A...674A..34G). TESS amplitudes: 0.151 (I) and 0.033 (II); Min II at
phase 0.500. Out-of-eclipse variation 0.02 TESS. B-V= 0.90 (APASS); J-K= 0.59 (2MASS).

**File 1 description:** TESS light curve of BD-13 1046 against time (S32 SPOC 2-min, 2020; S98 QLP,
2025), folded at P = 5.078277 d, and close-ups of both minima from S32.

**File 2 description:** TESS sector 32, SPOC 2-min PDCSAP photometry (2020 Nov-Dec): HJD (UTC),
delta TESS mag from the out-of-eclipse median, error.

## Notes

- Checked against the VSX Manual (2018-11-05 edition, scratch/Manual.pdf) on 2026-10-14: position
  from Gaia via VizieR; V max from a catalogue with the amplitude in another band (allowed when a
  calibrated min and max in one band aren't available); two or three decimals for magnitudes;
  epoch to 3 decimals; eclipse duration = first to last contact of Min I as % of P; a light curve
  against time plus a phase plot (brightest at the top); remarks only on the star's nature, Min II
  and the photometry; revision comment lists the sources. A third file (the PDF report) can be
  added by saving the draft and reopening it.

- Revised 2026-10-14 after the VSX moderator's forum post "New people submitting to VSX: things to
  keep in mind" (forums.aavso.org/t/4856): remarks hold only facts about the star, not how they
  were found (the earlier draft listed the method and the Gaia agreement). The analysis stays in
  the report and supporting files.
- Max: APASS DR9 V = 10.471 ± 0.023 (6 obs); Tycho-2 VT 10.479. Eclipses take 2% of the orbit, so
  catalogue V is effectively maximum light. The depth (0.151 mag) is from SPOC 2-min data,
  corrected for crowding; QLP gives 0.122 mag.
- Epoch is Min I in HJD (UTC): BJD_TDB 2459990.01912 converted at the star's position.
- ASAS-SN V (AP19370517, 2013-2018): primary eclipse seen at the TESS ephemeris (~3.6σ, 7 points
  0.13 mag fainter); median V 10.50 out of eclipse. Too sparse for a V depth, so the form keeps the TESS
  amplitude. Goes in the report (not the remarks).
