# Variable stars from the KESTREL search (research-note material)

Online material for a research note in preparation for the Research Notes of the AAS (RNAAS), *Five New Eclipsing
Binaries and Revised Periods for 34 Catalogued Variables from the KESTREL TESS Transit Search* (Steve Price,
ORCID [0009-0004-6010-3869](https://orcid.org/0009-0004-6010-3869)). **Status: draft, not yet submitted.**

The KESTREL transit search of about 17,900 TESS K and M dwarfs finds many variable stars, which it rejects as
planet candidates. These are the ones missing from the AAVSO International Variable Star Index (VSX), or listed
there without the TESS period, that survived the checks below.

## How they were checked

- **Which star?** A pixel-level depth map for every star: in each sector, the flux lost during the dips in a
  TESScut cutout is fitted with the image each catalogued star nearby would produce. Many shallow eclipses on the
  search targets turned out to be deep eclipses on fainter neighbours; those stars are listed under the neighbour,
  with the target's depth map.
- **Eclipsing binaries:** measured on the source's own light curve (up to eight sectors, eclipses masked in the
  flattening). Min I is the deeper eclipse; depths are medians of the central 20% of each eclipse; the period and
  epoch come from a weighted line through the per-sector Min I times. Two faint neighbours with no pipeline light
  curve were measured in TESScut apertures; only their periods and phases are given.
- **Rotation periods:** Lomb–Scargle periodograms of the unflattened light curve of each sector and of all sectors
  together, with folds at the peak, twice the peak, the VSX period and the search period, inspected by eye. The
  period given is the median of the per-sector periods, with their scatter as the uncertainty.
- **Rejected:** folds in which the variation outside the "eclipses" is as large as the eclipses (spotted or
  pulsating stars folded at a multiple of their period), stars without a consistent period, and stars whose VSX
  period TESS confirms.

Depths and amplitudes are in TESS magnitudes, in the light curve used, and are not corrected for light from other
stars. Numbers in parentheses are uncertainties in the last digits. "n d⁻¹ alias": the VSX period is an n-cycles-
per-day alias of the TESS period. "not seen in TESS": the VSX period has no counterpart in the TESS data.

The full table, with coordinates, Gaia DR3 IDs and G magnitudes, is [eb_note_table.csv](eb_note_table.csv).
Each star's folder holds the fold (`fold.png`, `fold.json`) or periodogram and folds (`period.png`, `period.json`),
and the depth map (`depth_map.png`, `depth_map.txt`).

### New eclipsing binaries (5)

| Star | P (d) | Min I (BJD_TDB) | Min I / Min II (mag) | Phase Min II | Type | VSX entry now | Files |
|---|---|---|---|---|---|---|---|
| TIC 150693986 | 2.9099671(18) | 2460205.59505(22) | 0.0348 / 0.0058 | 0.500 | EA | none | [TIC150693986](TIC150693986/) |
| TIC 342671380 | 64.39157(10) | 2460736.638(12) | 0.336 / 0.195 | 0.317 | EA | none | [TIC342671380](TIC342671380/) |
| TIC 97456896 | 2.8823489(14) | 2459968.19173(40) | 0.154 / 0.0728 | 0.499 | EA | none | [TIC97456896](TIC97456896/) |
| TIC 100778380 | 0.91732230(39) | 2459861.61926(44) | 0.139 / 0.0419 | 0.500 | EA | none | [TIC100778380](TIC100778380/) |
| TIC 240121931 | 5.1903122(45) | 2459569.40293(39) | – | 0.496 | EA | none | [TIC240121931](TIC240121931/) |

### Eclipses in an unresolved system (source not identified) (1)

| Star | P (d) | Min I (BJD_TDB) | Min I / Min II (mag) | Phase Min II | Type | VSX entry now | Files |
|---|---|---|---|---|---|---|---|
| TIC 287318353 | 0.16667160(48) | 2459746.2966(15) | 0.0035 / 0.0035 | 0.500 | E: | none | [TIC287318353](TIC287318353/) |

### Eclipsing binaries in VSX without this period or type (7)

| Star | P (d) | Min I (BJD_TDB) | Min I / Min II (mag) | Phase Min II | Type | VSX entry now | Files |
|---|---|---|---|---|---|---|---|
| TIC 165725811 | 10.470734(26) | 2460502.1717(15) | 0.241 / 0.0427 | 0.452 | EA | Gaia DR3 6161606438426049920: RS, no period | [TIC165725811](TIC165725811/) |
| TIC 184940024 | 0.42798210(43) | 2460321.58038(26) | – | 0.498 | EW: | Gaia DR3 2085849050543848832: S, no period | [TIC184940024](TIC184940024/) |
| TIC 415559924 | 3.0358417(25) | 2459535.86207(50) | 0.643 / 0.642 | 0.500 | EA | NSVS 9731467: EB, 1.517740 d (half) | [TIC415559924](TIC415559924/) |
| TIC 247165505 | 1.2640052(42) | 2459605.7623(20) | 0.302 / 0.147 | 0.500 | EA | Gaia DR3 3165429861096208512: RS, no period | [TIC247165505](TIC247165505/) |
| TIC 294191640 | 1.59391120(28) | 2459713.27135(17) | 0.0319 / 0.0055 | 0.501 | EA | Gaia DR3 5366582187778186112: VAR, no period | [TIC294191640](TIC294191640/) |
| TIC 415641176 | 1.65629160(83) | 2459826.93890(18) | 0.0841 / 0.0102 | 0.502 | EA | ASAS J073126+2605.7: ROT, 0.7134 d; rotation 1.652 d | [TIC415641176](TIC415641176/) |
| TIC 207012283 | 5.8725449(70) | 2458715.09081(58) | 0.0382 / 0.016 | 0.498 | EA | Gaia DR3 3331189592697496320: RS, no period; EB in Kostov et al. (2025), 5.872547 d | [TIC207012283](TIC207012283/) |

### Rotation periods for variables in VSX without a TESS-confirmed period (27)

| Star | P (d) | Amplitude by sector (TESS mag) | VSX entry now | Files |
|---|---|---|---|---|
| TIC 20168032 | 0.41773(44) | 0.049–0.115 | ASAS J054102+2036.3: ROT, 0.72 d (1 d⁻¹ alias) | [TIC20168032](TIC20168032/) |
| TIC 206492505 | 0.46144(20) | 0.047–0.092 | ASAS J035428-4930.6: ROT, 0.3155 d (1 d⁻¹ alias) | [TIC206492505](TIC206492505/) |
| TIC 238553527 | 0.46847(29) | 0.038–0.094 | V0391 Gem: BY, 0.3188 d (1 d⁻¹ alias) | [TIC238553527](TIC238553527/) |
| TIC 440852527 | 0.23034(30) | 0.033–0.133 | ASAS J071811+1735.2: ROT, 0.1872 d (1 d⁻¹ alias); or EW at 2P | [TIC440852527](TIC440852527/) |
| TIC 282504081 | 0.9155(37) | 0.021–0.076 | ASAS J060013+0046.9: VAR, 10.95475 d (1 d⁻¹ alias) | [TIC282504081](TIC282504081/) |
| TIC 117121960 | 0.951(14) | 0.035–0.105 | KU Cnc: RS, 20.82 d (1 d⁻¹ alias) | [TIC117121960](TIC117121960/) |
| TIC 88478727 | 1.0569(16) | 0.032–0.053 | GJ 1054A: BY, 0.513 d (1 d⁻¹ alias) | [TIC88478727](TIC88478727/) |
| TIC 106344480 | 1.3274(30) | 0.014–0.058 | ASAS J071844-2616.1: ROT, 0.5702 d (1 d⁻¹ alias) | [TIC106344480](TIC106344480/) |
| TIC 446089922 | 1.4299(24) | 0.035–0.126 | ASAS J045556+4606.2: ROT, 0.58873 d (1 d⁻¹ alias) | [TIC446089922](TIC446089922/) |
| TIC 302965929 | 3.0872(86) | 0.039–0.154 | ASAS J040830-7844.6: ROT, 0.42962 d (2 d⁻¹ alias) | [TIC302965929](TIC302965929/) |
| TIC 247117382 | 0.54935(93) | 0.017–0.096 | ASAS J073122+1556.0: DSCT, 0.20712 d (3 d⁻¹ alias) | [TIC247117382](TIC247117382/) |
| TIC 156805574 | 0.77466(42) | 0.050–0.061 | ASASSN-V J092101.39+365038.4: ROT, 0.99781 d (not seen in TESS) | [TIC156805574](TIC156805574/) |
| TIC 97398789 | 1.1339(18) | 0.057–0.091 | ASAS J020959+1404.8: MISC, 8.47277 d (not seen in TESS) | [TIC97398789](TIC97398789/) |
| TIC 92877752 | 1.3805(44) | 0.028–0.070 | ASAS J211155-3258.5: ROT, 3.62 d (not seen in TESS) | [TIC92877752](TIC92877752/) |
| TIC 450087679 | 1.4177(54) | 0.061–0.108 | ASAS J044800+0737.8: ROT, 0.771 d (not seen in TESS) | [TIC450087679](TIC450087679/) |
| TIC 314604460 | 1.4417(47) | 0.018–0.074 | ASASSN-V J184609.39+191214.0: ROT, 0.99665 d (not seen in TESS) | [TIC314604460](TIC314604460/) |
| TIC 231292500 | 2.440(25) | 0.024–0.064 | ASASSN-V J025735.32-504813.1: ROT, 1.0005 d (not seen in TESS) | [TIC231292500](TIC231292500/) |
| TIC 92997988 | 3.881(51) | 0.006–0.099 | ASASSN-V J113721.93-480128.1: ROT, 1.3366 d (not seen in TESS) | [TIC92997988](TIC92997988/) |
| TIC 286278040 | 0.7128(10) | 0.078–0.138 | Gaia DR3 3760430720201431936: RS, no period | [TIC286278040](TIC286278040/) |
| TIC 220401419 | 4.602(57) | 0.055–0.099 | Gaia DR3 4678041618178220672: RS, no period | [TIC220401419](TIC220401419/) |
| TIC 310170499 | 0.8158(15) | 0.018–0.045 | V1022 Her: UV+BY, no period | [TIC310170499](TIC310170499/) |
| TIC 237211224 | 0.8116(13) | 0.012–0.015 | Gaia DR3 2289127756709633664: ROT, no period | [TIC237211224](TIC237211224/) |
| TIC 232573695 | 1.0877(42) | 0.003–0.030 | Gaia DR3 1423851103951550976: RS, no period | [TIC232573695](TIC232573695/) |
| TIC 303946923 | 1.4600(32) | 0.002–0.005 | Gaia DR3 5248007658377932800: ROT, no period | [TIC303946923](TIC303946923/) |
| TIC 262722292 | 1.618(24) | 0.017–0.057 | Gaia DR3 580547052908336896: RS, no period | [TIC262722292](TIC262722292/) |
| TIC 41230546 | 7.47(14) | 0.014–0.032 | Gaia DR3 5283902246271491072: RS, no period | [TIC41230546](TIC41230546/) |
| TIC 272085437 | 7.99(18) | 0.009–0.026 | Gaia DR3 5263101337390488192: ROT, no period | [TIC272085437](TIC272085437/) |

## Notes

- **TIC 342671380:** strongly eccentric (Min II at phase 0.317, e cos ω ≈ 0.29); the eclipses last about 10.5 h
  (Min I) and 4.6 h (Min II). Found on TIC 342671370, 18″ away. In `fold.png` the labels are the other way round
  (the plot calls the shallower eclipse Min I); the table follows the convention that Min I is the deeper.
- **TIC 287318353:** two equal 3.5-mmag eclipses every 0.16667 d. Its common-proper-motion companion 3″ away
  (Gaia DR3 4550841557503143168, RUWE 12.6) is the more likely source, but TESS cannot separate it, or
  TIC 287318354 (7″), from the K dwarf.
- **TIC 207012283:** an eclipsing binary at 5.872547 d in the TESS Ten Thousand Catalog (Kostov et al. 2025,
  ApJS 279, 50), without a secondary eclipse; one is detected here (14.6 ppt, phase 0.498).
- **TIC 415641176:** spot modulation at 1.652 d as well as the 1.6563-d eclipses.
- **TIC 440852527 (ASAS J071811+1735.2):** 0.2303 d, or a contact binary at twice that.
- **BD−13 1046 (TIC 348773952)**, a sixth new detached binary from the search, is submitted to VSX separately
  ([vsx/TIC348773952](../vsx/TIC348773952/)).
