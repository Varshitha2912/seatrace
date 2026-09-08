"""
SeaTrace — Streamlit app shell.

Wires biomass -> carbon -> uncertainty -> map into one page. This is a
transparent, literature-informed prototype estimating carbon in seaweed
aquaculture. It is NOT a certified MRV system - it documents its own
assumptions, uncertainty, and limitations at every step.

Run with:
    streamlit run app.py
"""

import streamlit as st
from streamlit_folium import st_folium

from config.coefficients import COEFFICIENTS, list_blocking
from modules.biomass import get_biomass
from modules.carbon import biomass_to_carbon
from modules.mapping import get_map
from modules.uncertainty import run_simulation

st.set_page_config(page_title="SeaTrace", page_icon="🌊", layout="wide")

st.title("🌊 SeaTrace")
st.caption(
    "A transparent, literature-informed prototype estimating carbon in "
    "seaweed aquaculture. Not a certified MRV system - see assumptions and "
    "limitations below."
)

blocking = list_blocking()
if blocking:
    st.warning(
        f"**{len(blocking)} coefficients are still unresolved:** "
        f"{', '.join(blocking)}. Results below use documented placeholders "
        "for these - see config/coefficients.py and the team's Notion "
        "Blockers database."
    )

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Run the pipeline")
    run_clicked = st.button("Run", type="primary")

    if run_clicked:
        with st.spinner("Estimating biomass..."):
            biomass_result = get_biomass()
        st.success(
            f"Wet biomass estimate: {biomass_result['wet_biomass_tonnes']} "
            f"tonnes ({biomass_result['method']})"
        )
        st.caption(biomass_result["notes"])

        with st.spinner("Converting biomass to carbon..."):
            carbon_result = biomass_to_carbon(biomass_result["wet_biomass_tonnes"])
        st.metric(
            "Estimated durable carbon (tonnes)",
            f"{carbon_result['durable_carbon_tonnes']:.2f}",
        )
        st.caption(f"Total carbon in dry biomass: {carbon_result['total_carbon_tonnes']:.2f} t")
        with st.expander("Assumptions used"):
            st.json(carbon_result["assumptions"])

        with st.spinner("Running uncertainty simulation (200+ runs)..."):
            uncertainty_result = run_simulation(
                n_iterations=200,
                wet_biomass_tonnes=biomass_result["wet_biomass_tonnes"],
            )
        st.write("**Durable carbon range (Monte Carlo, n=200):**")
        u1, u2, u3 = st.columns(3)
        u1.metric("p5", f"{uncertainty_result['p5']:.2f} t")
        u2.metric("median", f"{uncertainty_result['median']:.2f} t")
        u3.metric("p95", f"{uncertainty_result['p95']:.2f} t")
    else:
        st.info("Click **Run** to estimate biomass, carbon, and uncertainty.")

with col2:
    st.subheader("Study site")
    farm_map = get_map()
    st_folium(farm_map, width=None, height=450)

st.markdown("---")
with st.expander("Coefficients used (config/coefficients.py)"):
    for cid, entry in sorted(COEFFICIENTS.items()):
        st.markdown(f"**{cid} — {entry['parameter']}** ({entry['owner']}, {entry['status']})")
        st.caption(entry["plain_english"])
        st.write(f"Value: `{entry['value']}` {entry['unit']} | Range: {entry['range']}")
        st.caption(f"Source: {entry['source']}")
        st.caption(entry["how_solid"])
        st.markdown("&nbsp;")
