# ============================================================
# ECOWAS Border Intelligence Analytics Platform (EBIAP)
# Home Page
# ============================================================

import streamlit as st

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="ECOWAS Border Intelligence Analytics Platform",
    page_icon="🌍",
    layout="wide"
)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title("🌍 ECOWAS Border Intelligence Analytics Platform (EBIAP)")

st.subheader(
    "Impact Assessment of Simulated Regional Trade Diversion "
    "Following the AES Countries' Withdrawal from ECOWAS"
)

st.markdown("---")

# ------------------------------------------------------------
# Welcome
# ------------------------------------------------------------

st.header("Welcome")

st.write(
    """
This application demonstrates how data analytics, business intelligence,
geospatial analysis and forecasting can support evidence-based decision
making for ECOWAS regional border management.

Use the navigation menu on the left to explore the different dashboards.
"""
)

# ------------------------------------------------------------
# Project Highlights
# ------------------------------------------------------------

st.markdown("## Project Highlights")

col1, col2 = st.columns(2)

with col1:
    st.success("✔ Executive Dashboard")
    st.success("✔ Trade Analytics")
    st.success("✔ Risk Intelligence")
    st.success("✔ Geospatial Analytics")

with col2:
    st.success("✔ Forecasting")
    st.success("✔ Performance Scorecard")
    st.success("✔ Download Centre")
    st.success("✔ About the Project")

st.markdown("---")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.info(
    "Developed as a Data Analytics & Business Intelligence Portfolio "
    "Project using Python, Streamlit and Plotly."
)