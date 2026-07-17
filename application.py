import folium
from streamlit_folium import st_folium


# ============================================================
# ECOWAS Border Intelligence Analytics Platform (EBIAP)
# Streamlit Application
# ============================================================


# ============================================================
# Chapter 1 - Import Libraries
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import folium
from streamlit_folium import st_folium

from pathlib import Path

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(

    page_title="ECOWAS Border Intelligence Analytics Platform",

    page_icon="🌍",

    layout="wide",

    initial_sidebar_state="expanded"

)


# ============================================================
# Chapter 2 - Application Header
# ============================================================

st.title("🌍 ECOWAS Border Intelligence Analytics Platform")

st.subheader(

    "Impact Assessment of Simulated Regional Trade Diversion Following the AES Countries' Withdrawal from ECOWAS"

)

st.markdown("---")

st.sidebar.success("System Online")

st.sidebar.markdown("---")

st.sidebar.write("ECOWAS Border Intelligence Platform")

# ============================================================
# Chapter 3 - Load Datasets
# ============================================================

@st.cache_data
def load_data():

    data_folder = Path("data")
    output_folder = Path("outputs")

    transactions = pd.read_csv(
        data_folder / "trade_diversion_transactions.csv"
    )

# Load border coordinates
    border_locations = pd.read_csv("data/border_locations.csv")

    # Merge coordinates into the transaction dataset
    transactions = transactions.merge(
        border_locations[
            ["Border_Post", "Latitude", "Longitude"]
        ],
        on="Border_Post",
        how="left"

    )

    scorecard = pd.read_csv(
        output_folder / "border_performance_scorecard.csv"
    )

    return transactions, scorecard


df, scorecard = load_data()
st.write("Step 1 OK")


# ============================================================
# Sidebar Filters
# ============================================================
st.write("Step 2 OK")

st.sidebar.header("Dashboard Filters")

selected_country = st.sidebar.selectbox(
    "Entry Country",
    ["All"] + sorted(df["Entry_Country"].unique().tolist())
)

selected_border = st.sidebar.selectbox(
    "Border Post",
    ["All"] + sorted(df["Border_Post"].unique().tolist())
)

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Entry_Country"] == selected_country
    ]

if selected_border != "All":
    filtered_df = filtered_df[
        filtered_df["Border_Post"] == selected_border
    ]


# ============================================================
# Chapter 4 - Sidebar
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "Select Dashboard",

    [

        "Executive Dashboard",

        "Trade Analytics",

        "Risk Intelligence",

        "Geospatial Analytics",

        "Forecast",

        "Performance Scorecard",

        "Downloads",

        "About"

    ]

)


# ============================================================
# Chapter 5 - Executive Dashboard
# ============================================================

if page == "Executive Dashboard":
    st.header("Executive Dashboard")

    st.caption("Real-time overview of ECOWAS regional border operations")
    st.header("Executive Dashboard")

    total_transactions = len(filtered_df)

    total_trade = filtered_df["Trade_Value_USD"].sum()

    total_revenue = filtered_df["Revenue_Collected_USD"].sum()

    avg_queue = filtered_df["Queue_Length"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(

        "Transactions",

        f"{total_transactions:,}"

    )

    col2.metric(

        "Trade Value",

        f"${total_trade:,.0f}"

    )

    col3.metric(

        "Revenue",

        f"${total_revenue:,.0f}"

    )

    col4.metric(

        "Average Queue",

        f"{avg_queue:.1f}"

    )

    st.markdown("---")

    st.subheader("Trade Value by Entry Country")

    trade_summary = (
        filtered_df.groupby("Entry_Country")["Trade_Value_USD"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        trade_summary,
        x="Entry_Country",
        y="Trade_Value_USD",
        color="Trade_Value_USD",
        title="Trade Value by Entry Country"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Revenue Collected by Entry Country")

    revenue_summary = (
        filtered_df.groupby("Entry_Country")["Revenue_Collected_USD"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        revenue_summary,
        names="Entry_Country",
        values="Revenue_Collected_USD",
        title="Revenue Collected by Entry Country"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("Top 10 Busiest Border Posts")

    border_summary = (
        filtered_df.groupby("Border_Post")["Trade_Value_USD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        border_summary,
        x="Trade_Value_USD",
        y="Border_Post",
        orientation="h",
        color="Trade_Value_USD",
        title="Top 10 Busiest Border Posts"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    st.subheader("Monthly Trade Trend")

    monthly_trade = (
        filtered_df.groupby("Period")["Trade_Value_USD"]
        .sum()
        .reset_index()
    )

    fig4 = px.line(
        monthly_trade,
        x="Period",
        y="Trade_Value_USD",
        markers=True,
        title="Monthly Trade Value Trend"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")








