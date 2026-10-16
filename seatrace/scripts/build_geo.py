"""
Build data/geo.json: coastline outlines and water-only dispersion paths for the
D'Entrecasteaux Channel around Tower Bay.

Run once (needs `pip install global-land-mask matplotlib`):
    python scripts/build_geo.py

Coastline: 1 km global land mask (global-land-mask package, derived from GLOBE
DEM), contoured at the land/water boundary. Coarse - good for context, not
navigation.
Paths: shortest water-only route (8-connected grid search) from the farm
centroid (N-09) to the north channel exit into Storm Bay and the south exit,
following the CSIRO channel model's outflow directions (N-20).
"""

import heapq
import json
import math
import os
import sys

import numpy as np
from global_land_mask import globe
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.coefficients import get_coefficient  # noqa: E402

BBOX = {"lat_min": -43.62, "lat_max": -42.98, "lon_min": 146.88, "lon_max": 147.45}
STEP = 0.004  # ~400 m grid, finer than the 1 km mask so contours are smooth
NORTH_EXIT = (-43.06, 147.36)   # channel mouth into Storm Bay / Derwent estuary
SOUTH_EXIT = (-43.56, 147.08)   # channel southern entrance


def grid():
    lats = np.arange(BBOX["lat_max"], BBOX["lat_min"] - 1e-9, -STEP)
    lons = np.arange(BBOX["lon_min"], BBOX["lon_max"] + 1e-9, STEP)
    lon2, lat2 = np.meshgrid(lons, lats)
    land = globe.is_land(lat2, lon2)
    return lats, lons, land


def coastline(lats, lons, land):
    fig, ax = plt.subplots()
    cs = ax.contour(lons, lats, land.astype(float), levels=[0.5])
    rings = []
    for path in cs.allsegs[0]:
        if len(path) < 6:
            continue
        rings.append([[round(float(la), 4), round(float(lo), 4)] for lo, la in path[::2]])
    plt.close(fig)
    return rings


def nearest_water(lats, lons, land, pt):
    i = int(round((BBOX["lat_max"] - pt[0]) / STEP))
    j = int(round((pt[1] - BBOX["lon_min"]) / STEP))
    best = None
    for di in range(-6, 7):
        for dj in range(-6, 7):
            a, b = i + di, j + dj
            if 0 <= a < land.shape[0] and 0 <= b < land.shape[1] and not land[a, b]:
                d = di * di + dj * dj
                if best is None or d < best[0]:
                    best = (d, a, b)
    return best[1], best[2]


def water_path(lats, lons, land, start, goal):
    """A* over water cells, with a penalty for hugging the coast so the path
    keeps to mid-channel."""
    s, g = nearest_water(lats, lons, land, start), nearest_water(lats, lons, land, goal)
    h, w = land.shape
    # distance-to-land penalty
    near = np.zeros_like(land, dtype=float)
    for di in range(-2, 3):
        for dj in range(-2, 3):
            near = np.maximum(near, np.roll(np.roll(land, di, 0), dj, 1).astype(float) * (3 - max(abs(di), abs(dj))))
    openq = [(0.0, s)]
    came, cost = {s: None}, {s: 0.0}
    while openq:
        _, cur = heapq.heappop(openq)
        if cur == g:
            break
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if not di and not dj:
                    continue
                n = (cur[0] + di, cur[1] + dj)
                if not (0 <= n[0] < h and 0 <= n[1] < w) or land[n]:
                    continue
                c = cost[cur] + math.hypot(di, dj) * (1 + near[n])
                if n not in cost or c < cost[n]:
                    cost[n] = c
                    came[n] = cur
                    heapq.heappush(openq, (c + math.hypot(n[0] - g[0], n[1] - g[1]), n))
    path, cur = [], g
    while cur is not None:
        path.append(cur)
        cur = came[cur]
    path.reverse()
    pts = [[round(float(lats[a]), 4), round(float(lons[b]), 4)] for a, b in path]
    # light smoothing
    sm = [pts[0]]
    for k in range(1, len(pts) - 1):
        sm.append([round((pts[k - 1][0] + pts[k][0] + pts[k + 1][0]) / 3, 4),
                   round((pts[k - 1][1] + pts[k][1] + pts[k + 1][1]) / 3, 4)])
    sm.append(pts[-1])
    return sm[::2] + [sm[-1]]


def main():
    lats, lons, land = grid()
    farm = get_coefficient("N-09")["centroid"]
    out = {
        "bbox": BBOX,
        "source": "global-land-mask (1 km, GLOBE DEM); paths: water-only grid search",
        "coastline": coastline(lats, lons, land),
        "path_north": water_path(lats, lons, land, farm, NORTH_EXIT),
        "path_south": water_path(lats, lons, land, farm, SOUTH_EXIT),
        "labels": [
            {"name": "Bruny Island", "lat": -43.33, "lon": 147.30},
            {"name": "Tasmania", "lat": -43.14, "lon": 146.97},
            {"name": "D'Entrecasteaux Channel", "lat": -43.31, "lon": 147.13},
            {"name": "Storm Bay", "lat": -43.05, "lon": 147.40},
            {"name": "Southern Ocean", "lat": -43.60, "lon": 147.22},
        ],
    }
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "geo.json")
    with open(path, "w") as f:
        json.dump(out, f)
    print("wrote", path, len(out["coastline"]), "rings", len(out["path_north"]), len(out["path_south"]))


if __name__ == "__main__":
    main()
