# ============================================================
# Executive Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# Load Data
# ============================================================

@st.cache_data
def load_data():

    data_folder = Path("data")
    output_folder = Path("outputs")

    df = pd.read_csv(
        data_folder / "trade_diversion_transactions.csv"
    )

    scorecard = pd.read_csv(
        output_folder / "border_performance_scorecard.csv"
    )

    return df, scorecard

df, scorecard = load_data()

# ============================================================
# Dashboard Header
# ============================================================

st.title("📊 Executive Dashboard")

st.caption(
    "Real-time monitoring of ECOWAS regional border operations."
)

st.markdown("---")


# ============================================================
# Sidebar Filters
# ============================================================

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Entry Country",
    ["All"] + sorted(df["Entry_Country"].unique())
)

border = st.sidebar.selectbox(
    "Border Post",
    ["All"] + sorted(df["Border_Post"].unique())
)

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["Entry_Country"] == country
    ]

if border != "All":
    filtered_df = filtered_df[
        filtered_df["Border_Post"] == border
    ]

    # ============================================================
    # Executive KPIs
    # ============================================================

    total_transactions = len(filtered_df)

    total_trade = filtered_df["Trade_Value_USD"].sum()

    total_revenue = filtered_df["Revenue_Collected_USD"].sum()

    avg_processing = filtered_df["Processing_Time_Minutes"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col2.metric(
        "Trade Value (USD)",
        f"${total_trade:,.0f}"
    )

    col3.metric(
        "Revenue (USD)",
        f"${total_revenue:,.0f}"
    )

    col4.metric(
        "Avg Processing Time",
        f"{avg_processing:.1f} min"
    )

    st.markdown("---")

    # ============================================================
    # Trade Value by Entry Country
    # ============================================================

    trade_summary = (
        filtered_df
        .groupby("Entry_Country")["Trade_Value_USD"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        trade_summary,
        x="Entry_Country",
        y="Trade_Value_USD",
        color="Trade_Value_USD",
        text_auto=".2s",
        title="Trade Value by Entry Country"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # Revenue Distribution
    # ============================================================

    revenue_summary = (
        filtered_df
        .groupby("Entry_Country")["Revenue_Collected_USD"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        revenue_summary,
        names="Entry_Country",
        values="Revenue_Collected_USD",
        hole=0.45,
        title="Revenue Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ============================================================
    # Monthly Trade Trend
    # ============================================================

    st.markdown("---")

    monthly_trade = (
        filtered_df
        .groupby("Period")["Trade_Value_USD"]
        .sum()
        .reset_index()
    )

    fig3 = px.line(
        monthly_trade,
        x="Period",
        y="Trade_Value_USD",
        markers=True,
        title="Monthly Trade Value Trend"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ============================================================
    # Top 10 Busiest Border Posts
    # ============================================================

    st.markdown("---")

    border_summary = (
        filtered_df
        .groupby("Border_Post")["Trade_Value_USD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        border_summary,
        x="Trade_Value_USD",
        y="Border_Post",
        orientation="h",
        color="Trade_Value_USD",
        title="Top 10 Busiest Border Posts"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # ============================================================
    # High-Risk Transactions
    # ============================================================

    st.markdown("---")

    st.subheader("🚨 Top 10 Highest-Risk Transactions")

    top_risk = (
        filtered_df
        .sort_values("Smuggling_Risk", ascending=False)
        .head(10)
    )

    st.dataframe(
        top_risk[
            [
                "Transaction_ID",
                "Border_Post",
                "Entry_Country",
                "Commodity",
                "Trade_Value_USD",
                "Smuggling_Risk"
            ]
        ],
        use_container_width=True
    )

    # ============================================================
    # Executive Summary
    # ============================================================

    st.markdown("---")

    st.subheader("📋 Executive Summary")

    highest_border = (
        border_summary.iloc[0]["Border_Post"]
    )

    highest_trade = (
        border_summary.iloc[0]["Trade_Value_USD"]
    )

    st.info(
        f"""
    • Total Transactions Analysed: **{total_transactions:,}**

    • Total Trade Value: **${total_trade:,.0f}**

    • Total Revenue Collected: **${total_revenue:,.0f}**

    • Highest Trade Border: **{highest_border}**

    • Trade Value at Highest Border: **${highest_trade:,.0f}**
    """
    )

