# ============================================================
# ECOWAS Border Intelligence Analytics Platform
# Geospatial Analytics
# ============================================================

# ============================================================
# Chapter 1 - Import Libraries
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# Chapter 2 - Page Configuration
# ============================================================

st.set_page_config(
    page_title="Geospatial Analytics",
    page_icon="🌍",
    layout="wide"
)

# ============================================================
# Chapter 3 - Load Data
# ============================================================

@st.cache_data
def load_data():

    transactions = pd.read_csv(
        Path("data") / "trade_diversion_transactions.csv"
    )

    locations = pd.read_csv(
        Path("data") / "border_locations.csv"
    )

    df = transactions.merge(
        locations,
        on="Border_Post",
        how="left"
    )

    return df

df = load_data()

# ============================================================
# Chapter 4 - Dashboard Header
# ============================================================

st.title("🌍 Geospatial Analytics")

st.caption(
    "Spatial analysis of ECOWAS border activities."
)

st.markdown("---")

# ============================================================
# Chapter 5 - Border Location Preview
# ============================================================

st.subheader("Border Location Dataset")

st.dataframe(
    df.head(),
    use_container_width=True
)


# ============================================================
# Chapter 6 - Interactive Border Map
# ============================================================

st.markdown("---")

st.subheader("ECOWAS Border Map")

border_summary = (
    df.groupby(
        ["Border_Post", "Latitude", "Longitude", "Entry_Country"],
        as_index=False
    )["Trade_Value_USD"]
    .sum()
)

fig = px.scatter_map(
    border_summary,
    lat="Latitude",
    lon="Longitude",
    size="Trade_Value_USD",
    color="Entry_Country",
    hover_name="Border_Post",
    hover_data={
        "Trade_Value_USD": ":,.0f",
        "Latitude": False,
        "Longitude": False
    },
    zoom=4,
    height=650,
    title="Trade Value Across ECOWAS Border Posts"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="ecowas_map"
)

# ============================================================
# Chapter 7 - High-Risk Border Map
# ============================================================

st.markdown("---")

st.subheader("High-Risk Border Locations")

high_risk = df[
    df["Smuggling_Risk"] == "High"
]

high_risk_map = (
    high_risk.groupby(
        ["Border_Post", "Latitude", "Longitude"],
        as_index=False
    )
    .size()
)

high_risk_map.rename(
    columns={"size": "High_Risk_Transactions"},
    inplace=True
)

fig2 = px.scatter_map(
    high_risk_map,
    lat="Latitude",
    lon="Longitude",
    size="High_Risk_Transactions",
    color="High_Risk_Transactions",
    hover_name="Border_Post",
    zoom=4,
    height=650,
    title="High-Risk Border Locations"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="high_risk_map"
)

# ============================================================
# Chapter 8 - Trade Value by Border
# ============================================================

st.markdown("---")

st.subheader("Top 15 Border Posts by Trade Value")

border_trade = (
    df.groupby("Border_Post")["Trade_Value_USD"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig3 = px.bar(
    border_trade,
    x="Trade_Value_USD",
    y="Border_Post",
    orientation="h",
    color="Trade_Value_USD",
    title="Top 15 Border Posts by Trade Value"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="border_trade"
)

# ============================================================
# Chapter 9 - High-Risk Border Table
# ============================================================

st.markdown("---")

st.subheader("High-Risk Border Locations")

high_risk = df[df["Smuggling_Risk"] == "High"]

st.dataframe(

    high_risk[
        [
            "Border_Post",
            "Entry_Country",
            "Commodity",
            "Trade_Value_USD",
            "Smuggling_Risk"
        ]
    ],

    use_container_width=True,
    hide_index=True

)

# ============================================================
# Chapter 10 - Executive Geospatial Summary
# ============================================================

st.markdown("---")

highest_border = border_trade.iloc[0]["Border_Post"]
highest_trade = border_trade.iloc[0]["Trade_Value_USD"]

st.success(f"""

## Executive Geospatial Summary

**Highest Trade Border:** {highest_border}

**Trade Value:** ${highest_trade:,.0f}

**High-Risk Transactions:** {len(high_risk):,}

**Recommendation:**
Increase surveillance and intelligence-led border operations at the identified high-volume border posts.

""")

# ============================================================
# Chapter 11 - Download Border Summary
# ============================================================

st.markdown("---")

st.subheader("Download Border Summary")

csv = border_trade.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Border Trade Summary",
    data=csv,
    file_name="border_trade_summary.csv",
    mime="text/csv"
)