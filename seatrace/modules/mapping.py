"""
Map - the farm in context, with depth basemap and dispersion footprint.

Owners: Ramesh + Varshitha. Epic E6.
  Sprint 2: farm boundary (N-09), coastline and bathymetry context
  Sprint 4: dispersion footprint (modules/dispersion.py)
"""

import folium

from config.coefficients import get_coefficient
from modules.dispersion import footprint

OCEAN_TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}"


def get_map(zoom_start: int = 11, show_dispersion: bool = True) -> folium.Map:
    lat, lon = get_coefficient("N-09")["centroid"]
    fmap = folium.Map(location=(lat - 0.1, lon + 0.15), zoom_start=zoom_start, tiles=None)
    folium.TileLayer(OCEAN_TILES, attr="Esri, GEBCO, NOAA, Garmin", name="Ocean depth (Esri/GEBCO)").add_to(fmap)
    folium.TileLayer("OpenStreetMap", name="Streets (OSM)").add_to(fmap)

    folium.Polygon(
        locations=get_coefficient("N-09")["value"],
        color="#0b6e4f", weight=2, fill=True, fill_opacity=0.5,
        tooltip="Tower Bay research site, 7.9 ha (MAST M276-26(T))",
    ).add_to(fmap)

    if show_dispersion:
        fp = footprint()
        layer = folium.FeatureGroup(name="Detritus dispersion footprint")
        for route in fp["routes"]:
            pts = route["points"]
            for a, b in zip(pts, pts[1:]):
                folium.PolyLine(
                    [(a["lat"], a["lon"]), (b["lat"], b["lon"])],
                    color="#c2410c", weight=2 + 10 * route["share"] * a["intact"],
                    opacity=0.25 + 0.65 * a["intact"],
                ).add_to(layer)
            end = pts[-1]
            folium.CircleMarker((end["lat"], end["lon"]), radius=5, color="#c2410c", fill=True,
                                tooltip=f"{route['name']}: {route['share']:.0%} of outflow, "
                                        f"{fp['intact_at_exit']:.0%} of detritus still intact").add_to(layer)
        folium.Circle((lat, lon), radius=800, color="#7c3aed", fill=True, fill_opacity=0.15,
                      tooltip="Local settling zone on sandy seabed (~15 m): where buried carbon (N-05) ends up").add_to(layer)
        layer.add_to(fmap)

    folium.LayerControl().add_to(fmap)
    return fmap
