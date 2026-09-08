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
        "value": 0.252,
        "unit": "fraction of dry weight",
        "range": "0.24 - 0.32",
        "source": "Reid et al. - weight ratios of kelps for IMTA. Verify publisher version via QUT Library.",
        "original_region": "Northern hemisphere - Saccharina latissima",
        "type": "Transferred species",
        "how_solid": (
            "WEAK. Completely different species. Must be replaced with an "
            "Ecklonia radiata value (see Blocker B-04) or we openly document "
            "the cross-species transfer and widen the range."
        ),
        "status": "Not started",
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
        "value": "TO FIND",
        "unit": "lat / lon",
        "range": "n/a",
        "source": "IMAS lease, Tower Bay near Dover, southeast Tasmania. Roughly 43.3S 147.0E.",
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": "Ramesh is finding exact corner coordinates.",
        "status": "Not started",
        "owner": "Ramesh",
    },
    "N-10": {
        "parameter": "Farm area",
        "plain_english": "How big the farm is. Determines whether we can see it from satellite at all.",
        "value": "TO FIND",
        "unit": "hectares",
        "range": "n/a",
        "source": "To measure from lease data or satellite imagery",
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": (
            "BLOCKING - see Blocker B-02. One hectare = 100 Sentinel-2 "
            "pixels. Under ~1 ha and satellite biomass estimation is not "
            "viable."
        ),
        "status": "Not started",
        "owner": "Moniesh",
    },
    "N-11": {
        "parameter": "Modelled species",
        "plain_english": "Which of the three seaweeds grown at Tower Bay we're actually modelling.",
        "value": "TO CONFIRM",
        "unit": "n/a",
        "range": "n/a",
        "source": "Tower Bay farms Ecklonia radiata, Macrocystis pyrifera and Lessonia corrugata",
        "original_region": "Southeast Tasmania",
        "type": "Measured",
        "how_solid": (
            "BLOCKING - see Blocker B-01. If the site is predominantly "
            "Macrocystis, then N-01, N-02 and N-07 all change."
        ),
        "status": "Not started",
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
        "value": "TO FIND",
        "unit": "fraction of wet weight",
        "range": "0.10 - 0.15",
        "source": "TO FIND - search kelp dry matter content",
        "original_region": "TBC",
        "type": "Literature-derived",
        "how_solid": (
            "Needed to convert the wet biomass Moniesh produces into the dry "
            "weight Khushi's carbon fraction applies to. Currently missing."
        ),
        "status": "Not started",
        "owner": "Khushi",
    },
    "N-14": {
        "parameter": "Kelp yield per hectare",
        "plain_english": "How much seaweed a hectare of farm produces in a season. Only needed if we use the literature fallback instead of satellite.",
        "value": "TO FIND",
        "unit": "tonnes per hectare",
        "range": "TBC",
        "source": "TO FIND - search Tasmanian or Australian kelp cultivation yield",
        "original_region": "TBC",
        "type": "Literature-derived",
        "how_solid": "Only required if Blocker B-02 or B-03 forces the literature biomass path. Find it as insurance.",
        "status": "Not started",
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
