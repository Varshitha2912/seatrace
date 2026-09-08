"""
Biomass — estimate how much seaweed grew from satellite imagery.

Owner: Moniesh
Epic 1 of 5. See config/coefficients.py for N-09 (farm location), N-10 (farm
area), N-12 (usable Sentinel-2 scenes), and N-14 (literature yield fallback).

Sprint 1: stub only. Not allowed until Sprint 4: ML biomass prediction.
"""

from config.coefficients import get_coefficient


def get_biomass(farm_geometry=None, start_date=None, end_date=None):
    """Estimate wet biomass (tonnes) for the farm over the given date window.

    This is a Sprint 1 stub. It returns a fixed placeholder value so the rest
    of the pipeline (carbon, fate, uncertainty, map) can be wired together and
    smoke-tested end to end before the real Sentinel-2 pipeline exists.

    Real implementation (later sprint) will:
      1. Pull Sentinel-2 scenes over farm_geometry between start_date/end_date
         (see N-12, usable scene count - currently blocked on B-03).
      2. Apply a biomass index (e.g. NDVI/FAI-derived) to estimate wet
         biomass per hectare.
      3. Multiply by farm area (N-10 - currently blocked on B-02).
      4. Fall back to the literature yield figure (N-14) if imagery is
         insufficient.

    Args:
        farm_geometry: A GeoPandas/Shapely geometry for the farm boundary.
            Sprint 1: unused, placeholder farm polygon lives in mapping.py.
        start_date, end_date: Growing season window. Defaults to N-08
            (April - August) when not supplied.

    Returns:
        dict with:
            wet_biomass_tonnes (float): placeholder estimate
            method (str): "stub" in Sprint 1
            notes (str): what's still missing
    """
    season = get_coefficient("N-08")["value"]

    # Placeholder value only - NOT derived from any real imagery yet.
    # Do not use this number for anything beyond wiring/smoke-testing.
    wet_biomass_tonnes = 12.5

    return {
        "wet_biomass_tonnes": wet_biomass_tonnes,
        "method": "stub",
        "season": season,
        "notes": (
            "Sprint 1 stub - fixed placeholder, not derived from satellite "
            "imagery. Needs N-09 (farm location), N-10 (farm area), and B-03 "
            "(Sentinel-2 scene count) resolved before this can be real."
        ),
    }
