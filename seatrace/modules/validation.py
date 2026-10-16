"""
Validation - compare SeaTrace with published figures and similar sites.

Owner: Shraddha. Sprint 5. Revised 13 Oct 2026 after source verification.

Nobody has measured where this farm's carbon went, so these checks test
plausibility and internal consistency. Reference values below are published
figures used only for comparison (they are not model inputs).
"""

from config.coefficients import get_value
from modules.biomass import full_scale_biomass, get_biomass
from modules.carbon import biomass_to_carbon, default_params

# Published reference points, all checked 13 Oct 2026
KJD_EXPORT_OF_NPP = 0.43           # Krause-Jensen & Duarte 2016: 43% of macroalgal NPP exported
KJD_BED_BURIAL_OF_NPP = 0.004      # ... 0.4% of NPP buried in the habitat
KJD_SEQUESTERED_OF_NPP = 173 / 1521  # 173 of 1,521 TgC/yr
KJD_DOC_DEEP_UPPER = 0.33
TINDERBOX_WET_T = 3.6               # Blue Economy CRC, Nov 2024
BIANCACCI_KG_PER_M = 1.2            # Biancacci et al. 2022, Tasmanian farmed Macrocystis
FIELER_LOSS = (0.08, 0.13)          # Fieler et al. 2021, normal-harvest losses
DUARTE2025_FARM_BURIAL_CO2_HA = 1.06   # Duarte et al. 2025 Nat Clim Change: burial attributable to farms
FALKLANDS_WILD_CO2_HA = 3.6         # Bayley et al. 2017: 0.065 TgC/yr over ~664 km2 of wild Macrocystis


def wild_forest_durable_of_npp(doc_deep: float) -> float:
    """Krause-Jensen & Duarte fate tree applied to NPP, as published."""
    doc = get_value("N-17")
    per_export = (doc * doc_deep + (1 - doc) * get_value("N-04")
                  + (1 - doc) * (1 - get_value("N-04")) * get_value("N-05"))
    return KJD_EXPORT_OF_NPP * per_export + KJD_BED_BURIAL_OF_NPP


def checks() -> list:
    b = get_biomass()
    r = biomass_to_carbon(b["wet_biomass_tonnes"])
    f = r["fractions"]
    fs = full_scale_biomass()
    rf = biomass_to_carbon(fs["wet_biomass_tonnes"])
    area = get_value("N-10")
    kjd_reproduced = wild_forest_durable_of_npp(KJD_DOC_DEEP_UPPER)

    return [
        {
            "check": "Fate tree reproduces the published global budget",
            "ours": kjd_reproduced, "published": KJD_SEQUESTERED_OF_NPP, "unit": "share",
            "source": "Krause-Jensen & Duarte (2016), Nature Geoscience: 173 of 1,521 TgC/yr of macroalgal NPP sequestered",
            "verdict": "match" if abs(kjd_reproduced - KJD_SEQUESTERED_OF_NPP) < 0.006 else "differs",
            "explanation": "Run with the paper's own inputs, our fate code gives 10.9% against the paper's 11.4%. The half-point gap comes from the paper rounding and listing 30% and 33% for the same DOC step, so the structure is coded correctly.",
        },
        {
            "check": "Share of fixed carbon stored, farm vs wild forest",
            "ours": f["durable"], "published": KJD_SEQUESTERED_OF_NPP, "unit": "share",
            "source": "Krause-Jensen & Duarte (2016) for wild forests; Duarte et al. (2017) note the share is likely smaller for farms because the crop is harvested",
            "verdict": "lower, as expected",
            "explanation": "We store about 7.5% of the carbon the kelp fixes, versus about 11% in wild forests. The difference is the harvest: about 64% of fixed carbon is taken away and sold.",
        },
        {
            "check": "Kelp grown, compared with the sister site",
            "ours": b["wet_biomass_tonnes"], "published": TINDERBOX_WET_T, "unit": "t",
            "source": "Blue Economy CRC (Nov 2024): ~3.6 t grown at Tinderbox on 360 m of line; Biancacci et al. (2022): 1.2 kg/m at other Tasmanian farms",
            "verdict": "assumed equal",
            "explanation": "Tower Bay is assumed to match Tinderbox. Nothing public gives the Tower Bay line length or harvest weight, so this check is circular until IMAS supplies them.",
        },
        {
            "check": "Kelp lost before harvest",
            "ours": get_value("N-23"), "published": FIELER_LOSS[1], "unit": "share",
            "source": "Fieler et al. (2021), farmed Saccharina in Norway: 8-13% lost by a normal harvest, 49% when delayed",
            "verdict": "transferred",
            "explanation": "Central value is taken from this study, so it matches by construction. The check is that it is a farm measurement, unlike the 71% wild-forest figure used before.",
        },
        {
            "check": "Full-scale farm: CO2 stored per hectare",
            "ours": rf["durable_co2_t"] / area, "published": DUARTE2025_FARM_BURIAL_CO2_HA, "unit": "t CO2/ha",
            "source": "Duarte et al. (2025), Nature Climate Change: sediment burial attributable to 20 seaweed farms averaged 1.06 t CO2e/ha/yr; Bayley et al. (2017): wild Falklands giant kelp ~3.6 t CO2/ha/yr",
            "verdict": "lower",
            "explanation": "Even if the whole site were farmed, we estimate well under the 20-farm average. Wild-forest density (12 t/ha) is low for a farm, and our share buried on a sandy channel floor is small.",
        },
        {
            "check": "Share of lost carbon released again",
            "ours": f["released"] / (f["poc_lost"] + f["doc_released"]), "published": 0.90, "unit": "share",
            "source": "N-06 cross-check: deep-ocean monitoring and lab studies report more than 90% remineralisation",
            "verdict": "disagrees",
            "explanation": "About 79% of the carbon lost before harvest is released again, against more than 90% from monitoring. If monitoring is right, stored carbon is roughly half our central value.",
        },
    ]
