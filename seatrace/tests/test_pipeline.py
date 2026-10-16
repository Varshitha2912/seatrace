import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from config.coefficients import COEFFICIENTS, list_blocking, list_transferred  # noqa: E402
from modules.biomass import full_scale_biomass, get_biomass, season_series  # noqa: E402
from modules.carbon import biomass_to_carbon, default_params, fate_split  # noqa: E402
from modules.validation import wild_forest_durable_of_npp  # noqa: E402
from modules.dispersion import footprint  # noqa: E402
from modules.fate import one_at_a_time, scenarios  # noqa: E402
from modules.report import build, to_markdown  # noqa: E402
from modules.uncertainty import run_simulation, stability_check  # noqa: E402


def test_no_placeholders_left():
    assert list_blocking() == []


def test_every_sampled_coefficient_has_a_range_and_source():
    for cid, c in COEFFICIENTS.items():
        assert c["source"], cid
        if c["dist"] != "fixed":
            assert c["low"] is not None and c["high"] is not None and c["low"] <= c["high"], cid


def test_biomass_is_grow_line_based():
    b = get_biomass()
    assert b["wet_biomass_tonnes"] == pytest.approx(3.6)      # 360 m x 10 kg/m (Tinderbox)
    assert b["low_tonnes"] == pytest.approx(0.432)            # 1.2 kg/m (Biancacci 2022)
    assert full_scale_biomass()["wet_biomass_tonnes"] == pytest.approx(94.5)


def test_fate_tree_reproduces_krause_jensen_duarte():
    # paper: 173 of 1,521 TgC/yr sequestered (11.4%); our code with its inputs
    assert wild_forest_durable_of_npp(0.33) == pytest.approx(173 / 1521, abs=0.006)
    assert wild_forest_durable_of_npp(0.33) == pytest.approx(0.43 * 0.244 + 0.004, abs=1e-3)


def test_farm_fate_central():
    f = fate_split(default_params())
    assert f["harvested"] == pytest.approx(0.64)
    assert f["durable"] == pytest.approx(0.0748, abs=1e-4)


def test_100_tonnes_definition_of_done():
    r = biomass_to_carbon(100)
    assert r["durable_t"] < r["exported_t"] < r["carbon_t"]
    assert r["harvested_c_t"] + r["buried_t"] + r["deep_t"] + r["released_t"] == pytest.approx(r["carbon_t"])


def test_losses_cannot_exceed_production():
    with pytest.raises(ValueError):
        biomass_to_carbon(1, {"poc_loss_fraction": 0.6, "doc_release_fraction": 0.5})


def test_season_sums_to_total():
    s = season_series(3.6)
    assert len(s) == 7
    assert sum(x["growth_wet_t"] for x in s) == pytest.approx(3.6)
    assert s[-1]["standing_wet_t"] == pytest.approx(3.6)


def test_monte_carlo_is_reproducible_and_stable():
    a, b = run_simulation(1000, 7), run_simulation(1000, 7)
    assert a["median"] == b["median"]
    assert a["p5"] < a["median"] < a["p95"]
    assert stability_check(5000)["stable"]  # heavy right tail: p95 needs 5000 runs


def test_monte_carlo_refuses_too_few_runs():
    with pytest.raises(ValueError):
        run_simulation(100)


def test_scenarios_and_sensitivity():
    names = [s["name"] for s in scenarios()]
    assert len(names) >= 4
    t = one_at_a_time()
    assert t["rows"][0]["swing"] >= t["rows"][-1]["swing"]


def test_dispersion_decays_along_routes():
    fp = footprint()
    for r in fp["routes"]:
        intact = [p["intact"] for p in r["points"]]
        assert intact[0] == pytest.approx(1.0)
        assert all(x >= y for x, y in zip(intact, intact[1:]))


def test_transferred_are_flagged():
    assert {"N-01", "N-02", "N-07", "N-15", "N-22", "N-23"} <= set(list_transferred())


def test_every_coefficient_has_verification_note():
    assert all(c.get("verified") for c in COEFFICIENTS.values())


def test_report_builds():
    md = to_markdown(build(1000))
    for section in ("## Result", "## Coefficients, sources and verification status", "## Spatial evidence", "## Limitations"):
        assert section in md
