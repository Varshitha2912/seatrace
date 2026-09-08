# SeaTrace

**Team 41 — QUT Capstone**
Varshitha · Moniesh · Khushi · Ramesh · Shraddha Chandana

> The science exists. The data is public. The layer connecting them does not.
> SeaTrace builds that layer.

## What this is

Seaweed absorbs carbon. But when fragments break off and drift, nobody can
prove where that carbon ends up — buried on the seafloor (real removal),
eaten and released back to the air (no benefit), or exported to deep water
(real removal). This blocks seaweed carbon credits.

SeaTrace is a **transparent, literature-informed prototype** that estimates
carbon removal from free satellite imagery and published science, and
reports it as an honest range with the working shown. **It is not a
certified MRV system.** It documents its own assumptions, uncertainty, and
limitations at every step.

## Study site

IMAS lease, **Tower Bay near Dover, southeast Tasmania** (~43.3°S, 147.0°E —
exact corners still to be confirmed, see coefficient N-09). Growing season:
April–August.

**Species:** *Ecklonia radiata* (golden kelp) is the current working
assumption, but Tower Bay grows three species (*Ecklonia radiata*,
*Macrocystis pyrifera*, *Lessonia corrugata*) and this is not yet confirmed
(see coefficient N-11 and the team's Blockers database in Notion). If the
site is predominantly *Macrocystis*, coefficients N-01, N-02, and N-07 all
need redoing.

## The five pieces

1. **Biomass** — satellite imagery estimates how much seaweed grew (Moniesh)
2. **Carbon** — published coefficients convert biomass to carbon (Khushi)
3. **Fate** — where the carbon goes: buried, deep water, or released (Khushi)
4. **Uncertainty** — run it 200+ times, report a range not a number (Shraddha Chandana)
5. **Map + app** — visualise and deliver it (Ramesh + Varshitha)

## Stack

Python · Streamlit · GeoPandas · Folium

## Project rules

- **Nobody hardcodes numbers.** Everything comes from `config/coefficients.py`,
  which mirrors the team's Notion Coefficients database.
- **Push something every day**, even if broken.
- **Weekly integration test, every Friday.** Non-negotiable.
- **Nothing gets added without something being cut.** Log it in the Notion
  Changes Log.
- **Stuck for two hours? Ask the group.**

Not allowed until Sprint 4: ML biomass prediction, original ocean
circulation modelling, automated certification, real-time monitoring,
registry integration, UI polish.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

## Repo layout

```
app.py                    Streamlit shell — wires everything together
modules/
  biomass.py               get_biomass() — satellite biomass estimate (stub)
  carbon.py                biomass_to_carbon() — biomass -> carbon (stub)
  mapping.py                get_map() — Folium map of the study site
  uncertainty.py            run_simulation() — Monte Carlo, 200+ runs (stub)
config/
  coefficients.py           All 14 coefficients (N-01..N-14): values, ranges,
                             sources, and honest caveats. Single source of
                             truth — mirrors the Notion Coefficients database.
data/                       Local data cache (gitignored, kept via .gitkeep)
```

## Status

Sprint 1 scaffold: all four modules are stubs, wired together end to end and
smoke-tested. Real biomass/carbon/uncertainty logic depends on resolving the
open blockers below.

## Open blockers (owner / due — see Notion Blockers database for current status)

| ID | Question | Owner | Due |
|---|---|---|---|
| B-05 | When is this project actually due? | Varshitha | 09-10 |
| B-01 | Which species does Tower Bay actually grow? | Ramesh | 09-12 |
| B-03 | How many cloud-free Sentinel-2 images across the season? | Moniesh | 09-12 |
| B-04 | What is the carbon content of *Ecklonia radiata*? | Khushi | 09-12 |
| B-02 | Is the farm big enough to see from satellite? | Moniesh | 09-10 |

## Coefficients still needing real values

See `config/coefficients.py` for the full set with sources and caveats.
Currently unresolved (`TO FIND` / `TO CONFIRM` / `TO COUNT`):

- **N-09** farm location (exact corners)
- **N-10** farm area (hectares) — blocking, tied to B-02
- **N-11** modelled species — blocking, tied to B-01
- **N-12** usable Sentinel-2 scene count — blocking, tied to B-03
- **N-13** dry matter fraction
- **N-14** kelp yield per hectare (literature fallback insurance figure)
- **N-01** carbon content of biomass — currently a cross-species placeholder
  (*Saccharina*, not *Ecklonia*), tied to B-04

Full project context, task tracking, and the live Coefficients/Blockers/
Changes Log databases live in Notion: **🌊 SeaTrace — Team 41 Project Hub**.
