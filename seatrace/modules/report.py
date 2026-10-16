"""
Report generator - the per-farm carbon report SeaTrace exists to produce.

Owner: Ramesh. Epic E7 - "Build structured report generator" (Sprint 5).
Contains the estimate, uncertainty range, every assumption, all data sources,
the spatial evidence, verification status and limitations. Markdown + JSON.

    python -m modules.report            # writes reports/seatrace_report.md and .json
"""

import datetime as dt
import json
import os

from config.coefficients import COEFFICIENTS, get_coefficient, get_value, list_transferred
from modules.biomass import full_scale_biomass, get_biomass, season_series
from modules.carbon import biomass_to_carbon
from modules.dispersion import footprint
from modules.fate import one_at_a_time, scenarios
from modules.uncertainty import run_simulation
from modules.validation import checks

KG = 1000.0


def build(n_iterations: int = 5000, seed: int = 41) -> dict:
    b = get_biomass()
    point = biomass_to_carbon(b["wet_biomass_tonnes"])
    mc = run_simulation(n_iterations, seed)
    season = season_series(b["wet_biomass_tonnes"])
    for row in season:
        c = biomass_to_carbon(row["growth_wet_t"])
        row["carbon_t"] = c["carbon_t"]
        row["durable_co2_t"] = c["durable_co2_t"]
    return {
        "generated": dt.date.today().isoformat(),
        "model_version": "2.0 (13 Oct 2026, after source verification)",
        "farm": {
            "name": "IMAS Scientific Research Permit site, Tower Bay, D'Entrecasteaux Channel, Tasmania",
            "corners": get_coefficient("N-09")["value"],
            "permit_area_ha": get_value("N-10"),
            "line_m": get_value("N-22"),
            "species": get_value("N-11"),
            "season": get_value("N-08"),
        },
        "headline": {
            "durable_co2_median_t": mc["median"],
            "durable_co2_p5_t": mc["p5"],
            "durable_co2_p95_t": mc["p95"],
            "durable_co2_point_t": point["durable_co2_t"],
            "n_iterations": n_iterations, "seed": seed,
        },
        "biomass": dict(b),
        "full_scale": dict(full_scale_biomass()),
        "point_estimate": {k: v for k, v in point.items() if k != "params"},
        "params": point["params"],
        "season": season,
        "stages": mc["stages"],
        "scenarios": scenarios(),
        "sensitivity": one_at_a_time(),
        "validation": checks(),
        "dispersion": {k: v for k, v in footprint().items() if k != "routes"},
        "coefficients": {cid: dict(c) for cid, c in COEFFICIENTS.items()},
        "transferred": list_transferred(),
    }


def kg(t: float) -> str:
    return f"{t * KG:,.0f} kg" if t < 1 else f"{t:,.2f} t"


def to_markdown(r: dict) -> str:
    h, p, f = r["headline"], r["point_estimate"], r["point_estimate"]["fractions"]
    L = []
    L.append("# SeaTrace carbon report: Tower Bay kelp trial\n")
    L.append(f"Generated {r['generated']}, model {r['model_version']}. Team 41, QUT. "
             "A transparent, literature-based estimate. **Not a certified carbon removal claim**: no approved "
             "methodology for seaweed farms exists yet (Verra M0172 is at draft stage).\n")
    L.append("## Result\n")
    L.append(f"One trial season ({r['farm']['season']}) stored an estimated **{kg(h['durable_co2_median_t'])} of CO2** "
             f"long term (90% range {kg(h['durable_co2_p5_t'])} to {kg(h['durable_co2_p95_t'])}; "
             f"{h['n_iterations']:,} Monte Carlo runs, seed {h['seed']}). With central values: {kg(h['durable_co2_point_t'])}.\n")
    L.append(f"The kelp fixed about {kg(p['carbon_t'] * 44 / 12)} of CO2 in total, but {f['harvested']:.0%} of that left in the harvest "
             f"and most of the rest was released again as lost kelp rotted.\n")
    L.append("This is not adjusted for how much CO2 the sea re-absorbs from the air after the kelp's uptake "
             "(air-sea re-equilibration), which Hurd et al. (2022) say must be shown before any credit claim. That would lower it further.\n")
    L.append("## Farm\n")
    L.append(f"- Site: {r['farm']['name']}\n- Permit area: {r['farm']['permit_area_ha']} ha (the kelp occupied only part of it)\n"
             f"- Grow-line: {r['farm']['line_m']:.0f} m (assumed equal to the Tinderbox sister site)\n- Species: {r['farm']['species']}\n"
             "- Corners (WGS84): " + "; ".join(f"{a:.6f}, {b:.6f}" for a, b in r["farm"]["corners"]) + "\n")
    L.append("## Pipeline, stage by stage (median and 90% range)\n")
    L.append("| Stage | p5 | Median | p95 | Unit |\n|---|---:|---:|---:|---|")
    for s in r["stages"]:
        L.append(f"| {s['label']} | {s['p5']:.4f} | {s['median']:.4f} | {s['p95']:.4f} | {s['unit']} |")
    L.append("\n## Where the fixed carbon went (central case)\n")
    L.append(f"- Harvested and taken away: {f['harvested']:.1%} (not counted as stored)")
    L.append(f"- Reached deep water: {f['deep']:.1%} (dissolved {f['doc_deep']:.1%}, pieces {f['poc_deep']:.1%})")
    L.append(f"- Buried in the seabed: {f['buried']:.1%}")
    L.append(f"- Released back to water and air: {f['released']:.1%}\n")
    L.append("## Season\n")
    L.append("| Month | Standing kelp (t wet) | Growth (t wet) | CO2 stored from that growth |\n|---|---:|---:|---:|")
    for s in r["season"]:
        L.append(f"| {s['month']} | {s['standing_wet_t']:.2f} | {s['growth_wet_t']:.2f} | {kg(s['durable_co2_t'])} |")
    L.append("\nMonthly split uses an assumed growth curve (N-21); the total does not depend on it.\n")
    L.append("## Scenarios\n")
    L.append("| Scenario | Kelp (t wet) | Share of fixed C stored | CO2 stored | vs central |\n|---|---:|---:|---:|---:|")
    for s in r["scenarios"]:
        L.append(f"| {s['name']} | {s['wet_t']:.1f} | {s['durable_fraction']:.1%} | {kg(s['durable_co2_t'])} | {s['change_vs_central']:+.0%} |")
    L.append("\n## Sensitivity (one input at a time, low to high)\n")
    L.append("| Input | At low | At high |\n|---|---:|---:|")
    for s in r["sensitivity"]["rows"]:
        L.append(f"| {s['label']} | {kg(s['co2_at_low'])} | {kg(s['co2_at_high'])} |")
    L.append("\n## Checks against published figures and similar sites\n")
    for c in r["validation"]:
        fmt = (lambda v: f"{v:.1%}") if c["unit"] == "share" else (lambda v: f"{v:.2f} {c['unit']}")
        pub = "n/a" if c["published"] is None else fmt(c["published"])
        L.append(f"- **{c['check']}**: ours {fmt(c['ours'])}, published {pub} ({c['verdict']}). {c['explanation']} Source: {c['source']}.")
    d = r["dispersion"]
    L.append("\n## Spatial evidence\n")
    L.append("- Permit boundary: MAST Notices to Mariners M276-26(T) and M178-21(T); geodesic area 7.873 ha.")
    L.append("- Satellite timing: " + "; ".join(f"{s['clear']} clear Sentinel-2 scenes, {s['window']}" for s in r["biomass"]["satellite_timing"]) + ".")
    L.append(f"- Dispersion: channel water leaves in ~{d['flushing_days']:.0f} days (mostly north to Storm Bay; CSIRO). "
             f"At {d['decay_per_day']}/day decay, {d['intact_at_exit']:.0%} of lost kelp is still intact on leaving "
             f"(range {d['intact_at_exit_range'][0]:.0%} to {d['intact_at_exit_range'][1]:.0%}).\n")
    L.append("## Coefficients, sources and verification status\n")
    L.append("| ID | Parameter | Value | Range | Type | Source | Verified |\n|---|---|---|---|---|---|---|")
    for cid, c in r["coefficients"].items():
        val = c["value"] if not isinstance(c["value"], list) else "4 corners"
        L.append(f"| {cid} | {c['parameter']} | {val} {c['unit']} | {c['range']} | {c['type']} | {c['source']} | {c.get('verified', '')} |")
    L.append("\nBorrowed from another region or species: " + ", ".join(r["transferred"]) + ".\n")
    L.append("## Limitations\n")
    L.append("1. Tower Bay's grow-line length and harvest weight are not public; both are assumed equal to Tinderbox.")
    L.append("2. Loss rates (N-23, N-24) were measured on Norwegian sugar-kelp farms, not Tasmanian giant kelp.")
    L.append("3. No one has measured where this farm's carbon went; fate fractions are bounded, not verified.")
    L.append("4. Air-sea re-equilibration is not modelled, so the figure is an upper bound on CO2 actually removed from the air.")
    L.append("5. Emissions from boats, moorings and processing (life-cycle) are not subtracted.")
    L.append("6. The 2023-24 Tower Bay trial was killed by a marine heatwave; a season can store nothing.")
    L.append("7. The dispersion footprint is schematic (decay x flushing time), not a circulation model.")
    return "\n".join(L) + "\n"


def write(out_dir: str = "reports") -> tuple:
    r = build()
    os.makedirs(out_dir, exist_ok=True)
    md, js = os.path.join(out_dir, "seatrace_report.md"), os.path.join(out_dir, "seatrace_report.json")
    with open(md, "w") as fh:
        fh.write(to_markdown(r))
    with open(js, "w") as fh:
        json.dump(r, fh, indent=2, default=str)
    return md, js


if __name__ == "__main__":
    print(write())
