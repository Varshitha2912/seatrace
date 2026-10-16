"""
Build web/credit_check.html: the buyer-facing credit check prototype.

    python scripts/build_buyer.py

Uses the same coefficient register and model as the SeaTrace app, plus the
late-harvest loss range from Fieler et al. (2021): 49.4% lost when harvest was
delayed to August (95% CI 34.4-70.8%), capped at 0.65 so total losses stay
below 100% of production.
"""

import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from config.coefficients import COEFFICIENTS, CO2_PER_C  # noqa: E402
from modules.carbon import PARAM_IDS  # noqa: E402

LATE_HARVEST_LOSS = {"low": 0.344, "mode": 0.494, "high": 0.65}


def main():
    data = {
        "generated": dt.date.today().isoformat(),
        "co2PerC": CO2_PER_C,
        "coef": {cid: {k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()} for cid, c in COEFFICIENTS.items()},
        "paramIds": PARAM_IDS,
        "late": LATE_HARVEST_LOSS,
    }
    web = os.path.join(ROOT, "web")
    tpl = open(os.path.join(web, "template.html")).read()
    style = tpl[tpl.index('<link rel="preconnect"'):tpl.index("</style>")]
    body = open(os.path.join(web, "buyer_body.html")).read()
    out = "<title>SeaTrace Credit Check</title>\n" + style + body.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    path = os.path.join(web, "credit_check.html")
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path, f"{len(out) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
