"""
Carbon and fate - from harvested kelp to carbon stored long term.

Owner: Khushi. Epics E3 (carbon) and E4 (fate model).

Revised 13 Oct 2026 after source verification. A farm is not a wild forest:
most kelp is harvested and leaves the system, so only what is lost before
harvest can be stored. Losses come from farm measurements (N-23, N-24),
not the wild-forest detritus fraction (N-03, now comparison only).

    harvested wet   W   = line length (N-22) x yield per metre (N-15)
    dry             D   = W x dry matter fraction (N-13)
    harvested C     Ch  = D x carbon content (N-01)
    fixed C         Cf  = Ch / (1 - f_poc - f_doc)
    lost as pieces  POC = Cf x f_poc (N-23)
    released as DOC DOC = Cf x f_doc (N-24)

    POC to deep sea       POC x N-04
    POC buried on shelf   POC x (1 - N-04) x N-05    (Krause-Jensen & Duarte 2016)
    DOC to deep water     DOC x N-18
    everything else lost  released (remineralised, N-06)

Stored long term = deep + buried. Harvested carbon is NOT counted: it is
sold or used, and returns to the atmosphere on short timescales.
"""

from config.coefficients import CO2_PER_C, get_value

PARAM_IDS = {
    "yield_kg_per_m": "N-15",
    "dry_matter_fraction": "N-13",
    "carbon_content_fraction": "N-01",
    "poc_loss_fraction": "N-23",
    "doc_release_fraction": "N-24",
    "doc_deep_fraction": "N-18",
    "poc_deep_fraction": "N-04",
    "poc_burial_fraction": "N-05",
}


def default_params() -> dict:
    """Central values for every model input, read from the register."""
    return {name: float(get_value(cid)) for name, cid in PARAM_IDS.items()}


def harvest_wet_tonnes(p: dict, line_m: float = None) -> float:
    line_m = line_m if line_m is not None else get_value("N-22")
    return line_m * p["yield_kg_per_m"] / 1000.0


def fate_split(p: dict) -> dict:
    """Fates per unit of carbon FIXED by the kelp."""
    poc, doc = p["poc_loss_fraction"], p["doc_release_fraction"]
    poc_deep = poc * p["poc_deep_fraction"]
    buried = poc * (1 - p["poc_deep_fraction"]) * p["poc_burial_fraction"]
    doc_deep = doc * p["doc_deep_fraction"]
    harvested = 1 - poc - doc
    deep = poc_deep + doc_deep
    released = poc + doc - deep - buried
    return {"harvested": harvested, "poc_lost": poc, "doc_released": doc,
            "poc_deep": poc_deep, "doc_deep": doc_deep, "deep": deep,
            "buried": buried, "released": released, "durable": deep + buried}


def biomass_to_carbon(wet_harvest_tonnes: float, coeffs: dict = None) -> dict:
    """Harvested wet kelp (t) -> carbon fixed and its fates (t C).

    `coeffs` overrides any entry of default_params().
    """
    p = default_params()
    p.update(coeffs or {})
    if p["poc_loss_fraction"] + p["doc_release_fraction"] >= 1:
        raise ValueError("Losses must be less than all carbon fixed")

    dry = wet_harvest_tonnes * p["dry_matter_fraction"]
    c_harv = dry * p["carbon_content_fraction"]
    f = fate_split(p)
    c_fix = c_harv / f["harvested"]

    out = {
        "wet_t": wet_harvest_tonnes,
        "dry_t": dry,
        "harvested_c_t": c_harv,
        "carbon_t": c_fix,
        "exported_t": c_fix * (f["poc_lost"] + f["doc_released"]),
        "buried_t": c_fix * f["buried"],
        "deep_t": c_fix * f["deep"],
        "released_t": c_fix * f["released"],
        "durable_t": c_fix * f["durable"],
        "durable_co2_t": c_fix * f["durable"] * CO2_PER_C,
        "fractions": f,
        "params": p,
    }
    out["retained_t"] = c_harv
    out["total_carbon_tonnes"] = c_fix
    out["durable_carbon_tonnes"] = out["durable_t"]
    assert out["durable_t"] <= out["exported_t"] <= c_fix
    assert abs(c_harv + out["buried_t"] + out["deep_t"] + out["released_t"] - c_fix) < 1e-9
    return out

