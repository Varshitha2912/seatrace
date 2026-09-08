"""
Uncertainty — run the pipeline many times and report a range, not a number.

Owner: Shraddha Chandana
Epic 4 of 5. Moved here from Khushi in the workload rebalance (see Changes
Log C-002).

Not allowed until Sprint 4: none of the restrictions apply to this module
specifically, but keep the simulation simple (no ML) per the project rules.
"""

import random

import numpy as np

from config.coefficients import get_coefficient
from modules.carbon import biomass_to_carbon


def run_simulation(n_iterations: int = 200, wet_biomass_tonnes: float = 12.5, seed: int = None) -> dict:
    """Run a Monte Carlo simulation over the carbon estimate and report
    p5 / median / p95.

    Sprint 1: stub. Perturbs the two Epic-2 coefficients (N-01 carbon
    content, and the dry-matter-fraction placeholder) within their
    documented literature ranges, re-runs biomass_to_carbon() each time, and
    summarises the distribution of durable_carbon_tonnes.

    Args:
        n_iterations: Number of Monte Carlo draws. Project rule: 200+.
        wet_biomass_tonnes: Input biomass to propagate uncertainty through.
            Sprint 1: a fixed placeholder (see modules.biomass stub).
        seed: Optional RNG seed for reproducible test runs.

    Returns:
        dict with:
            n_iterations (int)
            p5, median, p95 (float): durable carbon tonnes at each
                percentile
            samples (list[float]): raw simulation output, for debugging
    """
    if n_iterations < 200:
        raise ValueError(
            f"Project rule: uncertainty simulation must use 200+ runs, got {n_iterations}"
        )

    rng = random.Random(seed)

    n01_range = get_coefficient("N-01")["range"]  # "0.24 - 0.32"
    n01_low, n01_high = _parse_range(n01_range, fallback=(0.24, 0.32))

    # N-13 (dry matter fraction) literature range is 0.10 - 0.15 per Notion,
    # even though the value itself is still TO FIND.
    dry_matter_low, dry_matter_high = 0.10, 0.15

    samples = []
    for _ in range(n_iterations):
        carbon_content_fraction = rng.uniform(n01_low, n01_high)
        dry_matter_fraction = rng.uniform(dry_matter_low, dry_matter_high)

        result = biomass_to_carbon(
            wet_biomass_tonnes,
            coeffs={
                "carbon_content_fraction": carbon_content_fraction,
                "dry_matter_fraction": dry_matter_fraction,
            },
        )
        samples.append(result["durable_carbon_tonnes"])

    p5, median, p95 = np.percentile(samples, [5, 50, 95])

    return {
        "n_iterations": n_iterations,
        "p5": float(p5),
        "median": float(median),
        "p95": float(p95),
        "samples": samples,
    }


def _parse_range(range_str: str, fallback: tuple) -> tuple:
    """Parse a Notion range string like '0.24 - 0.32' into (low, high).
    Falls back to the given tuple if parsing fails (e.g. 'n/a', 'wide')."""
    try:
        low_str, high_str = range_str.replace("–", "-").split("-")
        return float(low_str.strip()), float(high_str.strip())
    except (ValueError, AttributeError):
        return fallback
