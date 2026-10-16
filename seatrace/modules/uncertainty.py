"""
Uncertainty - Monte Carlo over every registered range, end to end.

Owner: Shraddha. Epic E5.
  Sprint 2: samples the real coefficient ranges (no placeholders, no fake carbon function)
  Sprint 4: 1000+ iterations, stability check, error propagated through every stage
"""

import math

import numpy as np

from config.coefficients import get_coefficient, get_value
from modules.carbon import PARAM_IDS, biomass_to_carbon, harvest_wet_tonnes

STAGES = [
    ("wet_t", "Kelp harvested (wet)", "t"),
    ("dry_t", "Kelp harvested (dry)", "t"),
    ("carbon_t", "Carbon fixed by the kelp", "t C"),
    ("exported_t", "Carbon lost before harvest", "t C"),
    ("durable_t", "Durable carbon", "t C"),
    ("durable_co2_t", "Durable CO2", "t CO2"),
]


def _sample(rng, cid: str) -> float:
    c = get_coefficient(cid)
    lo, hi, mode = c["low"], c["high"], float(c["value"])
    if c["dist"] == "triangular":
        return float(rng.triangular(lo, mode, hi))
    if c["dist"] == "loguniform":
        return float(math.exp(rng.uniform(math.log(lo), math.log(hi))))
    return float(rng.uniform(lo, hi))


def run_simulation(n_iterations: int = 5000, seed: int = 41) -> dict:
    if n_iterations < 200:
        raise ValueError(f"Project rule: 200+ runs, got {n_iterations}")
    rng = np.random.default_rng(seed)
    stages = {k: [] for k, _, _ in STAGES}
    for _ in range(n_iterations):
        p = {name: _sample(rng, cid) for name, cid in PARAM_IDS.items()}
        r = biomass_to_carbon(harvest_wet_tonnes(p), p)
        for k in stages:
            stages[k].append(r[k])
    summary = []
    for k, label, unit in STAGES:
        a = np.array(stages[k])
        p5, p50, p95 = np.percentile(a, [5, 50, 95])
        summary.append({"stage": k, "label": label, "unit": unit,
                        "p5": float(p5), "median": float(p50), "p95": float(p95),
                        "mean": float(a.mean())})
    co2 = summary[-1]
    return {
        "n_iterations": n_iterations, "seed": seed,
        "p5": co2["p5"], "median": co2["median"], "p95": co2["p95"],
        "stages": summary,
        "samples": stages["durable_co2_t"],
    }


def stability_check(n_iterations: int = 5000, seeds=(1, 2, 3, 4, 5)) -> dict:
    """Is the distribution stable across runs? Coefficient of variation of the
    median and p95 across seeds; under 2% counts as stable."""
    meds, p95s = [], []
    for s in seeds:
        r = run_simulation(n_iterations, s)
        meds.append(r["median"])
        p95s.append(r["p95"])
    cv_med = float(np.std(meds) / np.mean(meds))
    cv_p95 = float(np.std(p95s) / np.mean(p95s))
    return {"n_iterations": n_iterations, "seeds": list(seeds), "medians": meds, "p95s": p95s,
            "cv_median": cv_med, "cv_p95": cv_p95, "stable": cv_med < 0.02 and cv_p95 < 0.02}
