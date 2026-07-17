# ============================================================
# ECOWAS Border Intelligence Analytics Platform
# Performance Scorecard
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
    page_title="Performance Scorecard",
    page_icon="🏆",
    layout="wide"
)

# ============================================================
# Chapter 3 - Load Dataset
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        Path("outputs") / "border_performance_scorecard.csv"
    )

scorecard = load_data()

# ============================================================
# Chapter 4 - Header
# ============================================================

st.title("🏆 Performance Scorecard")

st.caption(
    "Performance assessment of ECOWAS border posts."
)

st.markdown("---")

# ============================================================
# Chapter 5 - KPI Cards
# ============================================================

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Border Posts",
    len(scorecard)
)

col2.metric(
    "Average Score",
    f"{scorecard['Efficiency_Score'].mean():.1f}"
)

col3.metric(
    "Highest Score",
    f"{scorecard['Efficiency_Score'].max():.1f}"
)

col4.metric(
    "Lowest Score",
    f"{scorecard['Efficiency_Score'].min():.1f}"
)

# ============================================================
# Chapter 6 - Border Efficiency Ranking
# ============================================================

st.markdown("---")

fig1 = px.bar(
    scorecard.sort_values(
        "Efficiency_Score",
        ascending=False
    ),
    x="Border_Post",
    y="Efficiency_Score",
    color="Efficiency_Score",
    title="Border Efficiency Ranking"
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="efficiency"
)

# ============================================================
# Chapter 7 - Revenue Ranking
# ============================================================

st.markdown("---")

fig2 = px.bar(
    scorecard.sort_values(
        "Revenue_USD",
        ascending=False
    ),
    x="Border_Post",
    y="Revenue_USD",
    color="Revenue_USD",
    title="Revenue Collected"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="revenue"
)

# ============================================================
# Chapter 8 - Queue Length
# ============================================================

st.markdown("---")

fig3 = px.bar(
    scorecard.sort_values(
        "Avg_Queue"
    ),
    x="Border_Post",
    y="Avg_Queue",
    color="Avg_Queue",
    title="Average Queue Length"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="queue"
)

# ============================================================
# Chapter 9 - Processing Time
# ============================================================

st.markdown("---")

fig4 = px.bar(
    scorecard.sort_values(
        "Avg_Processing_Time"
    ),
    x="Border_Post",
    y="Avg_Processing_Time",
    color="Avg_Processing_Time",
    title="Average Processing Time"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="processing"
)

# ============================================================
# Chapter 10 - Performance Table
# ============================================================

st.markdown("---")

st.dataframe(
    scorecard,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# Chapter 11 - Download Scorecard
# ============================================================

st.markdown("---")

csv = scorecard.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Performance Scorecard",
    csv,
    "border_performance_scorecard.csv",
    "text/csv"
)

# ============================================================
# Chapter 12 - Executive Summary
# ============================================================

st.markdown("---")

best = scorecard.sort_values(
    "Efficiency_Score",
    ascending=False
).iloc[0]

st.success(f"""

## Executive Summary

**Best Performing Border:** {best['Border_Post']}

**Efficiency Score:** {best['Efficiency_Score']:.2f}

### Recommendation

Continue strengthening automation, intelligence-led inspections,
and regional cooperation to improve border performance.

""")


