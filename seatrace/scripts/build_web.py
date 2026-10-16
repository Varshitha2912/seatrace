"""
Build web/index.html: the standalone browser version of SeaTrace.

    python scripts/build_web.py

Embeds the coefficient register, scenario definitions, map geometry and the
Python reference results into web/template.html, so the browser app uses
exactly the same numbers as the Python pipeline (project rule: no hardcoding).
"""

import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from config.coefficients import COEFFICIENTS, CO2_PER_C  # noqa: E402
from modules.carbon import PARAM_IDS  # noqa: E402
from modules.dispersion import load_geo  # noqa: E402
from modules.fate import LABELS, scenario_definitions  # noqa: E402
from modules.report import build, to_markdown  # noqa: E402

K = 1000.0  # svg units per degree of latitude


def projector(bbox):
    c = math.cos(math.radians((bbox["lat_min"] + bbox["lat_max"]) / 2))

    def p(lat, lon):
        return round((lon - bbox["lon_min"]) * c * K, 1), round((bbox["lat_max"] - lat) * K, 1)
    w = (bbox["lon_max"] - bbox["lon_min"]) * c * K
    h = (bbox["lat_max"] - bbox["lat_min"]) * K
    km_per_unit = 111.32 / K
    return p, round(w, 1), round(h, 1), km_per_unit


def land_path(bbox, proj):
    """Smoothed filled land polygons from the 1 km land mask."""
    from global_land_mask import globe
    from scipy.ndimage import gaussian_filter
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    st = 0.0015
    lats = np.arange(bbox["lat_max"] + 0.01, bbox["lat_min"] - 0.01, -st)
    lons = np.arange(bbox["lon_min"] - 0.01, bbox["lon_max"] + 0.01, st)
    la, lo = np.meshgrid(lats, lons, indexing="ij")
    m = gaussian_filter(globe.is_land(la, lo).astype(float), 2.2)
    fig, ax = plt.subplots()
    cs = ax.contourf(lons, lats, m, levels=[0.5, 2])
    d = []
    for path in cs.get_paths():
        for verts, code in path.iter_segments(simplify=False):
            x, y = proj(verts[1], verts[0])
            d.append(("M" if code == 1 else "L") + f"{x} {y}" if code in (1, 2) else "Z")
    plt.close(fig)
    return "".join(d)


def main():
    geo = load_geo()
    bbox = geo["bbox"]
    proj, w, h, kmu = projector(bbox)

    routes = []
    for key, name in (("path_north", "North to Storm Bay"), ("path_south", "South to the Southern Ocean")):
        pts, km, prev = [], 0.0, None
        for lat, lon in geo[key]:
            if prev:
                dlat = math.radians(lat - prev[0])
                dlon = math.radians(lon - prev[1]) * math.cos(math.radians((lat + prev[0]) / 2))
                km += 6371.0 * math.hypot(dlat, dlon)
            x, y = proj(lat, lon)
            pts.append([x, y, round(km, 3)])
            prev = (lat, lon)
        routes.append({"key": key, "name": name, "pts": pts})

    corners = COEFFICIENTS["N-09"]["value"]
    water = {"D'Entrecasteaux Channel", "Storm Bay", "Southern Ocean"}
    labels = [{"name": l["name"], "x": proj(l["lat"], l["lon"])[0], "y": proj(l["lat"], l["lon"])[1],
               "water": l["name"] in water} for l in geo["labels"]]

    ref = build(5000, 41)
    data = {
        "generated": ref["generated"],
        "co2PerC": CO2_PER_C,
        "coef": {cid: {k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()} for cid, c in COEFFICIENTS.items()},
        "paramIds": PARAM_IDS,
        "labels": LABELS,
        "scenarios": [{"name": n, "why": w_, "overrides": o, "wet": wet} for n, w_, o, wet in scenario_definitions()],
        "geo": {
            "w": w, "h": h, "kmPerUnit": kmu, "land": land_path(bbox, proj), "routes": routes,
            "farm": [proj(a, b) for a, b in corners],
            "farmCentroid": proj(*COEFFICIENTS["N-09"]["centroid"]),
            "labels": labels,
            "source": geo["source"],
        },
        "validation": ref["validation"],
        "reportMd": to_markdown(ref),
        "modelVersion": ref["model_version"],
        "python": {
            "point_durable_co2": ref["headline"]["durable_co2_point_t"],
            "mc_median": ref["headline"]["durable_co2_median_t"],
            "mc_p5": ref["headline"]["durable_co2_p5_t"],
            "mc_p95": ref["headline"]["durable_co2_p95_t"],
            "durable_fraction": ref["point_estimate"]["fractions"]["durable"],
        },
    }
    with open(os.path.join(ROOT, "web", "template.html")) as f:
        tpl = f.read()
    out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    path = os.path.join(ROOT, "web", "index.html")
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path, f"{len(out) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
