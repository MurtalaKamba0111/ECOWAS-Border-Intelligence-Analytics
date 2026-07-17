# ============================================================
# ECOWAS Border Intelligence Analytics Platform
# Forecast Analytics
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
    page_title="Forecast Analytics",
    page_icon="📈",
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

st.title("📈 Forecast Analytics")

st.caption(
    "Forecasting regional trade, revenue and border performance."
)

st.markdown("---")

# ============================================================
# Chapter 5 - Forecast KPI Cards
# ============================================================

total_trade = df["Trade_Value_USD"].sum()

total_revenue = df["Revenue_Collected_USD"].sum()

average_queue = df["Queue_Length"].mean()

average_processing = df["Processing_Time_Minutes"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Trade",
    f"${total_trade:,.0f}"
)

col2.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

col3.metric(
    "Average Queue",
    f"{average_queue:.1f}"
)

col4.metric(
    "Average Processing Time",
    f"{average_processing:.1f} min"
)

# ============================================================
# Chapter 6 - Monthly Trade Trend
# ============================================================

st.markdown("---")

st.subheader("Monthly Trade Trend")

trade_monthly = (
    df.groupby("Period")["Trade_Value_USD"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    trade_monthly,
    x="Period",
    y="Trade_Value_USD",
    markers=True,
    title="Monthly Trade Value"
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="monthly_trade"
)

# ============================================================
# Chapter 7 - Monthly Revenue Trend
# ============================================================

st.markdown("---")

st.subheader("Monthly Revenue Trend")

revenue_monthly = (
    df.groupby("Period")["Revenue_Collected_USD"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    revenue_monthly,
    x="Period",
    y="Revenue_Collected_USD",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="monthly_revenue"
)

# ============================================================
# Chapter 8 - Monthly Cargo Trend
# ============================================================

st.markdown("---")

st.subheader("Monthly Cargo Volume")

cargo_monthly = (
    df.groupby("Period")["Cargo_Weight_kg"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    cargo_monthly,
    x="Period",
    y="Cargo_Weight_kg",
    markers=True,
    title="Monthly Cargo Volume"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="monthly_cargo"
)

# ============================================================
# Chapter 9 - Queue Length Trend
# ============================================================

st.markdown("---")

st.subheader("Monthly Queue Length")

queue_monthly = (
    df.groupby("Period")["Queue_Length"]
    .mean()
    .reset_index()
)

fig4 = px.line(
    queue_monthly,
    x="Period",
    y="Queue_Length",
    markers=True,
    title="Average Queue Length"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="queue_length"
)

# ============================================================
# Chapter 10 - Processing Time Trend
# ============================================================

st.markdown("---")

st.subheader("Average Processing Time")

processing_monthly = (
    df.groupby("Period")["Processing_Time_Minutes"]
    .mean()
    .reset_index()
)

fig5 = px.line(
    processing_monthly,
    x="Period",
    y="Processing_Time_Minutes",
    markers=True,
    title="Average Processing Time"
)

st.plotly_chart(
    fig5,
    use_container_width=True,
    key="processing_time"
)

# ============================================================
# Chapter 11 - Simple Trade Forecast
# ============================================================

st.markdown("---")

st.subheader("Trade Forecast")

forecast = trade_monthly.copy()

forecast["Forecast"] = (
    forecast["Trade_Value_USD"]
    .rolling(3, min_periods=1)
    .mean()
)

fig6 = px.line(
    forecast,
    x="Period",
    y=[
        "Trade_Value_USD",
        "Forecast"
    ],
    markers=True,
    title="Actual vs Forecast Trade Value"
)

st.plotly_chart(
    fig6,
    use_container_width=True,
    key="forecast_trade"
)

# ============================================================
# Chapter 12 - Executive Forecast Summary
# ============================================================

st.markdown("---")

latest_trade = trade_monthly.iloc[-1]["Trade_Value_USD"]

forecast_trade = forecast.iloc[-1]["Forecast"]

latest_revenue = revenue_monthly.iloc[-1]["Revenue_Collected_USD"]

st.success(f"""

## Executive Forecast Summary

**Latest Monthly Trade Value:** ${latest_trade:,.0f}

**Forecast Trade Value:** ${forecast_trade:,.0f}

**Latest Revenue:** ${latest_revenue:,.0f}

### Recommendations

• Increase border monitoring at high-volume crossings.

• Improve customs processing efficiency.

• Allocate more officers during peak trade periods.

• Continue monitoring trade diversion trends across ECOWAS.

""")

