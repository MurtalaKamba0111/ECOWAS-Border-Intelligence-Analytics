# ============================================================
# ECOWAS Border Intelligence Analytics Platform
# Risk Intelligence Dashboard
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
    page_title="Risk Intelligence",
    page_icon="🚨",
    layout="wide"
)

# ============================================================
# Chapter 3 - Load Dataset
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        Path("data") / "trade_diversion_transactions.csv"
    )

df = load_data()

# ============================================================
# Chapter 4 - Dashboard Header
# ============================================================

st.title("🚨 Risk Intelligence Dashboard")

st.caption(
    "Monitoring high-risk border transactions across ECOWAS."
)

st.markdown("---")

# ============================================================
# Chapter 5 - Risk KPI Cards
# ============================================================

risk_summary = (
    df["Smuggling_Risk"]
    .value_counts()
)

high = risk_summary.get("High", 0)
medium = risk_summary.get("Medium", 0)
low = risk_summary.get("Low", 0)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "High Risk",
    f"{high:,}"
)

col2.metric(
    "Medium Risk",
    f"{medium:,}"
)

col3.metric(
    "Low Risk",
    f"{low:,}"
)

col4.metric(
    "Total Transactions",
    f"{len(df):,}"
)

# ============================================================
# Chapter 6 - Risk Distribution
# ============================================================

st.markdown("---")

st.subheader("Risk Distribution")

risk_distribution = (
    df["Smuggling_Risk"]
    .value_counts()
    .reset_index()
)

risk_distribution.columns = [
    "Risk_Level",
    "Transactions"
]

fig1 = px.pie(
    risk_distribution,
    names="Risk_Level",
    values="Transactions",
    hole=0.45,
    title="Distribution of Smuggling Risk"
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="risk_distribution"
)

# ============================================================
# Chapter 7 - High-Risk Border Ranking
# ============================================================

st.markdown("---")

st.subheader("High-Risk Border Posts")

high_risk = df[
    df["Smuggling_Risk"] == "High"
]

border_risk = (
    high_risk
    .groupby("Border_Post")
    .size()
    .reset_index(name="High_Risk_Transactions")
    .sort_values(
        by="High_Risk_Transactions",
        ascending=False
    )
)

fig2 = px.bar(
    border_risk,
    x="Border_Post",
    y="High_Risk_Transactions",
    color="High_Risk_Transactions",
    title="High-Risk Transactions by Border Post"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="border_risk"
)

# ============================================================
# Chapter 8 - High-Risk Commodity Ranking
# ============================================================

st.markdown("---")

st.subheader("High-Risk Commodities")

commodity_risk = (
    high_risk
    .groupby("Commodity")
    .size()
    .reset_index(name="High_Risk_Transactions")
    .sort_values(
        by="High_Risk_Transactions",
        ascending=False
    )
)

fig3 = px.bar(
    commodity_risk,
    x="Commodity",
    y="High_Risk_Transactions",
    color="High_Risk_Transactions",
    title="High-Risk Commodities"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="commodity_risk"
)

# ============================================================
# Chapter 9 - High-Risk Vehicle Analysis
# ============================================================

st.markdown("---")

st.subheader("High-Risk Vehicle Types")

vehicle_risk = (
    high_risk
    .groupby("Vehicle_Type")
    .size()
    .reset_index(name="High_Risk_Transactions")
)

fig4 = px.pie(
    vehicle_risk,
    names="Vehicle_Type",
    values="High_Risk_Transactions",
    hole=0.45,
    title="High-Risk Transactions by Vehicle Type"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="vehicle_risk"
)

# ============================================================
# Chapter 10 - High-Risk Entry Country Ranking
# ============================================================

st.markdown("---")

st.subheader("High-Risk Entry Countries")

country_risk = (
    high_risk
    .groupby("Entry_Country")
    .size()
    .reset_index(name="High_Risk_Transactions")
    .sort_values(
        by="High_Risk_Transactions",
        ascending=False
    )
)

fig5 = px.bar(
    country_risk,
    x="Entry_Country",
    y="High_Risk_Transactions",
    color="High_Risk_Transactions",
    title="High-Risk Transactions by Entry Country"
)

st.plotly_chart(
    fig5,
    use_container_width=True,
    key="country_risk"
)

# ============================================================
# Chapter 11 - Top High-Risk Transactions
# ============================================================

st.markdown("---")

st.subheader("Top High-Risk Transactions")

st.dataframe(

    high_risk[

        [

            "Transaction_ID",

            "Transaction_Date",

            "Entry_Country",

            "Border_Post",

            "Commodity",

            "Vehicle_Type",

            "Trade_Value_USD",

            "Revenue_Collected_USD",

            "Inspection_Result"

        ]

    ],

    use_container_width=True,

    hide_index=True

)

# ============================================================
# Chapter 12 - Executive Risk Summary
# ============================================================

st.markdown("---")

highest_border = (
    border_risk.iloc[0]["Border_Post"]
)

highest_country = (
    country_risk.iloc[0]["Entry_Country"]
)

highest_commodity = (
    commodity_risk.iloc[0]["Commodity"]
)

st.success(f"""

## Executive Risk Summary

**Highest-Risk Border Post:** {highest_border}

**Highest-Risk Entry Country:** {highest_country}

**Highest-Risk Commodity:** {highest_commodity}

**Total High-Risk Transactions:** {len(high_risk):,}

**Recommendation:** Increase inspections, deploy additional officers,
and strengthen intelligence-led operations at identified high-risk
border locations.

""")

