"""
Dispersion footprint - where shed kelp detritus is modelled to travel and settle.

Owner: Ramesh. Epic E6 - "Render dispersion footprint on the map" (Sprint 4).

Not an ocean circulation model (that's out of scope per the project rules).
It combines two published numbers with the channel geometry:
  - detritus decays as exp(-k t), k = N-02
  - water leaves the D'Entrecasteaux Channel after ~N-19 days, mostly north
    into Storm Bay (share N-20), the rest south
So the share of detritus still intact at distance s along a route is
exp(-k * s * T). Routes are water-only paths from data/geo.json.

This footprint is for display and explanation. It does not feed the carbon
number, which uses the registered fate fractions (modules/carbon.py).
"""

import json
import math
import os

from config.coefficients import get_coefficient, get_value

GEO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "geo.json")


def load_geo() -> dict:
    with open(GEO_PATH) as f:
        return json.load(f)


def _km(a, b):
    dlat = math.radians(b[0] - a[0])
    dlon = math.radians(b[1] - a[1]) * math.cos(math.radians((a[0] + b[0]) / 2))
    return 6371.0 * math.hypot(dlat, dlon)


def _weighted(path, k, T):
    seg = [0.0]
    for i in range(1, len(path)):
        seg.append(seg[-1] + _km(path[i - 1], path[i]))
    total = seg[-1]
    pts = [{"lat": p[0], "lon": p[1], "km": d, "intact": math.exp(-k * (d / total) * T)}
           for p, d in zip(path, seg)]
    return pts, total


def footprint(decay_per_day: float = None, flushing_days: float = None, north_share: float = None) -> dict:
    k = decay_per_day if decay_per_day is not None else get_value("N-02")
    T = flushing_days if flushing_days is not None else get_value("N-19")
    n = north_share if north_share is not None else get_value("N-20")
    geo = load_geo()
    north, north_km = _weighted(geo["path_north"], k, T)
    south, south_km = _weighted(geo["path_south"], k, T)
    exit_intact = math.exp(-k * T)
    k_lo, k_hi = get_coefficient("N-02")["low"], get_coefficient("N-02")["high"]
    return {
        "decay_per_day": k, "flushing_days": T, "north_share": n,
        "farm": get_coefficient("N-09")["value"],
        "routes": [
            {"name": "North to Storm Bay", "share": n, "km": north_km, "points": north},
            {"name": "South to the Southern Ocean", "share": 1 - n, "km": south_km, "points": south},
        ],
        "intact_at_exit": exit_intact,
        "intact_at_exit_range": (math.exp(-k_hi * T), math.exp(-k_lo * T)),
        "settles_in_channel": 1 - exit_intact,
        "seabed": get_coefficient("N-16")["value"],
        "notes": (
            "Detritus that rots inside the channel releases its carbon locally; a small share "
            "of the particles settles on the sandy seabed (~15 m) and may be buried (N-05). "
            "Pieces flushed out reach Storm Bay or the southern entrance, not yet the deep ocean."
        ),
    }
