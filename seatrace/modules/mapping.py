"""
Map + app (mapping half) — visualise the farm and results.

Owners: Ramesh + Varshitha
Epic 5 of 5. See config/coefficients.py for N-09 (farm location, currently
TO FIND).
"""

import folium

# Tower Bay, near Dover, southeast Tasmania - approximate centre per N-09
# (exact corners still TO FIND, see Blocker: Ramesh is finding exact corner
# coordinates).
TOWER_BAY_APPROX_LATLON = (-43.3, 147.0)


def get_map(farm_geometry=None, center=TOWER_BAY_APPROX_LATLON, zoom_start=11):
    """Build a Folium map centred on the study region, with a placeholder
    farm polygon until the real lease boundary (N-09) is confirmed.

    Args:
        farm_geometry: Optional GeoPandas/Shapely geometry for the real farm
            boundary. When None, a small placeholder polygon near the
            approximate Tower Bay coordinates is drawn instead.
        center: (lat, lon) to centre the map on. Defaults to the approximate
            Tower Bay location.
        zoom_start: Initial Folium zoom level.

    Returns:
        folium.Map
    """
    fmap = folium.Map(location=center, zoom_start=zoom_start, tiles="OpenStreetMap")

    folium.Marker(
        location=center,
        popup="Tower Bay (approx.) - IMAS lease, southeast Tasmania",
        tooltip="Tower Bay",
    ).add_to(fmap)

    if farm_geometry is not None:
        folium.GeoJson(farm_geometry, name="Farm boundary").add_to(fmap)
    else:
        # Placeholder farm polygon - NOT the real lease boundary. Swap this
        # out once N-09 (exact corner coordinates) is confirmed.
        lat, lon = center
        offset = 0.01
        placeholder_polygon = [
            [lat - offset, lon - offset],
            [lat - offset, lon + offset],
            [lat + offset, lon + offset],
            [lat + offset, lon - offset],
        ]
        folium.Polygon(
            locations=placeholder_polygon,
            color="#2a9d8f",
            fill=True,
            fill_opacity=0.3,
            popup="Placeholder farm boundary - real corners TO FIND (N-09)",
            tooltip="Placeholder - not the real lease boundary",
        ).add_to(fmap)

    folium.LayerControl().add_to(fmap)
    return fmap
