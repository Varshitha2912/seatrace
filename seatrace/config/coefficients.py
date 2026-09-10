"""
Coefficients — the single source of truth for every number used in the SeaTrace
carbon model.

Project rule: NOBODY HARDCODES NUMBERS. Every coefficient used anywhere in
modules/ must be imported from here, never typed inline. If a module needs a
new number, add it here first — with a source, a range, and an honest
assessment of how solid it is.

This file mirrors the "Coefficients" database in the team's Notion project hub
(SeaTrace — Team 41 Project Hub > Coefficients). That Notion database is the
canonical live copy — when a value changes there, update it here too and log
the change in the Changes Log.

Each entry is a dict with:
    id            Notion coefficient ID (N-01 .. N-14)
    parameter     Short name
    plain_english Plain-language explanation of what this number means
    value         Current value (string "TO FIND"/"TO CONFIRM"/"TO COUNT" for
                   blocking unknowns, otherwise a float, or a string for
                   non-numeric values like a date window)
    unit          Unit of measurement
    range         Literature range or "n/a"
    source        Citation / where this came from
    original_region  Where the source data was actually measured
    type          One of: Literature-derived, Transferred region,
                   Transferred species, Measured, Derived, Assumed
    how_solid     Honest caveat text — read this before trusting the number
    status        Notion status: "Not started" | "In progress" | "Done"
    owner         Team member responsible
"""

COEFFICIENTS = {
    "N-01": {
        "parameter": "Carbon content of biomass",
        "plain_english": "If you dry out the seaweed, what fraction of what's left is carbon.",
        "value": 0.3217,
        "unit": "fraction of dry weight",
        "range": "0.24 - 0.32",
        "source": (
            "Reed & Miller (2021), cited in Gould et al. (2025), Limnology & "
            "Oceanography Letters: 'dry biomass is 32.17% C' for Macrocystis "
            "pyrifera (California). SUPERSEDES the earlier Ecklonia radiata "
            "value (0.30, Staehr & Wernberg 2009) now that Blocker B-01 has "
            "independently confirmed the Tower Bay species is Macrocystis "
            "pyrifera, not Ecklonia radiata - see B-01 for the citation and "
            "a thermal-tolerance cross-check corroborating it."
        ),
        "original_region": "California (Santa Barbara Channel) - Macrocystis pyrifera (right species per B-01)",
        "type": "Transferred region",
        "how_solid": (
            "GOOD - direct, species-specific %C figure via a 2025 "
            "peer-reviewed synthesis citing the primary source. Geographic "
            "transfer caveat remains (California, not Tasmania) - same "
            "category of caveat as N-02/N-07 below. Range field still shows "
            "the old Ecklonia-derived bounds and needs updating once a "
            "Macrocystis-specific range is found."
        ),
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-02": {
        "parameter": "Detrital decay rate",
        "plain_english": "Once a bit of seaweed breaks off, how fast it rots away. Half is gone in about 9 days.",
        "value": 0.075,
        "unit": "per day",
        "range": "0.044 - 0.106",
        "source": "Filbee-Dexter et al. (2023), Scientific Reports - kelp detritus export via dense shelf water transport",
        "original_region": "Western Australia continental shelf",
        "type": "Transferred region",
        "how_solid": (
            "GOOD. Right species (Ecklonia radiata) and same temperate reef "
            "system, but measured in WA not Tasmania. We use it and document "
            "the transfer."
        ),
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-03": {
        "parameter": "Detritus export fraction",
        "plain_english": "Of everything the seaweed grows, how much drifts away rather than being harvested. About 71%.",
        "value": 0.71,
        "unit": "fraction of production",
        "range": "0.70 - 0.80",
        "source": "Carbon export from seaweed forests to deep ocean sinks. Verify publisher version.",
        "original_region": "Global synthesis",
        "type": "Literature-derived",
        "how_solid": (
            "GOOD. Global average with a tight standard error. Australian "
            "studies report ~80%, so 0.71 is the conservative end. Test the "
            "full range in sensitivity analysis."
        ),
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-04": {
        "parameter": "POC exported to deep sea",
        "plain_english": "Of the bits that drift away, how much sinks to deep water where the carbon stays locked up. About 11%.",
        "value": 0.11,
        "unit": "fraction of exported POC",
        "range": "0.06 - 0.17 (assumed)",
        "source": "Krause-Jensen & Duarte (2016), Nature Geoscience 9(10), 737-742",
        "original_region": "Global",
        "type": "Literature-derived",
        "how_solid": (
            "OK. The standard figure used for nearshore kelp forests "
            "worldwide. The paper states no uncertainty range, so ours is "
            "assumed - that assumption must be documented."
        ),
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-05": {
        "parameter": "POC buried in shelf sediment",
        "plain_english": "Of the bits that drift away, how much settles into seafloor mud and stays there. About 4%.",
        "value": 0.04,
        "unit": "fraction of exported POC",
        "range": "0.02 - 0.06 (assumed)",
        "source": "Krause-Jensen & Duarte (2016), Nature Geoscience 9(10), 737-742",
        "original_region": "Global",
        "type": "Literature-derived",
        "how_solid": "OK. Same source and same caveat as N-04. Cite the primary paper, never a secondary summary or blog.",
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-06": {
        "parameter": "Remineralised fraction",
        "plain_english": "Everything else - eaten or rotted, carbon returns to the water and air. No climate benefit.",
        "value": "calculate as residual",
        "unit": "fraction of exported carbon",
        "range": "wide",
        "source": "Balance of N-04 and N-05. Cross-check against deep ocean monitoring reporting >90% remineralisation.",
        "original_region": "n/a",
        "type": "Derived",
        "how_solid": (
            "UNCERTAIN. Lab studies suggest over 90% is lost this way, which "
            "does not fully agree with our other numbers. That disagreement "
            "IS our uncertainty - report it, do not resolve it away."
        ),
        "status": "Not started",
        "owner": "Khushi",
    },
    "N-07": {
        "parameter": "Cross-shelf export with decay",
        "plain_english": "How much detritus makes it past the continental shelf edge once you account for it rotting on the way.",
        "value": 0.21,
        "unit": "fraction",
        "range": "0.17 - 0.29",
        "source": "Filbee-Dexter et al. (2023), Scientific Reports",
        "original_region": "Western Australia continental shelf",
        "type": "Transferred region",
        "how_solid": "GOOD, with the same WA-to-Tasmania transfer caveat as N-02.",
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-08": {
        "parameter": "Growing season window",
        "plain_english": "When the kelp goes in the water and when it's harvested. This is the window we search satellite images for.",
        "value": "April - August",
        "unit": "months",
        "range": "n/a",
        "source": "Biancacci et al. (2022a), via Botanica Marina Tasmania review",
        "original_region": "Southeast Tasmania",
        "type": "Literature-derived",
        "how_solid": (
            "GOOD for location - region-matched. But derived for Macrocystis "
            "pyrifera. Confirm it applies if we model Ecklonia radiata."
        ),
        "status": "In progress",
        "owner": "Moniesh",
    },
    "N-09": {
        "parameter": "Farm location",
        "plain_english": "Exactly where the farm is. Needed to draw it on the map and point the satellite at it.",
        "value": (
            "4 corners (WGS84): -43.387917,147.034183 / -43.389583,147.039067 / "
            "-43.390967,147.037833 / -43.389333,147.033033. "
            "Centroid: -43.389450,147.036029"
        ),
        "unit": "lat / lon",
        "range": "n/a",
        "source": (
            "Marine and Safety Tasmania (MAST) Notice to Mariners "
            "M276-26(T), 'D'Entrecasteaux Channel, Tower Bay - Mooring "
            "Works', published 4 Aug 2026. Permit area marked by 4 IALA "
            "special marks at the coordinates above (converted from DMS: "
            "43 23.275'S 147 02.051'E / 43 23.375'S 147 02.344'E / "
            "43 23.458'S 147 02.270'E / 43 23.360'S 147 01.982'E). "
            "https://mast.tas.gov.au/notices/m276-26t-dentrecasteaux-channel-tower-bay-mooring-works/"
        ),
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": (
            "GOOD - authoritative government source (navigational safety "
            "notice, not a secondary citation). Scientific Research Permit "
            "site, not a commercial Marine Farm Lease - active through "
            "30 July 2027. See also modules/mapping.py, which already draws "
            "this boundary (was hardcoded there separately from here - now "
            "synced)."
        ),
        "status": "Done",
        "owner": "Ramesh",
    },
    "N-10": {
        "parameter": "Farm area",
        "plain_english": "How big the farm is. Determines whether we can see it from satellite at all.",
        "value": 7.875,
        "unit": "hectares",
        "range": "n/a",
        "source": "Shoelace-formula calculation from the N-09 corner coordinates (MAST Notice M276-26(T)).",
        "original_region": "Southeast Tasmania",
        "type": "Derived",
        "how_solid": (
            "GOOD - resolves Blocker B-02. ~7.875 ha = ~787 Sentinel-2 "
            "pixels (1 ha = 100 pixels), well above the ~1 ha satellite-"
            "viability threshold."
        ),
        "status": "Done",
        "owner": "Moniesh",
    },
    "N-11": {
        "parameter": "Modelled species",
        "plain_english": "Which of the three seaweeds grown at Tower Bay we're actually modelling.",
        "value": "Macrocystis pyrifera (giant kelp) - best-evidenced answer, see Blocker B-01",
        "unit": "n/a",
        "range": "n/a",
        "source": "Tower Bay farms Ecklonia radiata, Macrocystis pyrifera and Lessonia corrugata",
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": (
            "B-01 resolved via independent research (not an IMAS reply): "
            "Blue Economy CRC's own project page names Tower Bay directly - "
            "giant kelp was out-planted there and killed by the 2023-24 "
            "heatwave. Corroborated by a thermal-tolerance cross-check "
            "(20-21C kill temperature fits Macrocystis's known Tasmanian "
            "sensitivity far better than Ecklonia radiata or Lessonia "
            "corrugata). Ramesh has separately emailed IMAS directly "
            "(9 Sept) for an official confirmation - still pending, revisit "
            "if that reply says otherwise. This change means N-01/N-02/N-07 "
            "need Macrocystis-specific values - N-01 already updated."
        ),
        "status": "In progress",
        "owner": "Ramesh",
    },
    "N-12": {
        "parameter": "Usable Sentinel-2 scenes",
        "plain_english": "How many clear, non-cloudy satellite images we can get across one growing season.",
        "value": "TO COUNT",
        "unit": "scenes per season",
        "range": "n/a",
        "source": "Copernicus Data Space archive query",
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": (
            "BLOCKING - see Blocker B-03. Fewer than six changes our "
            "temporal resolution assumption and may trigger the "
            "literature-biomass fallback."
        ),
        "status": "Not started",
        "owner": "Moniesh",
    },
    "N-13": {
        "parameter": "Dry matter fraction",
        "plain_english": "How much of the wet seaweed is actually solid matter rather than water.",
        "value": 0.055,  # see range - a second source (FAO, North America) says 0.118; unresolved conflict
        "unit": "fraction of wet weight",
        "range": "0.055 - 0.118",
        "source": (
            "Two Macrocystis pyrifera sources disagree: (1) Forbes et al. "
            "(2025), J. Phycol., 'A historical review of giant kelp "
            "harvesting in Tasmania' - real 1970-71 Tasmanian harvest "
            "records give a wet-to-dry conversion factor of 0.055. (2) FAO "
            "Fisheries Technical Paper 'Biology of the Macrocystis resource "
            "in North America' - reports 88.2% water content, i.e. ~0.118 "
            "dry matter (North America, not Tasmania)."
        ),
        "original_region": "Tasmania (Forbes 2025) vs North America (FAO) - conflicting",
        "type": "Literature-derived",
        "how_solid": (
            "PARTIAL - not fully resolved. Tasmania-specific figure (0.055) "
            "is the better regional match but notably lower than the North "
            "America figure and lower than this project's old placeholder "
            "range (0.10-0.15). Possibly both are correct for different "
            "populations/seasons/measurement methods (1970s commercial "
            "dry-down vs lab wet-content). Using the Tasmania value (0.055) "
            "as current best guess but flagging - Khushi should verify "
            "against the Forbes 2025 methods section before trusting this."
        ),
        "status": "In progress",
        "owner": "Khushi",
    },
    "N-14": {
        "parameter": "Kelp yield per hectare",
        "plain_english": "How much seaweed a hectare of farm produces in a season. Only needed if we use the literature fallback instead of satellite.",
        "value": 12,  # tonnes/ha, mean; see range for max
        "unit": "tonnes per hectare",
        "range": "10 - 20 t/ha",
        "source": (
            "Forbes et al. (2025), J. Phycol., 'A historical review of "
            "giant kelp harvesting in Tasmania'. Historical Tasmanian "
            "surveys: potential yield ~1000-1200 t/km2 (10-12 t/ha); "
            "Alginates Australia's own records: mean 1200 t/km2, max 2000 "
            "t/km2 (12 t/ha mean, 20 t/ha max)."
        ),
        "original_region": "Tasmania - Macrocystis pyrifera, wild-harvested forests, 1970s data",
        "type": "Transferred region",
        "how_solid": (
            "GOOD region+species match (Tasmania, Macrocystis pyrifera - "
            "see B-01) but it's wild-forest harvest yield, not farmed-line "
            "yield - Tower Bay is a cultivation trial, not a natural forest "
            "being cut. Treat as an upper-bound sanity check for the "
            "literature fallback rather than a direct farm-yield figure."
        ),
        "status": "In progress",
        "owner": "Moniesh",
    },
}


def get_coefficient(coefficient_id: str) -> dict:
    """Look up a single coefficient by its Notion ID (e.g. 'N-01')."""
    try:
        return COEFFICIENTS[coefficient_id]
    except KeyError as exc:
        raise KeyError(
            f"Unknown coefficient id {coefficient_id!r}. "
            f"Valid ids: {sorted(COEFFICIENTS)}"
        ) from exc


def get_value(coefficient_id: str):
    """Return just the current value for a coefficient. Raises if it's still
    an unresolved placeholder (TO FIND / TO CONFIRM / TO COUNT), since a
    module should not silently compute with a missing number."""
    entry = get_coefficient(coefficient_id)
    value = entry["value"]
    if isinstance(value, str) and value.upper() in {"TO FIND", "TO CONFIRM", "TO COUNT"}:
        raise ValueError(
            f"{coefficient_id} ({entry['parameter']}) is still unresolved: "
            f"{value!r}. See Blockers in the Notion project hub."
        )
    return value


def list_blocking() -> list:
    """Return the IDs of coefficients that are still blocking (unresolved)."""
    blocking = []
    for cid, entry in COEFFICIENTS.items():
        value = entry["value"]
        if isinstance(value, str) and value.upper() in {"TO FIND", "TO CONFIRM", "TO COUNT"}:
            blocking.append(cid)
    return blocking
