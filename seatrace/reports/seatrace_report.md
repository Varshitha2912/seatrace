# SeaTrace carbon report: Tower Bay kelp trial

Generated 2026-10-13, model 2.0 (13 Oct 2026, after source verification). Team 41, QUT. A transparent, literature-based estimate. **Not a certified carbon removal claim**: no approved methodology for seaweed farms exists yet (Verra M0172 is at draft stage).

## Result

One trial season (May to November 2024) stored an estimated **37 kg of CO2** long term (90% range 13 kg to 94 kg; 5,000 Monte Carlo runs, seed 41). With central values: 46 kg.

The kelp fixed about 619 kg of CO2 in total, but 64% of that left in the harvest and most of the rest was released again as lost kelp rotted.

This is not adjusted for how much CO2 the sea re-absorbs from the air after the kelp's uptake (air-sea re-equilibration), which Hurd et al. (2022) say must be shown before any credit claim. That would lower it further.

## Farm

- Site: IMAS Scientific Research Permit site, Tower Bay, D'Entrecasteaux Channel, Tasmania
- Permit area: 7.875 ha (the kelp occupied only part of it)
- Grow-line: 360 m (assumed equal to the Tinderbox sister site)
- Species: Macrocystis pyrifera (giant kelp)
- Corners (WGS84): -43.387917, 147.034183; -43.389583, 147.039067; -43.390967, 147.037833; -43.389333, 147.033033

## Pipeline, stage by stage (median and 90% range)

| Stage | p5 | Median | p95 | Unit |
|---|---:|---:|---:|---|
| Kelp harvested (wet) | 1.2097 | 2.9170 | 3.9521 | t |
| Kelp harvested (dry) | 0.1062 | 0.2607 | 0.3926 | t |
| Carbon fixed by the kelp | 0.0538 | 0.1322 | 0.2372 | t C |
| Carbon lost before harvest | 0.0196 | 0.0538 | 0.1360 | t C |
| Durable carbon | 0.0036 | 0.0102 | 0.0256 | t C |
| Durable CO2 | 0.0133 | 0.0372 | 0.0938 | t CO2 |

## Where the fixed carbon went (central case)

- Harvested and taken away: 64.0% (not counted as stored)
- Reached deep water: 7.0% (dissolved 5.5%, pieces 1.4%)
- Buried in the seabed: 0.5%
- Released back to water and air: 28.5%

## Season

| Month | Standing kelp (t wet) | Growth (t wet) | CO2 stored from that growth |
|---|---:|---:|---:|
| May | 0.07 | 0.07 | 1 kg |
| Jun | 0.28 | 0.21 | 3 kg |
| Jul | 0.83 | 0.55 | 7 kg |
| Aug | 1.83 | 1.00 | 13 kg |
| Sep | 2.84 | 1.00 | 13 kg |
| Oct | 3.39 | 0.55 | 7 kg |
| Nov | 3.60 | 0.21 | 3 kg |

Monthly split uses an assumed growth curve (N-21); the total does not depend on it.

## Scenarios

| Scenario | Kelp (t wet) | Share of fixed C stored | CO2 stored | vs central |
|---|---:|---:|---:|---:|
| Central | 3.6 | 7.5% | 46 kg | +0% |
| Late harvest | 3.6 | 12.9% | 183 kg | +295% |
| Low growth | 0.4 | 7.5% | 6 kg | -88% |
| Dissolved carbon upper case | 3.6 | 9.6% | 59 kg | +28% |
| Sheltered channel | 3.6 | 4.7% | 29 kg | -38% |
| Full-scale farm | 94.5 | 7.5% | 1.22 t | +2525% |

## Sensitivity (one input at a time, low to high)

| Input | At low | At high |
|---|---:|---:|
| Kelp lost as pieces before harvest (N-23) | 39 kg | 183 kg |
| Kelp grown per metre of line (N-15) | 6 kg | 56 kg |
| Carbon released dissolved (N-24) | 26 kg | 61 kg |
| Dry matter fraction (N-13) | 25 kg | 56 kg |
| Dissolved carbon reaching deep water (N-18) | 33 kg | 59 kg |
| Carbon content (N-01) | 37 kg | 51 kg |
| Pieces reaching deep sea (N-04) | 42 kg | 51 kg |
| Pieces buried on shelf (N-05) | 44 kg | 47 kg |

## Checks against published figures and similar sites

- **Fate tree reproduces the published global budget**: ours 10.9%, published 11.4% (match). Run with the paper's own inputs, our fate code gives 10.9% against the paper's 11.4%. The half-point gap comes from the paper rounding and listing 30% and 33% for the same DOC step, so the structure is coded correctly. Source: Krause-Jensen & Duarte (2016), Nature Geoscience: 173 of 1,521 TgC/yr of macroalgal NPP sequestered.
- **Share of fixed carbon stored, farm vs wild forest**: ours 7.5%, published 11.4% (lower, as expected). We store about 7.5% of the carbon the kelp fixes, versus about 11% in wild forests. The difference is the harvest: about 64% of fixed carbon is taken away and sold. Source: Krause-Jensen & Duarte (2016) for wild forests; Duarte et al. (2017) note the share is likely smaller for farms because the crop is harvested.
- **Kelp grown, compared with the sister site**: ours 3.60 t, published 3.60 t (assumed equal). Tower Bay is assumed to match Tinderbox. Nothing public gives the Tower Bay line length or harvest weight, so this check is circular until IMAS supplies them. Source: Blue Economy CRC (Nov 2024): ~3.6 t grown at Tinderbox on 360 m of line; Biancacci et al. (2022): 1.2 kg/m at other Tasmanian farms.
- **Kelp lost before harvest**: ours 13.0%, published 13.0% (transferred). Central value is taken from this study, so it matches by construction. The check is that it is a farm measurement, unlike the 71% wild-forest figure used before. Source: Fieler et al. (2021), farmed Saccharina in Norway: 8-13% lost by a normal harvest, 49% when delayed.
- **Full-scale farm: CO2 stored per hectare**: ours 0.15 t CO2/ha, published 1.06 t CO2/ha (lower). Even if the whole site were farmed, we estimate well under the 20-farm average. Wild-forest density (12 t/ha) is low for a farm, and our share buried on a sandy channel floor is small. Source: Duarte et al. (2025), Nature Climate Change: sediment burial attributable to 20 seaweed farms averaged 1.06 t CO2e/ha/yr; Bayley et al. (2017): wild Falklands giant kelp ~3.6 t CO2/ha/yr.
- **Share of lost carbon released again**: ours 79.2%, published 90.0% (disagrees). About 79% of the carbon lost before harvest is released again, against more than 90% from monitoring. If monitoring is right, stored carbon is roughly half our central value. Source: N-06 cross-check: deep-ocean monitoring and lab studies report more than 90% remineralisation.

## Spatial evidence

- Permit boundary: MAST Notices to Mariners M276-26(T) and M178-21(T); geodesic area 7.873 ha.
- Satellite timing: 14 clear Sentinel-2 scenes, May-Nov 2024; 24 clear Sentinel-2 scenes, Jun 2025-Feb 2026.
- Dispersion: channel water leaves in ~23 days (mostly north to Storm Bay; CSIRO). At 0.075/day decay, 18% of lost kelp is still intact on leaving (range 9% to 85%).

## Coefficients, sources and verification status

| ID | Parameter | Value | Range | Type | Source | Verified |
|---|---|---|---|---|---|---|
| N-01 | Carbon content of biomass | 0.3 fraction of dry weight | 0.24 - 0.33 | Transferred region | Reed & Brzezinski (2009): ~30% of Macrocystis dry weight is carbon (as used by Bayley et al. 2017, Falklands). SBC LTER data imply ~28% and note 20-40% variation (Rassweiler et al. 2008). 0.3217 (Reed & Miller 2021, via Gould et al. 2025) kept as the upper end; not independently re-checked 13 Oct 2026. | 13 Oct 2026: 30% (Reed & Brzezinski 2009) confirmed via Bayley et al. 2017; ~28% from SBC LTER dataset. Changed central from 0.3217 to 0.30. |
| N-02 | Detrital decay rate | 0.075 per day | 0.007 - 0.106 (widened 2 Oct 2026) | Transferred species | 0.075/day: Ecklonia radiata detritus, WA shelf (Filbee-Dexter / van der Mheen work, primary paper to verify). Lower bound: Filbee-Dexter et al. (2020), ~0.74%/day mean across 35 sites. | 13 Oct 2026: primary source for 0.075/day not found. Filbee-Dexter et al. 2024 did not use per-day rates; Smale et al. 2022 found Laminaria detritus can take >4 months to decompose (slower). Display only. |
| N-03 | Detritus export fraction (wild forests) | 0.71 fraction of net primary production | 0.71 +/- 0.06 SE | Literature-derived | Filbee-Dexter et al. (2024), Carbon export from seaweed forests to deep ocean sinks, Nature Geoscience: 'the fraction of the production that is exported as detritus (71% +/- 6 SE)'. | 13 Oct 2026: value confirmed in the paper. Misapplied to a farm before; now comparison only. |
| N-04 | POC exported to deep sea | 0.11 fraction of exported POC | 0.05 - 0.17 (assumed; low end = N-07 sheltered-channel case) | Literature-derived | Krause-Jensen & Duarte (2016), Nature Geoscience 9, 737-742: about 11% of POC export (35 TgC/yr) reaches the deep sea. | 13 Oct 2026: 11% of POC export confirmed in the paper. |
| N-05 | POC buried in shelf sediment | 0.046 fraction of POC retained on the shelf | 0.02 - 0.06 (assumed) | Literature-derived | Krause-Jensen & Duarte (2016): of the 89% of POC export retained on the shelf, 'an estimated 4.6% (14 TgC/yr) is buried in shelf sediments'. | 13 Oct 2026: 4.6% of shelf-retained POC confirmed in the paper. |
| N-06 | Remineralised fraction | calculate as residual fraction of exported carbon | wide | Derived | Residual of the fate tree. Cross-check: deep ocean monitoring reports >90% remineralisation. | 13 Oct 2026: residual, no source needed. Monitoring >90% cross-check not re-checked. |
| N-07 | Cross-shelf export with decay | 0.21 fraction | 0.05 - 0.51 (widened 2 Oct 2026) | Transferred species | van der Mheen et al. (2024), Scientific Reports 14: 51%/yr passes the shelf edge, 17-29% after decomposition. | 13 Oct 2026: 51%/yr past the shelf edge, 17-29% with decomposition, confirmed (van der Mheen et al. 2024 abstract). |
| N-08 | Growing season window | May to November 2024 months | n/a | Measured | Blue Economy CRC harvest note (22 Nov 2024): Tinderbox harvested ~6 months after outplanting; Tower Bay due for harvest the following week. Matches N-12 (14 clear scenes May-Nov 2024). Biancacci et al. (2022): April deployment, harvest window July-August in other Tasmanian sites. | 13 Oct 2026: changed from April-August to the 2024 trial window. |
| N-09 | Farm location | 4 corners lat / lon (WGS84) | n/a | Measured | MAST Notice to Mariners M276-26(T), D'Entrecasteaux Channel, Tower Bay - Mooring Works, 4 Aug 2026. | 13 Oct 2026: all four corners confirmed against MAST M276-26(T) and M178-21(T). Notice describes the permit area only, not the kelp infrastructure. |
| N-10 | Farm area | 7.875 hectares | n/a | Measured | Shoelace formula on the N-09 corners (~436 x 184 m). | 13 Oct 2026: geodesic area of N-09 = 7.873 ha (pyproj, WGS84). This is the permit area, not the area under kelp. |
| N-11 | Modelled species | Macrocystis pyrifera (giant kelp) n/a | n/a | Measured | Confirmed by Jeffrey Wright (IMAS) by email: three successful Macrocystis trials at Tower Bay, last ended Feb 2026. | 13 Oct 2026: IMAS email not re-checked; CRC pages confirm Macrocystis trials at Tower Bay. |
| N-12 | Usable Sentinel-2 scenes | 14 clear (May-Nov 2024); 24 clear (Jun 2025-Feb 2026) scenes per trial | n/a | Measured | Copernicus Browser statistical time series, Sentinel-2 L2A over the N-09 polygon, 161 acquisitions (redone 2 Oct 2026). | 13 Oct 2026: not re-checked (Copernicus counts from 2 Oct). Windows agree with the CRC harvest note. |
| N-13 | Dry matter fraction | 0.1 fraction of wet weight | 0.055 - 0.12 | Literature-derived | Reed & Brzezinski (2009): dry weight is 10% of wet (as used by Bayley et al. 2017); Duarte et al. (2017) use 0.1; SBC LTER data imply ~0.09; FAO (North America) 88.2% water = 0.118. Low end 0.055: Forbes et al. (2025) Tasmanian harvest records (not re-checked; may describe processed kelp). | 13 Oct 2026: 0.10 confirmed via Bayley et al. 2017 and Duarte et al. 2017. Forbes 2025 full text could not be opened. |
| N-14 | Kelp yield per hectare (wild forests) | 12.0 tonnes wet per hectare | 10 - 20 t/ha | Transferred region | Forbes et al. (2025) J. Phycol.: historical Tasmanian surveys 10-12 t/ha; Alginates Australia records mean 12, max 20 t/ha (not re-checked 13 Oct 2026). | 13 Oct 2026: not re-checked (Forbes 2025 page did not open). Use changed to scenario only. |
| N-15 | Farm yield per metre of grow-line | 10.0 kg wet per metre of line (~6 months) | 1.2 - 12 | Transferred region | Blue Economy CRC (22 Nov 2024): ~3.6 t of Macrocystis grown at Tinderbox on 360 m of grow-line in ~6 months = 10 kg/m. Low end: Biancacci et al. (2022) Front. Mar. Sci. 9:951538, mean 1.20 kg/m (max 1.5) for farmed Macrocystis at two Tasmanian sites, 2020. | 13 Oct 2026: CRC article re-read; Biancacci 2022 checked. |
| N-16 | Grow-line depth and site water depth | Lines ~5 or 10 m below surface; ~15 m water over sand metres | Lines 5-10 m | Assumed | Blue Economy CRC, Developing Production Systems for Offshore Kelp Mariculture; Biancacci et al. (2022) Front. Mar. Sci. | 13 Oct 2026: confirmed on the CRC kelp mariculture page (lines ~5 or 10 m; ~15 m water over sand at Tinderbox). |
| N-17 | DOC share of exported carbon | 0.52 fraction of exported carbon | 0.40 - 0.60 (assumed) | Literature-derived | Khushi's durable_fraction.py (8 Oct 2026), nested structure after Krause-Jensen & Duarte (2016). Registered 13 Oct 2026 (was mislabelled N-16 in the script). | 13 Oct 2026: DOC = 52% of macroalgal export confirmed in Krause-Jensen & Duarte 2016. Used only in the wild-forest comparison. |
| N-18 | DOC reaching deep water | 0.24 fraction of DOC | 0.15 - 0.33 | Assumed | Upper end: Krause-Jensen & Duarte (2016), 33% of DOC exported below the mixed layer, which they call an upper boundary (their Table 1 lists 30%). Central 0.24 from Khushi's durable_fraction.py; no primary source found 13 Oct 2026. | 13 Oct 2026: 0.33 upper boundary confirmed; 0.24 unsourced. Type changed to Assumed. |
| N-19 | Channel flushing time | 23.0 days | 20 (winter, whole channel) - 26 (overall) | Literature-derived | CSIRO hydrodynamic model of the D'Entrecasteaux Channel (2003-06). | 13 Oct 2026: confirmed, CSIRO (Marine and Freshwater Research MF09134): whole-region flushing ~20-26 days. |
| N-20 | Share of outflow leaving north | 0.75 fraction | 0.60 - 0.90 (assumed) | Assumed | CSIRO D'Entrecasteaux Channel model: most water leaves north into Storm Bay, a smaller share south. Exact split not published; 0.75 assumed. | 13 Oct 2026: direction confirmed (predominantly northward, small share south); CSIRO gives no percentage, so 0.75 stays assumed. CSIRO also notes the northern channel connects poorly with the rest. |
| N-21 | Seasonal growth curve | 1.2 logistic rate per month (midpoint at mid-season) | n/a | Assumed | Assumed logistic shape, scaled so end-of-season biomass equals N-10 x N-14. Satellite gives timing only (C-005). | 13 Oct 2026: assumed shape, no source needed; season totals don't depend on it. |
| N-22 | Grow-line length at Tower Bay | 360.0 metres | unknown | Assumed | ASSUMED equal to Tinderbox, the sister site in the same IMAS/CRC project: 360 m of grow-line on three 18 m rings and a 60 m array (Blue Economy CRC kelp mariculture page; harvest note 22 Nov 2024). | 13 Oct 2026: new. Replaces 'whole 7.9 ha permit area is kelp'. |
| N-23 | Kelp lost from the farm as pieces | 0.13 fraction of production | 0.08 - 0.49 | Transferred species | Fieler et al. (2021) Front. Mar. Sci. 8:632725, farmed Saccharina latissima, Norway: 8-13% of produced dry weight lost by a normal harvest; 49% when harvest was delayed to August. | 13 Oct 2026: new; checked in the paper. |
| N-24 | Carbon released dissolved (DOC) | 0.23 fraction of fixed carbon | 0.12 - 0.29 | Literature-derived | Central: Krause-Jensen & Duarte (2016), DOC export 355 of 1,521 TgC/yr NPP (23%). Range: Neves et al. (2025), farmed Saccharina latissima, DOC release 12-29% of fixed carbon (via SINTEF summary). | 13 Oct 2026: new; K-J&D figures checked in the paper, Neves et al. via SINTEF summary. |

Borrowed from another region or species: N-01, N-02, N-03, N-04, N-05, N-07, N-13, N-14, N-15, N-16, N-17, N-18, N-22, N-23, N-24.

## Limitations

1. Tower Bay's grow-line length and harvest weight are not public; both are assumed equal to Tinderbox.
2. Loss rates (N-23, N-24) were measured on Norwegian sugar-kelp farms, not Tasmanian giant kelp.
3. No one has measured where this farm's carbon went; fate fractions are bounded, not verified.
4. Air-sea re-equilibration is not modelled, so the figure is an upper bound on CO2 actually removed from the air.
5. Emissions from boats, moorings and processing (life-cycle) are not subtracted.
6. The 2023-24 Tower Bay trial was killed by a marine heatwave; a season can store nothing.
7. The dispersion footprint is schematic (decay x flushing time), not a circulation model.
