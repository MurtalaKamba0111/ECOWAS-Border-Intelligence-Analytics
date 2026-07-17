# ============================================================
# Trade Analytics
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Trade Analytics",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():

    return pd.read_csv(
        Path("data") / "trade_diversion_transactions.csv"
    )

df = load_data()

st.title("📈 Trade Analytics")

st.caption(
    "Comprehensive analysis of regional trade flows."
)

st.markdown("---")

# ============================================================
# Commodity Analysis
# ============================================================

commodity_summary = (
    df.groupby("Commodity")["Trade_Value_USD"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(

    commodity_summary,

    x="Commodity",

    y="Trade_Value_USD",

    color="Trade_Value_USD",

    title="Trade Value by Commodity"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# Vehicle Type Analysis
# ============================================================

vehicle_summary = (
    df.groupby("Vehicle_Type")["Trade_Value_USD"]
    .sum()
    .reset_index()
)

fig2 = px.pie(

    vehicle_summary,

    names="Vehicle_Type",

    values="Trade_Value_USD",

    hole=0.45,

    title="Trade Value by Vehicle Type"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ============================================================
# Entry Country Analysis
# ============================================================

st.markdown("---")

country_summary = (
    df.groupby("Entry_Country")["Trade_Value_USD"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig3 = px.bar(

    country_summary,

    x="Entry_Country",

    y="Trade_Value_USD",

    color="Trade_Value_USD",

    title="Trade Value by Entry Country"

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ============================================================
# Monthly Trade Trend
# ============================================================

st.markdown("---")

monthly_trade = (
    df.groupby("Period")["Trade_Value_USD"]
    .sum()
    .reset_index()
)

fig4 = px.line(

    monthly_trade,

    x="Period",

    y="Trade_Value_USD",

    markers=True,

    title="Monthly Trade Trend"

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ============================================================
# Top 10 Commodities by Revenue
# ============================================================

st.markdown("---")

commodity_revenue = (
    df.groupby("Commodity")["Revenue_Collected_USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(

    commodity_revenue,

    x="Revenue_Collected_USD",

    y="Commodity",

    orientation="h",

    color="Revenue_Collected_USD",

    title="Top 10 Commodities by Revenue"

)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ============================================================
# Average Processing Time by Border Post
# ============================================================

st.markdown("---")

processing_summary = (
    df.groupby("Border_Post")["Processing_Time_Minutes"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig6 = px.bar(

    processing_summary,

    x="Border_Post",

    y="Processing_Time_Minutes",

    color="Processing_Time_Minutes",

    title="Average Processing Time by Border Post"

)

st.plotly_chart(
    fig6,
    use_container_width=True
)