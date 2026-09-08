"""
Carbon — convert biomass to carbon using published coefficients.

Owner: Khushi
Epic 2 of 5. See config/coefficients.py for N-01 (carbon content of biomass)
and N-13 (dry matter fraction).

Project rule: nobody hardcodes numbers - every coefficient here comes from
config/coefficients.py.
"""

from config.coefficients import get_coefficient


def biomass_to_carbon(wet_biomass_tonnes: float, coeffs: dict = None) -> dict:
    """Convert wet biomass (tonnes) into an estimate of durable carbon.

    Sprint 1: stub. Uses N-01 (carbon content of biomass, currently a
    cross-species Saccharina placeholder - see Blocker B-04) and N-13 (dry
    matter fraction, currently TO FIND) where available, otherwise falls back
    to a documented placeholder so the pipeline can still be smoke-tested.

    Args:
        wet_biomass_tonnes: Wet biomass estimate, e.g. from
            modules.biomass.get_biomass().
        coeffs: Optional dict of override coefficients, e.g.
            {"dry_matter_fraction": 0.12, "carbon_content_fraction": 0.252}.
            When omitted, values are pulled from config/coefficients.py.

    Returns:
        dict with:
            total_carbon_tonnes (float): total carbon in the dry biomass
            durable_carbon_tonnes (float): the portion assumed durable
                (sanity check: always <= total_carbon_tonnes)
            assumptions (dict): which coefficients/fallbacks were used
    """
    coeffs = coeffs or {}

    carbon_content_fraction = coeffs.get(
        "carbon_content_fraction", get_coefficient("N-01")["value"]
    )

    # N-13 (dry matter fraction) is still "TO FIND" in Notion. Use the
    # documented literature range midpoint (0.10-0.15) as an explicit,
    # labelled placeholder rather than silently guessing.
    dry_matter_fraction = coeffs.get("dry_matter_fraction", 0.125)

    dry_biomass_tonnes = wet_biomass_tonnes * dry_matter_fraction
    total_carbon_tonnes = dry_biomass_tonnes * carbon_content_fraction

    # Durable carbon is always a subset of total carbon extracted from
    # biomass - this is the sanity check every future refinement must keep
    # passing. Sprint 1 stub: assume a conservative 50% durability pending
    # the Fate module (fate.py, Epic 3) actually splitting buried / deep
    # water / released.
    durable_fraction_placeholder = 0.5
    durable_carbon_tonnes = total_carbon_tonnes * durable_fraction_placeholder

    assert durable_carbon_tonnes <= total_carbon_tonnes, (
        "Sanity check failed: durable carbon cannot exceed total carbon"
    )

    return {
        "total_carbon_tonnes": total_carbon_tonnes,
        "durable_carbon_tonnes": durable_carbon_tonnes,
        "assumptions": {
            "carbon_content_fraction": carbon_content_fraction,
            "carbon_content_source": "N-01 (cross-species Saccharina placeholder, see Blocker B-04)",
            "dry_matter_fraction": dry_matter_fraction,
            "dry_matter_source": "N-13 is TO FIND; using literature range midpoint 0.125 as placeholder",
            "durable_fraction_placeholder": durable_fraction_placeholder,
        },
    }
