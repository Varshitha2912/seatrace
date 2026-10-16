# SeaTrace methodology (model 2.0, 13 Oct 2026)

How to reproduce every number SeaTrace reports. All inputs live in
`config/coefficients.py`, each with a source, range and a `verified` note from
the 13 Oct 2026 source check. Nothing else in the code holds a model number
(published comparison values sit, labelled, in `modules/validation.py`).

## 1. Question

How much carbon did one season of the IMAS giant kelp (*Macrocystis pyrifera*)
trial at Tower Bay lock away for the long term, and where did it go? The output
is a range with every assumption shown. It is **not** a certified carbon
removal claim: no approved methodology for seaweed farms exists (Verra's seaweed
aquaculture methodology was archived in June 2024; framework M0172 is at draft
stage).

## 2. What changed in model 2.0 and why

| Change | Before | Now | Reason |
|---|---|---|---|
| Biomass basis | 7.875 ha permit area x 12 t/ha wild yield = 94.5 t | 360 m of line x 10 kg/m = 3.6 t | The permit area is not the kelp area. The CRC trials were three 18 m rings and a 60 m array. |
| N-15 yield per metre | 75 kg/m | 10 kg/m (range 1.2-12) | 3.6 t was grown on all 360 m at Tinderbox, not on the 48 m harvested. |
| Share of production lost | 0.71 (wild forests) | 0.13 as pieces (N-23) + 0.23 dissolved (N-24) | 0.71 is the wild-forest detritus share (Filbee-Dexter et al. 2024). Farms harvest most kelp; measured farm losses are 8-13%. |
| Harvested carbon | counted in 'stayed on lines' | explicitly not stored | It is sold or used and returns to the air within years. |
| N-13 dry matter | 0.055 | 0.10 (range 0.055-0.12) | Four sources give 0.09-0.12; the Tasmanian 0.055 is an unexplained outlier. |
| N-01 carbon content | 0.3217 | 0.30 (range 0.24-0.33) | Reed & Brzezinski 2009; SBC LTER ~0.28. |
| Season | April-August | May-November 2024 | Matches the actual Tower Bay trial and the satellite windows. |
| Monte Carlo | 2,000 runs | 5,000 runs | Heavier right tail needs more runs for a stable p95. |

## 3. Site

| Item | Value | ID | Verified |
|---|---|---|---|
| Permit boundary | 4 corners, MAST M276-26(T) / M178-21(T) | N-09 | yes, all corners |
| Permit area | 7.873 ha geodesic (WGS84) | N-10 | yes |
| Kelp line | 360 m, assumed equal to Tinderbox | N-22 | assumption |
| Species | *Macrocystis pyrifera* | N-11 | CRC pages |
| Season | May-November 2024 | N-08 | CRC harvest note |

## 4. Pipeline

```
harvested wet  W   = N-22 line (m) x N-15 yield (kg/m) / 1000
dry            D   = W x N-13
harvested C    Ch  = D x N-01
fixed C        Cf  = Ch / (1 - N-23 - N-24)
lost as pieces POC = Cf x N-23
leaked as DOC  DOC = Cf x N-24

POC to deep sea       POC x N-04                     (11% of POC export, Krause-Jensen & Duarte 2016)
POC buried on shelf   POC x (1 - N-04) x N-05        (4.6% of shelf-retained POC, same paper)
DOC to deep water     DOC x N-18
released              the rest of POC + DOC          (N-06)

stored long term      = deep + buried
CO2                   = stored C x 44/12
```

Central case: 3.6 t wet harvested, 169 kg C fixed, 64% harvested, 7.5% of
fixed carbon stored, **46 kg CO2**.

## 5. Uncertainty

Each run draws eight inputs independently: N-15 triangular (1.2, 10, 12);
N-13 triangular (0.055, 0.10, 0.12); N-01 triangular (0.24, 0.30, 0.33);
N-23 triangular (0.08, 0.13, 0.49); N-24 uniform 0.12-0.29; N-18 uniform
0.15-0.33; N-04 uniform 0.05-0.17; N-05 uniform 0.02-0.06. Line length (N-22)
is fixed and shown as a what-if.

5,000 runs, seed 41: **median 37 kg CO2, 90% range 13-94 kg**. Converged
(200,000 runs, Python and JavaScript separately): 13 / 37.5 / 95 kg. Stability
over five seeds at 5,000 runs: CV 0.8% (median), 1.6% (p95), limit 2%.

## 6. Sensitivity

Biggest drivers (low to high, others central): kelp lost as pieces 39-183 kg;
yield per metre 6-56 kg; DOC release 26-61 kg; dry matter 25-56 kg. Line length
scales everything in proportion. Scenarios: late harvest +295%; low growth
-88%; DOC upper case +28%; sheltered channel -38%; full-scale 7.9 ha farm at
wild-forest density 1.22 t.

## 7. Verification performed 13 Oct 2026

- **Code:** hand calculation equals module output to 1e-12; mass balance holds
  at all 256 low/high corners; Monte Carlo mean matches the analytic mean (the
  model is multilinear in independent inputs) within 0.05%; Python and the web
  app give identical outputs on 500 random input sets; percentile method matches
  numpy.
- **Sources:** every coefficient re-checked against its primary source where
  reachable; the outcome is in each entry's `verified` field.
- **Site:** MAST coordinates and geodesic area confirmed.
- **Comparisons:** see section 8.

## 8. Comparison with published figures and similar sites

| Check | SeaTrace | Published | Verdict |
|---|---|---|---|
| Fate tree with Krause-Jensen & Duarte inputs | 10.9% of NPP | 11.4% (173/1,521 TgC) | match (rounding in paper) |
| Share of fixed C stored, farm | 7.5% | ~11% wild forests | lower, as expected for a harvested crop (Duarte et al. 2017) |
| Kelp grown | 3.6 t | 3.6 t Tinderbox (CRC 2024); 1.2 kg/m elsewhere (Biancacci 2022) | assumed equal |
| Lost before harvest | 13% | 8-13% (Fieler et al. 2021) | transferred |
| Full-scale farm, per ha | 0.15 t CO2/ha | 1.06 t CO2e/ha/yr farm burial (Duarte et al. 2025, 20 farms); ~3.6 t CO2/ha/yr wild Falklands kelp (Bayley et al. 2017) | lower |
| Lost carbon released | 79% | >90% (monitoring) | disagrees; stored C could be ~half |

## 9. What a real verification would need (not done; cannot be done from desk data)

Following Hurd et al. (2022) forensic carbon accounting and the Ocean Visions
MRV priorities:

1. Measured Tower Bay line length, harvest weight and dry matter.
2. Measured erosion (hole-punch tagging) and DOC release on the crop.
3. Sediment traps and cores at and away from the site; carbon isotopes or eDNA
   to trace kelp carbon.
4. Air-sea CO2 re-equilibration in the channel (the ~20-26 day flushing time
   means some water leaves before re-equilibrating).
5. Baseline and additionality versus no farm; life-cycle emissions.
6. Storage for 100+ years demonstrated, then third-party audit under an
   approved methodology.

## 10. Limitations

1. Tower Bay line length and harvest weight are not public (assumed = Tinderbox).
2. Loss rates come from Norwegian *Saccharina* farms.
3. Fate fractions are global syntheses, bounded not verified.
4. Air-sea re-equilibration not modelled: figures are an upper bound on CO2 removed from the air.
5. Life-cycle emissions (boats, moorings, processing) not subtracted.
6. The 2023-24 trial was killed by a heatwave: a season can store nothing.
7. Inputs sampled independently; real correlations unknown.
8. Dispersion footprint is schematic, display only.

## 11. Reproduce

```bash
pip install -r requirements.txt
python -m pytest tests          # 15 tests
python -m modules.report        # reports/seatrace_report.md and .json
python scripts/build_web.py     # web/index.html (needs global-land-mask, scipy, matplotlib)
streamlit run app.py
```
