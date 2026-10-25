"""
SeaTrace - Streamlit app.

    streamlit run app.py

A transparent, literature-based estimate of durable carbon from the Tower Bay
kelp trial. Not a certified MRV system: every assumption and range is shown.
"""

import json

import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from config.coefficients import COEFFICIENTS
from modules.mapping import get_map
from modules.report import build, to_markdown

st.set_page_config(page_title="SeaTrace", page_icon="🌊", layout="wide")


@st.cache_data
def get_report(n, seed):
    return build(n, seed)


st.title("SeaTrace")
st.caption("How much carbon did the Tower Bay kelp trial lock away, and where did it go? "
           "A literature-based estimate with the working shown. Not a certified MRV statement.")

with st.sidebar:
    n = st.select_slider("Monte Carlo runs", [2000, 5000, 10000], value=5000)
    seed = st.number_input("Random seed", value=41, step=1)

r = get_report(n, int(seed))
h = r["headline"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("CO2 stored long term, median", f"{h['durable_co2_median_t']*1000:.0f} kg")
c2.metric("90% range", f"{h['durable_co2_p5_t']*1000:.0f} - {h['durable_co2_p95_t']*1000:.0f} kg")
c3.metric("Creditable (5th percentile)", f"{h['durable_co2_p5_t']*1000:.0f} kg", help="The 5th percentile of the Monte Carlo runs: 95% of runs store at least this much. Following expert advice (Prof J. Rhodes, QUT, 22 Oct 2026), a credit claim should rest on this conservative figure, not the median.")
c4.metric("Kelp line in trial", f"{r['farm']['line_m']:.0f} m", help=f"Trial season: {r['farm']['season']}")
st.info("In plain terms: a research-sized trial stores a few tens of kilograms of CO2. Most of the carbon the kelp "
        "absorbed left in the harvest, and most of what broke off rotted and was released again. "
        "Not a certified carbon removal claim.")

tabs = st.tabs(["Map", "Where carbon goes", "Uncertainty", "Sensitivity", "Validation", "Coefficients", "Report"])

with tabs[0]:
    st_folium(get_map(), width=None, height=520)
    d = r["dispersion"]
    st.caption(f"Water leaves the channel in about {d['flushing_days']:.0f} days, {d['north_share']:.0%} to the north. "
               f"{d['intact_at_exit']:.0%} of detritus is still intact on leaving (range "
               f"{d['intact_at_exit_range'][0]:.0%} to {d['intact_at_exit_range'][1]:.0%}).")

with tabs[1]:
    p = r["point_estimate"]
    st.bar_chart(pd.DataFrame({"kg C": [1000 * p["harvested_c_t"], 1000 * p["released_t"], 1000 * p["deep_t"], 1000 * p["buried_t"]]},
                              index=["Harvested", "Released", "Deep water", "Buried"]))
    st.subheader("Through the season")
    st.dataframe(pd.DataFrame(r["season"]), hide_index=True)

with tabs[2]:
    st.dataframe(pd.DataFrame(r["stages"])[["label", "p5", "median", "p95", "unit"]], hide_index=True)

with tabs[3]:
    st.dataframe(pd.DataFrame(r["scenarios"])[["name", "durable_fraction", "durable_co2_t", "change_vs_central", "why"]], hide_index=True)
    st.dataframe(pd.DataFrame(r["sensitivity"]["rows"])[["label", "co2_at_low", "co2_at_high", "swing"]], hide_index=True)

with tabs[4]:
    for c in r["validation"]:
        st.markdown(f"**{c['check']}** ({c['verdict']}): {c['explanation']}  \n_Source: {c['source']}_")

with tabs[5]:
    for cid, c in COEFFICIENTS.items():
        flag = " · transferred" if c["transferred"] else ""
        with st.expander(f"{cid} {c['parameter']} ({c['type']}{flag})"):
            st.write(c["plain_english"])
            st.write(f"Value: {c['value']} {c['unit']} | Range: {c['range']}")
            st.caption(f"Source: {c['source']}")
            st.caption(c["how_solid"])

with tabs[6]:
    md = to_markdown(r)
    st.download_button("Download report (Markdown)", md, "seatrace_report.md")
    st.download_button("Download data (JSON)", json.dumps(r, default=str, indent=2), "seatrace_report.json")
    st.markdown(md)
