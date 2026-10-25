"""
Coefficients - the single source of truth for every number used in SeaTrace.

Project rule: NOBODY HARDCODES NUMBERS. Every coefficient used anywhere in
modules/ comes from here. This file mirrors the "Coefficients" database in the
Notion hub (SeaTrace - Team 41 Project Hub > Coefficients), synced 13 Oct 2026.

Each entry has:
    parameter, plain_english, unit
    value          central value used in the point estimate (float) or text
    low, high      numeric range sampled by the Monte Carlo (None if fixed/text)
    dist           "uniform" | "triangular" | "loguniform" | "fixed"
    range          range as written in Notion
    source, original_region
    type           Literature-derived | Transferred region | Transferred species
                   | Measured | Derived | Assumed
    transferred    True if taken from another region or species (Sprint 3 task)
    how_solid      caveat - read before trusting the number
    owner
"""

COEFFICIENTS = {
    "N-01": {
        "parameter": "Carbon content of biomass",
        "plain_english": "If you dry the kelp, what fraction of what's left is carbon.",
        "value": 0.30, "low": 0.24, "high": 0.33, "dist": "triangular",
        "unit": "fraction of dry weight",
        "range": "0.24 - 0.33",
        "source": 'Reed & Brzezinski (2009): ~30% of Macrocystis dry weight is carbon (as used by Bayley et al. 2017, Falklands). Bell & Kroeker (2022) J. Phycol. 58:773, Alaska: blade carbon 29.0 +/- 0.3% of dry mass year-round. SBC LTER data imply ~28% and note 20-40% variation. 0.3217 (Reed & Miller 2021, via Gould et al. 2025) kept as the upper end; not independently re-checked.',
        "original_region": "California - Macrocystis pyrifera",
        "type": "Transferred region", "transferred": True,
        "how_solid": "GOOD species match, several consistent sources (0.28-0.32). Not measured on Tasmanian farmed kelp.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: 30% (Reed & Brzezinski 2009, via Bayley 2017) and 29.0% (Bell & Kroeker 2022) confirmed; ~28% from SBC LTER dataset. Central changed from 0.3217 to 0.30.'
    },
    "N-02": {
        "parameter": "Detrital decay rate",
        "plain_english": "Once a piece of kelp breaks off, how fast it rots away.",
        "value": 0.075, "low": 0.007, "high": 0.106, "dist": "loguniform",
        "unit": "per day",
        "range": "0.007 - 0.106 (widened 2 Oct 2026)",
        "source": "Van der Mheen et al. (2024) Sci. Rep. 14 (doi:10.1038/s41598-023-51003-5): 'k = 0.075 +/- 0.031 per day is the decay rate for Ecklonia radiata as determined in situ on the WCS by Simpkins et al.' (half-life 9.2 +/- 2.7 days). Lower bound: Filbee-Dexter et al. (2020), ~0.74%/day mean across 35 sites.",
        "original_region": "Western Australia continental shelf",
        "type": "Transferred species", "transferred": True,
        "how_solid": "WEAK - transferred across species (Ecklonia -> Macrocystis) and region (WA -> Tasmania). Published rates disagree ~10x, so sampled log-uniformly. Used only for the dispersion footprint.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: 0.075 +/- 0.031 per day confirmed in van der Mheen et al. 2024 Methods (Ecklonia radiata, in situ, Wadjemup/Rottnest shelf, WA; original Simpkins et al.). Transfer to Tasmanian Macrocystis remains a caveat. Display only.'
    },
    "N-03": {
        "parameter": "Detritus export fraction (wild forests)",
        "plain_english": "In a wild kelp forest, how much of everything it grows breaks off as detritus. Not used for the farm, where most kelp is harvested.",
        "value": 0.71, "low": 0.65, "high": 0.77, "dist": "fixed",
        "unit": "fraction of net primary production",
        "range": "0.71 +/- 0.06 SE",
        "source": "Filbee-Dexter et al. (2024), Carbon export from seaweed forests to deep ocean sinks, Nature Geoscience: 'the fraction of the production that is exported as detritus (71% +/- 6 SE)'.",
        "original_region": "Global synthesis of wild seaweed forests",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "VERIFIED value, but it applies to wild forests, not farms. Replaced in the farm model by N-23 and N-24 (13 Oct 2026). Used only in the wild-forest comparison.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: value confirmed in the paper. Misapplied to a farm before; now comparison only.",
    },
    "N-04": {
        "parameter": "POC exported to deep sea",
        "plain_english": "Of the kelp pieces that drift away, how much sinks to deep water where the carbon stays locked up.",
        "value": 0.11, "low": 0.05, "high": 0.17, "dist": "uniform",
        "unit": "fraction of exported POC",
        "range": "0.05 - 0.17 (assumed; low end = N-07 sheltered-channel case)",
        "source": "Krause-Jensen & Duarte (2016), Nature Geoscience 9, 737-742: about 11% of POC export (35 TgC/yr) reaches the deep sea.",
        "original_region": "Global",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "VERIFIED value and basis (fraction of POC export). Global; a sheltered 15 m channel probably exports less, hence the low end.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: 11% of POC export confirmed in the paper.",
    },
    "N-05": {
        "parameter": "POC buried in shelf sediment",
        "plain_english": "Of the kelp pieces that stay on the shelf, how much settles into the seabed and stays there.",
        "value": 0.046, "low": 0.02, "high": 0.06, "dist": "uniform",
        "unit": "fraction of POC retained on the shelf",
        "range": "0.02 - 0.06 (assumed)",
        "source": "Krause-Jensen & Duarte (2016): of the 89% of POC export retained on the shelf, 'an estimated 4.6% (14 TgC/yr) is buried in shelf sediments'.",
        "original_region": "Global",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "VERIFIED value and basis. Khushi's 0.046 was right; the old Notion row (0.04 of exported POC) had the wrong basis.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: 4.6% of shelf-retained POC confirmed in the paper.",
    },
    "N-06": {
        "parameter": "Remineralised fraction",
        "plain_english": "Everything else: eaten or rotted, so the carbon goes back to the water and air. No climate benefit.",
        "value": "calculate as residual", "low": None, "high": None, "dist": "fixed",
        "unit": "fraction of exported carbon",
        "range": "wide",
        "source": "Residual of the fate tree. Cross-check: deep ocean monitoring reports >90% remineralisation.",
        "original_region": "n/a",
        "type": "Derived", "transferred": False,
        "how_solid": "UNCERTAIN. Our tree implies ~80%; lab studies suggest >90%. That gap is reported as uncertainty, not resolved away.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: residual, no source needed. Monitoring >90% cross-check not re-checked.'
    },
    "N-07": {
        "parameter": "Cross-shelf export with decay",
        "plain_english": "How much detritus gets past the continental shelf edge after rotting on the way.",
        "value": 0.21, "low": 0.05, "high": 0.51, "dist": "uniform",
        "unit": "fraction",
        "range": "0.05 - 0.51 (widened 2 Oct 2026)",
        "source": "van der Mheen et al. (2024), Scientific Reports 14: 51%/yr passes the shelf edge, 17-29% after decomposition.",
        "original_region": "Western Australia continental shelf",
        "type": "Transferred species", "transferred": True,
        "how_solid": "WEAK - open WA shelf vs sheltered D'Entrecasteaux Channel. Used in the 'sheltered channel' sensitivity scenario.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: 51%/yr past the shelf edge, 17-29% with decomposition, confirmed (van der Mheen et al. 2024 abstract).'
    },
    "N-08": {
        "parameter": "Growing season window",
        "plain_english": "When the kelp was in the water growing at Tower Bay.",
        "value": "May to November 2024", "low": None, "high": None, "dist": "fixed",
        "months": ["May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
        "unit": "months", "range": "n/a",
        "source": "Blue Economy CRC harvest note (22 Nov 2024): Tinderbox harvested ~6 months after outplanting; Tower Bay due for harvest the following week. Matches N-12 (14 clear scenes May-Nov 2024). Biancacci et al. (2022): April deployment, harvest window July-August in other Tasmanian sites.",
        "original_region": "Southeast Tasmania",
        "type": "Measured", "transferred": False,
        "how_solid": "GOOD for the 2024 trial. The 2023-24 trial was killed by the summer heatwave; the 2025-26 trial ran Jun-Feb. Was 'April - August' before 13 Oct 2026, which did not match Tower Bay.",
        "owner": "Moniesh",
        "verified": "13 Oct 2026: changed from April-August to the 2024 trial window.",
    },
    "N-09": {
        "parameter": "Farm location",
        "plain_english": "Exactly where the farm is.",
        "value": [(-43.387917, 147.034183), (-43.389583, 147.039067),
                  (-43.390967, 147.037833), (-43.389333, 147.033033)],
        "centroid": (-43.389450, 147.036029),
        "low": None, "high": None, "dist": "fixed",
        "unit": "lat / lon (WGS84)", "range": "n/a",
        "source": "MAST Notice to Mariners M276-26(T), D'Entrecasteaux Channel, Tower Bay - Mooring Works, 4 Aug 2026.",
        "original_region": "Southeast Tasmania",
        "type": "Measured", "transferred": False,
        "how_solid": "GOOD - authoritative government source. IMAS Scientific Research Permit site, active to 30 July 2027.",
        "owner": "Ramesh",
        "verified": '13 Oct 2026: all four corners confirmed against MAST M276-26(T) and M178-21(T). Notice describes the permit area only, not the kelp infrastructure.'
    },
    "N-10": {
        "parameter": "Farm area",
        "plain_english": "How big the farm is.",
        "value": 7.875, "low": None, "high": None, "dist": "fixed",
        "unit": "hectares", "range": "n/a",
        "source": "Shoelace formula on the N-09 corners (~436 x 184 m).",
        "original_region": "Southeast Tasmania",
        "type": "Measured", "transferred": False,
        "how_solid": "GOOD - derived from an authoritative coordinate source. ~787 Sentinel-2 pixels.",
        "owner": "Moniesh",
        "verified": '13 Oct 2026: geodesic area of N-09 = 7.873 ha (pyproj, WGS84). This is the permit area, not the area under kelp.'
    },
    "N-11": {
        "parameter": "Modelled species",
        "plain_english": "Which seaweed we model.",
        "value": "Macrocystis pyrifera (giant kelp)", "low": None, "high": None, "dist": "fixed",
        "unit": "n/a", "range": "n/a",
        "source": "Confirmed by Jeffrey Wright (IMAS) by email: three successful Macrocystis trials at Tower Bay, last ended Feb 2026.",
        "original_region": "Southeast Tasmania",
        "type": "Measured", "transferred": False,
        "how_solid": "GOOD - resolved (B-01).",
        "owner": "Ramesh",
        "verified": '13 Oct 2026: IMAS email not re-checked; CRC pages confirm Macrocystis trials at Tower Bay.'
    },
    "N-12": {
        "parameter": "Usable Sentinel-2 scenes",
        "plain_english": "How many clear satellite images cover the farm during a trial.",
        "value": "14 clear (May-Nov 2024); 24 clear (Jun 2025-Feb 2026)",
        "scenes": [{"window": "May-Nov 2024", "clear": 14}, {"window": "Jun 2025-Feb 2026", "clear": 24}],
        "low": None, "high": None, "dist": "fixed",
        "unit": "scenes per trial", "range": "n/a",
        "source": "Copernicus Browser statistical time series, Sentinel-2 L2A over the N-09 polygon, 161 acquisitions (redone 2 Oct 2026).",
        "original_region": "Southeast Tasmania",
        "type": "Measured", "transferred": False,
        "how_solid": "GOOD for counts. Kelp signal in NDVI is faint: satellite gives timing, not tonnes (Changes Log C-005).",
        "owner": "Moniesh",
        "verified": '13 Oct 2026: not re-checked (Copernicus counts from 2 Oct). Windows agree with the CRC harvest note.'
    },
    "N-13": {
        "parameter": "Dry matter fraction",
        "plain_english": "How much of the wet kelp is solid matter rather than water.",
        "value": 0.10, "low": 0.055, "high": 0.12, "dist": "triangular",
        "unit": "fraction of wet weight",
        "range": "0.055 - 0.12",
        "source": "Reed & Brzezinski (2009): dry weight 10% of wet (as used by Bayley et al. 2017); Bell & Kroeker (2022): mean 10.3%, observed 8.8-12.6% (Alaska); Duarte et al. (2017) use 0.1; FAO (North America) 88.2% water = 0.118. Low end 0.055: Forbes et al. (2025) J. Phycol., a 1970-71 company wet-to-dry factor from harvest records; the paper does not say how 'dry weight' was measured.",
        "original_region": "California / North America; Tasmania for the low end",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "GOOD central (four sources at 0.09-0.12). The Tasmanian 0.055 is an outlier until its method is checked. Was central 0.055 before 13 Oct 2026.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: 0.10 confirmed (Reed & Brzezinski via Bayley; Bell & Kroeker 10.3%, 8.8-12.6%). Forbes 2025 read: 0.055 is a factory-record ratio with unstated drying method, so kept only as the low end. Central changed from 0.055.'
    },
    "N-14": {
        "parameter": "Kelp yield per hectare (wild forests)",
        "plain_english": "How much kelp a hectare of wild Tasmanian forest holds. Used only for the full-scale farm scenario.",
        "value": 12.0, "low": 10.0, "high": 20.0, "dist": "triangular",
        "unit": "tonnes wet per hectare",
        "range": "10 - 20 t/ha",
        "source": "Forbes et al. (2025) J. Phycol.: earlier Tasmanian surveys 'potential yield of ~1000-1200 t/km2'; Alginates Australia 'mean = 1200 t/km2; maximum = 2000 t/km2'. These are per-harvest standing crop; forests 'could generally sustain only one harvest per year'. Wet weight inferred, not stated.",
        "original_region": "Tasmania - wild Macrocystis forests, 1970s",
        "type": "Transferred region", "transferred": True,
        "how_solid": "Wild-forest standing crop, not a farm yield. The trial did not cover the 7.9 ha permit area, so this is no longer used for the Tower Bay estimate (13 Oct 2026); only for the 'full-scale farm' scenario.",
        "owner": "Moniesh",
        "verified": '13 Oct 2026: figures confirmed in Forbes 2025 (per-harvest standing crop, wet weight inferred). Used only for the full-scale scenario. For comparison, a modelled 16 ha Macrocystis longline farm yields ~20 wet t/ha/yr (Frieder et al. 2022).'
    },
    "N-15": {
        "parameter": "Farm yield per metre of grow-line",
        "plain_english": "Kelp grown per metre of line on the IMAS trial leases.",
        "value": 10.0, "low": 1.2, "high": 12.0, "dist": "triangular",
        "unit": "kg wet per metre of line (~6 months)",
        "range": "1.2 - 12",
        "source": "Blue Economy CRC (22 Nov 2024): ~3.6 t of Macrocystis grown at Tinderbox on 360 m of grow-line in ~6 months = 10 kg/m. Low end: Biancacci et al. (2022) Front. Mar. Sci. 9:951538, mean 1.20 kg/m (max 1.5) for farmed Macrocystis at two Tasmanian sites, 2020.",
        "original_region": "Southeast Tasmania - Tinderbox lease (same IMAS project as Tower Bay)",
        "type": "Transferred region", "transferred": True,
        "how_solid": "GOOD project and species match. CORRECTED 13 Oct 2026: was 75 kg/m, from dividing the whole-lease 3.6 t by the 48 m harvested. The CRC note says 3.6 t was grown on 360 m in total.",
        "owner": "Moniesh",
        "verified": "13 Oct 2026: CRC article re-read; Biancacci 2022 checked.",
    },
    "N-16": {
        "parameter": "Grow-line depth and site water depth",
        "plain_english": "How deep the lines sit and how deep the water is.",
        "value": "Lines ~5 or 10 m below surface; ~15 m water over sand",
        "line_depth_m": 7.5, "water_depth_m": 15.0,
        "low": None, "high": None, "dist": "fixed",
        "unit": "metres", "range": "Lines 5-10 m",
        "source": "Blue Economy CRC, Developing Production Systems for Offshore Kelp Mariculture; Biancacci et al. (2022) Front. Mar. Sci.",
        "original_region": "Southeast Tasmania - Tinderbox description",
        "type": "Assumed", "transferred": True,
        "how_solid": "ASSUMED for Tower Bay from the same IMAS project. Explains the faint satellite signal.",
        "owner": "Moniesh",
        "verified": '13 Oct 2026: confirmed on the CRC kelp mariculture page (lines ~5 or 10 m; ~15 m water over sand at Tinderbox).'
    },
    "N-17": {
        "parameter": "DOC share of exported carbon",
        "plain_english": "Of the carbon that leaves the farm, how much leaves dissolved in the water rather than as pieces.",
        "value": 0.52, "low": 0.40, "high": 0.60, "dist": "uniform",
        "unit": "fraction of exported carbon",
        "range": "0.40 - 0.60 (assumed)",
        "source": "Khushi's durable_fraction.py (8 Oct 2026), nested structure after Krause-Jensen & Duarte (2016). Registered 13 Oct 2026 (was mislabelled N-16 in the script).",
        "original_region": "Global",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "OK. Central value from the fate script; range assumed. Khushi to confirm the primary source.",
        "owner": "Khushi",
        "verified": '13 Oct 2026: DOC = 52% of macroalgal export confirmed in Krause-Jensen & Duarte 2016. Used only in the wild-forest comparison.'
    },
    "N-18": {
        "parameter": "DOC reaching deep water",
        "plain_english": "Of the dissolved carbon the kelp releases, how much reaches deep water and stays there.",
        "value": 0.24, "low": 0.15, "high": 0.33, "dist": "uniform",
        "unit": "fraction of DOC",
        "range": "0.15 - 0.33",
        "source": "Upper end: Krause-Jensen & Duarte (2016), 33% of DOC exported below the mixed layer, which they call an upper boundary (their Table 1 lists 30%). Central 0.24 from Khushi's durable_fraction.py; no primary source found 13 Oct 2026.",
        "original_region": "Global",
        "type": "Assumed", "transferred": True,
        "how_solid": "WEAK central: unsourced. 0.33 is a published upper boundary. Refractory DOC literature ranges 5-78% (Watanabe et al. 2020; Neves et al. 2025).",
        "owner": "Khushi",
        "verified": "13 Oct 2026: 0.33 upper boundary confirmed; 0.24 unsourced. Type changed to Assumed.",
    },
    "N-19": {
        "parameter": "Channel flushing time",
        "plain_english": "How many days water stays in the D'Entrecasteaux Channel before flowing out.",
        "value": 23.0, "low": 20.0, "high": 26.0, "dist": "uniform",
        "unit": "days",
        "range": "20 (winter, whole channel) - 26 (overall)",
        "source": "CSIRO hydrodynamic model of the D'Entrecasteaux Channel (2003-06).",
        "original_region": "D'Entrecasteaux Channel, Tasmania",
        "type": "Literature-derived", "transferred": False,
        "how_solid": "GOOD - local model. Used only for the dispersion footprint.",
        "owner": "Ramesh",
        "verified": '13 Oct 2026: confirmed, CSIRO (Marine and Freshwater Research MF09134): whole-region flushing ~20-26 days.'
    },
    "N-20": {
        "parameter": "Share of outflow leaving north",
        "plain_english": "Of the water leaving the channel, how much goes north to Storm Bay rather than south.",
        "value": 0.75, "low": 0.60, "high": 0.90, "dist": "uniform",
        "unit": "fraction",
        "range": "0.60 - 0.90 (assumed)",
        "source": "CSIRO D'Entrecasteaux Channel model: most water leaves north into Storm Bay, a smaller share south. Exact split not published; 0.75 assumed.",
        "original_region": "D'Entrecasteaux Channel, Tasmania",
        "type": "Assumed", "transferred": False,
        "how_solid": "ASSUMED split; direction is from the CSIRO model. Display only, does not change the carbon estimate.",
        "owner": "Ramesh",
        "verified": '13 Oct 2026: direction confirmed (predominantly northward, small share south); CSIRO gives no percentage, so 0.75 stays assumed. CSIRO also notes the northern channel connects poorly with the rest.'
    },
    "N-21": {
        "parameter": "Seasonal growth curve",
        "plain_english": "The shape of growth through the season: slow start, fast middle, levelling off.",
        "value": 1.2, "low": None, "high": None, "dist": "fixed",
        "unit": "logistic rate per month (midpoint at mid-season)",
        "range": "n/a",
        "source": "Assumed logistic shape, scaled so end-of-season biomass equals N-10 x N-14. Satellite gives timing only (C-005).",
        "original_region": "n/a",
        "type": "Assumed", "transferred": False,
        "how_solid": "ASSUMED shape. Season totals don't depend on it; only the month-by-month split does.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: assumed shape, no source needed; season totals don't depend on it."
    },
    "N-22": {
        "parameter": "Grow-line length at Tower Bay",
        "plain_english": "How many metres of kelp line were in the water.",
        "value": 360.0, "low": None, "high": None, "dist": "fixed",
        "unit": "metres",
        "range": "unknown",
        "source": "ASSUMED equal to Tinderbox, the sister site in the same IMAS/CRC project: 360 m of grow-line on three 18 m rings and a 60 m array (Blue Economy CRC kelp mariculture page; harvest note 22 Nov 2024).",
        "original_region": "Southeast Tasmania - Tinderbox",
        "type": "Assumed", "transferred": True,
        "how_solid": "ASSUMED. The single biggest unknown. Ask Jeff Wright (IMAS) for the Tower Bay line length and harvest weight; both would replace this and N-15.",
        "owner": "Moniesh",
        "verified": "13 Oct 2026: new. Replaces 'whole 7.9 ha permit area is kelp'.",
    },
    "N-23": {
        "parameter": "Kelp lost from the farm as pieces",
        "plain_english": "Share of what the farm grows that breaks off and drifts away before harvest.",
        "value": 0.13, "low": 0.08, "high": 0.49, "dist": "triangular",
        "unit": "fraction of production",
        "range": "0.08 - 0.49",
        "source": "Fieler et al. (2021) Front. Mar. Sci. 8:632725, farmed Saccharina latissima, Norway: 8-13% of produced dry weight lost by a normal harvest; 49% when harvest was delayed to August.",
        "original_region": "Norway - Saccharina latissima farms",
        "type": "Transferred species", "transferred": True,
        "how_solid": "OK. Measured on real kelp farms, but a different species and region. Tower Bay was harvested in November, later in the season than Biancacci et al. recommend, so losses may sit above the central value.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: new; checked in the paper.",
    },
    "N-24": {
        "parameter": "Carbon released dissolved (DOC)",
        "plain_english": "Share of the carbon the kelp fixes that leaks out dissolved in the water.",
        "value": 0.23, "low": 0.12, "high": 0.29, "dist": "uniform",
        "unit": "fraction of fixed carbon",
        "range": "0.12 - 0.29",
        "source": "Central: Krause-Jensen & Duarte (2016), DOC export 355 of 1,521 TgC/yr NPP (23%). Range: Neves et al. (2025), farmed Saccharina latissima, DOC release 12-29% of fixed carbon (via SINTEF summary).",
        "original_region": "Global; Norway for the farm range",
        "type": "Literature-derived", "transferred": True,
        "how_solid": "OK. Consistent central and farm range, but no Macrocystis farm measurement.",
        "owner": "Khushi",
        "verified": "13 Oct 2026: new; K-J&D figures checked in the paper, Neves et al. via SINTEF summary.",
    },
}

PLACEHOLDERS = {"TO FIND", "TO CONFIRM", "TO COUNT"}
CO2_PER_C = 44.0 / 12.0  # molecular weight ratio, a physical constant


def get_coefficient(coefficient_id: str) -> dict:
    try:
        return COEFFICIENTS[coefficient_id]
    except KeyError as exc:
        raise KeyError(f"Unknown coefficient {coefficient_id!r}. Valid: {sorted(COEFFICIENTS)}") from exc


def get_value(coefficient_id: str):
    value = get_coefficient(coefficient_id)["value"]
    if isinstance(value, str) and value.upper() in PLACEHOLDERS:
        raise ValueError(f"{coefficient_id} is still unresolved: {value!r}")
    return value


def get_range(coefficient_id: str) -> tuple:
    c = get_coefficient(coefficient_id)
    return c["low"], c["high"]


def list_blocking() -> list:
    return [cid for cid, c in COEFFICIENTS.items()
            if isinstance(c["value"], str) and c["value"].upper() in PLACEHOLDERS]


def list_transferred() -> list:
    """Every coefficient taken from another region or species (Sprint 3 task)."""
    return [cid for cid, c in COEFFICIENTS.items() if c["transferred"]]
