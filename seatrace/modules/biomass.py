"""
Biomass - how much kelp the Tower Bay trial grew.

Owner: Moniesh. Epic E2.

Revised 13 Oct 2026 after source verification. The 7.9 ha in N-10 is the
permit area, not the area under kelp. The CRC trials were research-scale:
three 18 m rings and a 60 m array, ~360 m of grow-line at the sister site
Tinderbox. So biomass is grow-line length x yield per metre:

    harvested wet biomass = N-22 (360 m, assumed = Tinderbox) x N-15 (10 kg/m)

Satellite imagery (N-12) still gives timing only (C-005).
The old area x wild yield figure (N-10 x N-14) is kept as the 'full-scale
farm' scenario.
"""

import math

from config.coefficients import get_coefficient, get_value


def get_biomass(yield_kg_per_m: float = None, line_m: float = None) -> dict:
    line = line_m if line_m is not None else get_value("N-22")
    y = yield_kg_per_m if yield_kg_per_m is not None else get_value("N-15")
    c = get_coefficient("N-15")
    return {
        "wet_biomass_tonnes": line * y / 1000,
        "low_tonnes": line * c["low"] / 1000,
        "high_tonnes": line * c["high"] / 1000,
        "line_m": line,
        "method": "grow-line length (N-22, assumed) x yield per metre (N-15)",
        "season": get_value("N-08"),
        "satellite_timing": get_coefficient("N-12")["scenes"],
        "notes": (
            "Tinderbox grew ~3.6 t on 360 m of line in ~6 months (Blue Economy CRC, Nov 2024). "
            "Tower Bay is assumed to have the same layout. Low end uses 1.2 kg/m from "
            "Biancacci et al. (2022). Ask IMAS for the Tower Bay line length and harvest weight."
        ),
    }


def full_scale_biomass() -> dict:
    """Scenario: the whole 7.9 ha permit area farmed at wild-forest density."""
    area = get_value("N-10")
    c = get_coefficient("N-14")
    return {"wet_biomass_tonnes": area * c["value"], "low_tonnes": area * c["low"],
            "high_tonnes": area * c["high"], "method": "N-10 x N-14 (scenario only)"}


def season_series(final_wet_tonnes: float, months=None) -> list:
    """Standing biomass and growth for each month of the season (N-08).

    Logistic shape (N-21, assumed) scaled so the last month equals the
    harvest biomass. Monthly increments sum exactly to the total.
    """
    months = months or get_coefficient("N-08")["months"]
    r = get_value("N-21")
    n = len(months)
    mid = (n - 1) / 2

    def raw(t):
        return 1.0 / (1.0 + math.exp(-r * (t - mid)))

    base = raw(-1)
    scale = final_wet_tonnes / (raw(n - 1) - base)
    rows, prev = [], 0.0
    for i, m in enumerate(months):
        standing = (raw(i) - base) * scale
        rows.append({"month": m, "standing_wet_t": standing, "growth_wet_t": standing - prev})
        prev = standing
    return rows
