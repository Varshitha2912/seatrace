"""
Fate scenarios and sensitivity analysis.

Owner: Khushi. Epic E4 - "Build sensitivity analysis across alternative fate
fractions" (Sprint 3). Revised 13 Oct 2026 for the farm model.

  scenarios()        whole alternative cases, side by side
  one_at_a_time()    vary each input low/high with the rest central (tornado)
"""

from config.coefficients import get_coefficient, get_value
from modules.biomass import full_scale_biomass
from modules.carbon import PARAM_IDS, biomass_to_carbon, default_params, harvest_wet_tonnes

LABELS = {
    "yield_kg_per_m": "Kelp grown per metre of line (N-15)",
    "dry_matter_fraction": "Dry matter fraction (N-13)",
    "carbon_content_fraction": "Carbon content (N-01)",
    "poc_loss_fraction": "Kelp lost as pieces before harvest (N-23)",
    "doc_release_fraction": "Carbon released dissolved (N-24)",
    "doc_deep_fraction": "Dissolved carbon reaching deep water (N-18)",
    "poc_deep_fraction": "Pieces reaching deep sea (N-04)",
    "poc_burial_fraction": "Pieces buried on shelf (N-05)",
}


def scenario_definitions() -> list:
    """(name, why, overrides, wet_override_tonnes or None)."""
    fs = full_scale_biomass()["wet_biomass_tonnes"]
    return [
        ("Central", "Tinderbox-sized trial (360 m of line, 10 kg/m), farm loss rates from Norwegian kelp farms.", {}, None),
        ("Late harvest", "Harvest delayed into warming water: 49% lost as pieces, as measured when a Norwegian farm harvested in August.",
         {"poc_loss_fraction": get_coefficient("N-23")["high"]}, None),
        ("Low growth", "Yield of 1.2 kg/m, the mean for farmed giant kelp at two Tasmanian sites in 2020 (Biancacci et al. 2022).",
         {"yield_kg_per_m": get_coefficient("N-15")["low"]}, None),
        ("Dissolved carbon upper case", "33% of dissolved carbon reaches deep water, the upper boundary in Krause-Jensen & Duarte (2016).",
         {"doc_deep_fraction": get_coefficient("N-18")["high"]}, None),
        ("Sheltered channel", "Tower Bay sits in a sheltered ~15 m channel: deep export at the low end for both pieces and dissolved carbon.",
         {"poc_deep_fraction": get_coefficient("N-04")["low"], "doc_deep_fraction": get_coefficient("N-18")["low"]}, None),
        ("Full-scale farm", "If the whole 7.9 ha permit area held kelp at wild Tasmanian forest density (12 t/ha). Not what the trial did; shows the scale-up.",
         {}, fs),
    ]


def _run(overrides: dict, wet=None) -> dict:
    p = default_params()
    p.update(overrides)
    return biomass_to_carbon(wet if wet is not None else harvest_wet_tonnes(p), p)


def scenarios() -> list:
    central = _run({})["durable_co2_t"]
    rows = []
    for name, why, ov, wet in scenario_definitions():
        r = _run(ov, wet)
        rows.append({
            "name": name, "why": why, "wet_t": r["wet_t"],
            "durable_fraction": r["fractions"]["durable"],
            "buried": r["fractions"]["buried"], "deep": r["fractions"]["deep"],
            "released": r["fractions"]["released"],
            "durable_co2_t": r["durable_co2_t"],
            "change_vs_central": r["durable_co2_t"] / central - 1.0,
        })
    return rows


def one_at_a_time() -> dict:
    central = _run({})["durable_co2_t"]
    rows = []
    for name, cid in PARAM_IDS.items():
        c = get_coefficient(cid)
        lo = _run({name: c["low"]})["durable_co2_t"]
        hi = _run({name: c["high"]})["durable_co2_t"]
        rows.append({"param": name, "label": LABELS[name], "id": cid,
                     "low_value": c["low"], "high_value": c["high"],
                     "co2_at_low": lo, "co2_at_high": hi, "swing": abs(hi - lo)})
    rows.sort(key=lambda r: r["swing"], reverse=True)
    return {"central": central, "rows": rows}
