import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# PAGE CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:1.2rem;
    padding-bottom:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

h1,h2,h3{
    color:white;
}

.metric-box{
    background:linear-gradient(135deg,#1E3A8A,#2563EB);
    padding:20px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 10px 25px rgba(37,99,235,.30);
    transition:.3s;
}

.metric-box:hover{
    transform:translateY(-5px);
}

.metric-title{
    color:white;
    font-size:17px;
    font-weight:500;
}

.metric-value{
    color:white;
    font-size:38px;
    font-weight:800;
}

.chart-card{
    background:#111827;
    border:1px solid #26344d;
    border-radius:18px;
    padding:15px;
}

.insight-card{
    background:#10243D;
    border-radius:18px;
    padding:18px;
    border:1px solid #234C84;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
# 📊 Financial Intelligence Dashboard
### Executive Overview of Listed Companies
""")

st.write("")

# =====================================================
# FILTERS
# =====================================================

left,right=st.columns([2,1])

with left:

    sector=st.selectbox(
        "Select Sector",
        ["All"]+sorted(df["broad_sector"].dropna().unique())
    )

with right:

    minimum_score=st.slider(
        "Minimum Health Score",
        0,
        100,
        0
    )

filtered=df.copy()

if sector!="All":
    filtered=filtered[
        filtered["broad_sector"]==sector
    ]

filtered=filtered[
    filtered["FinancialHealthScore"]>=minimum_score
]

# =====================================================
# KPI VALUES
# =====================================================

companies=filtered["company_name"].nunique()

avg_score=filtered["FinancialHealthScore"].mean()

highest_score=filtered["FinancialHealthScore"].max()

total_market_cap=filtered["market_cap_crore"].sum()

# =====================================================
# KPI CARDS
# =====================================================

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""
<div class="metric-box">

<div class="metric-title">
Companies
</div>

<div class="metric-value">
{companies}
</div>

</div>
""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""
<div class="metric-box">

<div class="metric-title">
Average Score
</div>

<div class="metric-value">
{avg_score:.2f}
</div>

</div>
""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""
<div class="metric-box">

<div class="metric-title">
Highest Score
</div>

<div class="metric-value">
{highest_score:.2f}
</div>

</div>
""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""
<div class="metric-box">

<div class="metric-title">
Market Cap
</div>

<div class="metric-value">
₹{total_market_cap/1000:.1f}K Cr
</div>

</div>
""",unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# ROW 1
# Score Distribution + Gauge + Sector Distribution
# =====================================================

left, right = st.columns((2, 1))

with left:

    fig = px.histogram(
        filtered,
        x="FinancialHealthScore",
        nbins=20,
        color_discrete_sequence=["#3B82F6"],
        title="Financial Health Score Distribution",
        template="plotly_dark",
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20, r=20, t=60, b=20),
        title_font_size=22,
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1,
        opacity=0.9,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with right:

    avg = filtered["FinancialHealthScore"].mean()

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg,
            title={
                "text": "<b>Average Financial Health</b>",
                "font": {"size": 22},
            },
            number={
                "font": {"size": 42},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                },
                "bar": {
                    "color": "#2563EB",
                    "thickness": 0.35,
                },
                "steps": [
                    {"range": [0, 40], "color": "#7F1D1D"},
                    {"range": [40, 60], "color": "#92400E"},
                    {"range": [60, 80], "color": "#365314"},
                    {"range": [80, 100], "color": "#14532D"},
                ],
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 4,
                    },
                    "value": avg,
                },
            },
        )
    )

    gauge.update_layout(
        template="plotly_dark",
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#111827",
    )

    st.plotly_chart(
        gauge,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    sector_dist = (
        filtered["broad_sector"]
        .value_counts()
        .reset_index()
    )

    sector_dist.columns = [
        "Sector",
        "Companies",
    ]

    donut = px.pie(
        sector_dist,
        values="Companies",
        names="Sector",
        hole=0.60,
        title="Sector Distribution",
        template="plotly_dark",
    )

    donut.update_traces(
        textinfo="percent+label"
    )

    donut.update_layout(
        height=330,
        paper_bgcolor="#111827",
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=False,
    )

    st.plotly_chart(
        donut,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.write("")
st.write("")

# =====================================================
# ROW 2
# Top 10 & Bottom 10 Companies
# =====================================================

left, right = st.columns(2)

with left:

    top10 = (
        filtered.groupby("company_name", as_index=False)[
            "FinancialHealthScore"
        ]
        .max()
        .sort_values(
            "FinancialHealthScore",
            ascending=False
        )
        .head(10)
        .sort_values("FinancialHealthScore")
    )

    fig = px.bar(
        top10,
        x="FinancialHealthScore",
        y="company_name",
        orientation="h",
        color="FinancialHealthScore",
        color_continuous_scale="Greens",
        text="FinancialHealthScore",
        template="plotly_dark",
        title="🏆 Top 10 Companies"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20,r=20,t=60,b=20),
        coloraxis_showscale=False,
        xaxis_title="Financial Health Score",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

with right:

    bottom10 = (
        filtered.groupby("company_name", as_index=False)[
            "FinancialHealthScore"
        ]
        .max()
        .sort_values(
            "FinancialHealthScore"
        )
        .head(10)
        .sort_values("FinancialHealthScore")
    )

    fig = px.bar(
        bottom10,
        x="FinancialHealthScore",
        y="company_name",
        orientation="h",
        color="FinancialHealthScore",
        color_continuous_scale="Reds",
        text="FinancialHealthScore",
        template="plotly_dark",
        title="📉 Bottom 10 Companies"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20,r=20,t=60,b=20),
        coloraxis_showscale=False,
        xaxis_title="Financial Health Score",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

st.write("")
st.write("")

# =====================================================
# ROW 3
# Sector Performance + Scatter Analysis
# =====================================================

left, right = st.columns(2)

with left:

    sector_scores = (
        filtered.groupby("broad_sector", as_index=False)
        .agg(
            AverageScore=("FinancialHealthScore", "mean"),
            Companies=("company_name", "nunique"),
        )
        .sort_values("AverageScore", ascending=False)
    )

    fig = px.bar(
        sector_scores,
        x="AverageScore",
        y="broad_sector",
        orientation="h",
        color="AverageScore",
        color_continuous_scale="Blues",
        text="AverageScore",
        template="plotly_dark",
        title="🏭 Average Financial Health by Sector",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_showscale=False,
        xaxis_title="Average Financial Health Score",
        yaxis_title="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with right:

    scatter = px.scatter(
        filtered,
        x="market_cap_crore",
        y="FinancialHealthScore",
        size="market_cap_crore",
        color="broad_sector",
        hover_name="company_name",
        template="plotly_dark",
        title="💰 Market Cap vs Financial Health",
        size_max=45,
    )

    scatter.update_layout(
        height=500,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Market Cap (Crores)",
        yaxis_title="Financial Health Score",
    )

    st.plotly_chart(
        scatter,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.write("")
st.write("")

# =====================================================
# ROW 4
# ROE vs ROCE
# =====================================================

required_cols = {"ROE", "ROCE"}

if required_cols.issubset(filtered.columns):

    fig = px.scatter(
        filtered,
        x="ROE",
        y="ROCE",
        size="market_cap_crore",
        color="broad_sector",
        hover_name="company_name",
        template="plotly_dark",
        title="📈 ROE vs ROCE Analysis",
        size_max=45,
    )

    fig.update_layout(
        height=600,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Return on Equity (ROE)",
        yaxis_title="Return on Capital Employed (ROCE)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.write("")
st.write("")

# =====================================================
# ROW 5
# TREEMAP
# =====================================================

required_cols = {
    "company_name",
    "broad_sector",
    "market_cap_crore",
    "FinancialHealthScore",
}

if required_cols.issubset(filtered.columns):

    treemap = px.treemap(
        filtered,
        path=["broad_sector", "company_name"],
        values="market_cap_crore",
        color="FinancialHealthScore",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        title="🌳 Market Capitalization Treemap",
    )

    treemap.update_layout(
        height=650,
        paper_bgcolor="#111827",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    st.plotly_chart(
        treemap,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.write("")
st.write("")

# =====================================================
# ROW 6
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("📌 Executive Insights")

best_company = filtered.loc[
    filtered["FinancialHealthScore"].idxmax()
]

worst_company = filtered.loc[
    filtered["FinancialHealthScore"].idxmin()
]

largest_company = filtered.loc[
    filtered["market_cap_crore"].idxmax()
]

sector_summary = (
    filtered.groupby("broad_sector")["FinancialHealthScore"]
    .mean()
    .sort_values(ascending=False)
)

best_sector = sector_summary.index[0]
worst_sector = sector_summary.index[-1]

c1, c2 = st.columns(2)

with c1:

    st.success(
        f"""
🏆 Best Company : {best_company['company_name']}

Financial Health Score : {best_company['FinancialHealthScore']:.2f}
"""
    )

    st.info(
        f"""
🏭 Best Sector : {best_sector}

Average Score : {sector_summary.iloc[0]:.2f}
"""
    )

    st.warning(
        f"""
💰 Largest Company :

{largest_company['company_name']}
"""
    )

with c2:

    st.error(
        f"""
📉 Lowest Company :

{worst_company['company_name']}

Financial Health Score : {worst_company['FinancialHealthScore']:.2f}
"""
    )

    st.info(
        f"""
📊 Weakest Sector :

{worst_sector}

Average Score : {sector_summary.iloc[-1]:.2f}
"""
    )

    st.success(
        f"""
📈 Dataset Average Score

{filtered['FinancialHealthScore'].mean():.2f}
"""
    )

st.write("")
st.divider()

st.caption(
    "Financial Intelligence Platform • Dashboard • Built with Streamlit & Plotly"
)