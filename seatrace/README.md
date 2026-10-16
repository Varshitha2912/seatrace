# SeaTrace

**Team 41, QUT Capstone** · Varshitha · Moniesh · Khushi · Ramesh · Shraddha Chandana

> The science exists. The data is public. The layer connecting them does not.
> SeaTrace builds that layer.

Seaweed absorbs carbon, but when pieces break off and drift, nobody can prove
where that carbon ends up: buried in the seabed or carried to deep water (real
removal), or rotted and released (no benefit). SeaTrace estimates it for one
farm from published science and free data, and reports an honest range with
the working shown. **It is not a certified MRV system.**

## Result (Tower Bay, one trial season, model 2.0)

CO2 stored long term: **37 kg median, 90% range 13 to 95 kg** (5,000 Monte
Carlo runs, seed 41). The trial was research-sized (~360 m of grow-line, assumed
equal to the Tinderbox sister site). About 64% of the carbon the kelp fixed left
in the harvest; most of what broke off rotted and was released.

Model 2.0 (13 Oct 2026) replaced two wrong inputs from version 1 (7.9 ha of kelp
and a wild-forest loss share of 0.71), which had given 1.4 t. Every coefficient
now carries a `verified` note. See `docs/METHODOLOGY.md`. Not a certified carbon
removal claim: no approved methodology for seaweed farms exists yet.

## Site

IMAS Scientific Research Permit site, Tower Bay, D'Entrecasteaux Channel,
southeast Tasmania. 7.875 ha, *Macrocystis pyrifera* (giant kelp, confirmed by
IMAS), trial season May to November 2024. The 7.9 ha is the permit area, not the
area under kelp.

## Run it

```bash
pip install -r requirements.txt
python -m pytest tests          # 15 tests
python -m modules.report        # reports/seatrace_report.md + .json
streamlit run app.py
```

A phone-friendly HTML version of the app (same model, runs in the browser)
is in `web/index.html`.

## Repo layout

```
app.py                  Streamlit app: map, fate, uncertainty, sensitivity, validation, report
config/coefficients.py  All coefficients N-01..N-21 with ranges, sources, caveats (mirrors Notion)
modules/
  biomass.py            get_biomass(), season_series()            Moniesh   E2
  carbon.py             biomass_to_carbon(), fate split           Khushi    E3/E4
  fate.py               scenarios(), one_at_a_time()              Khushi    E4
  uncertainty.py        run_simulation(), stability_check()       Shraddha  E5
  validation.py         checks against published figures          Shraddha
  dispersion.py         footprint(): decay x channel flushing     Ramesh    E6
  mapping.py            Folium map: farm, depth basemap, footprint Ramesh   E6
  report.py             build(), to_markdown(), write()           Ramesh    E7
scripts/build_geo.py    builds data/geo.json (coastline + water-only routes)
docs/METHODOLOGY.md     how to reproduce every number
tests/                  pytest suite (also runs on GitHub Actions)
web/index.html          standalone browser app
```

## Project rules

- **Nobody hardcodes numbers.** Everything comes from `config/coefficients.py`.
- **Nothing gets added without something being cut.** Log it in the Notion Changes Log.
- Weekly integration test every Friday: `python -m pytest tests`.

## Open questions

- Tower Bay grow-line length and 2024 harvest weight (ask IMAS); the result scales with them.
- What happened to the harvested kelp (sold, composted or sunk).
- Exact harvest date (late harvests lose far more kelp).
- Source for N-18 = 0.24 (published upper boundary is 0.33).
