import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

df = load_data()

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:1.2rem;
    padding-bottom:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

.metric-card{

background:linear-gradient(135deg,#2563EB,#1D4ED8);

padding:18px;

border-radius:18px;

text-align:center;

box-shadow:0 10px 25px rgba(37,99,235,.25);

}

.metric-title{

font-size:15px;

font-weight:500;

color:white;

}

.metric-value{

font-size:34px;

font-weight:800;

color:white;

margin-top:8px;

}

.section{

font-size:30px;

font-weight:700;

margin-top:20px;

margin-bottom:18px;

}

.info-card{

background:linear-gradient(135deg,#0F172A,#1E293B);

padding:22px;

border-radius:18px;

border:1px solid #23314F;

margin-bottom:20px;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("# 🏭 Sector Analysis")

st.markdown("""

Analyze and compare the financial performance of
different industry sectors using financial health,
profitability, valuation and market capitalization.

""")

st.write("")

# =====================================================
# SECTOR SUMMARY
# =====================================================

sector_summary = (

    df

    .groupby(
        "broad_sector",
        as_index=False
    )

    .agg(

        Companies=("company_name","nunique"),

        AvgHealth=("FinancialHealthScore","mean"),

        AvgROE=("roe_percentage","mean"),

        AvgROCE=("roce_percentage","mean"),

        AvgPE=("pe_ratio","mean"),

        MarketCap=("market_cap_crore","sum")

    )

)

sector_summary = sector_summary.sort_values(
    "AvgHealth",
    ascending=False
)

# =====================================================
# KPI CARDS
# =====================================================

largest_sector = sector_summary.loc[
    sector_summary["Companies"].idxmax(),
    "broad_sector"
]

best_sector = sector_summary.loc[
    sector_summary["AvgHealth"].idxmax(),
    "broad_sector"
]

avg_health = sector_summary["AvgHealth"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Total Sectors
</div>

<div class="metric-value">
{len(sector_summary)}
</div>

</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Largest Sector
</div>

<div class="metric-value" style="font-size:18px;">
{largest_sector}
</div>

</div>
""", unsafe_allow_html=True)

with c3:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Best Sector
</div>

<div class="metric-value" style="font-size:18px;">
{best_sector}
</div>

</div>
""", unsafe_allow_html=True)

with c4:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Average Health
</div>

<div class="metric-value">
{avg_health:.1f}
</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# SECTOR SUMMARY TABLE
# =====================================================

st.markdown(
    '<div class="section">📋 Sector Summary</div>',
    unsafe_allow_html=True
)

summary_table = sector_summary.copy()

summary_table.columns = [

    "Sector",

    "Companies",

    "Avg Health",

    "Avg ROE",

    "Avg ROCE",

    "Avg P/E",

    "Market Cap"

]

st.dataframe(

    summary_table,

    use_container_width=True,

    hide_index=True,

    height=350

)

st.write("")
st.write("")

# =====================================================
# SECTION 2
# Financial Health & Sector Size
# =====================================================

st.markdown(
    '<div class="section">📊 Sector Performance Overview</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# =====================================================
# AVERAGE FINANCIAL HEALTH
# =====================================================

with left:

    fig = px.bar(

        sector_summary,

        x="broad_sector",

        y="AvgHealth",

        color="AvgHealth",

        text="AvgHealth",

        color_continuous_scale="Blues",

        template="plotly_dark",

        title="Average Financial Health Score"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}",

        textposition="outside"

    )

    fig.update_layout(

        height=450,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Health Score",

        xaxis_tickangle=-30

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

# =====================================================
# COMPANIES PER SECTOR
# =====================================================

with right:

    fig = px.bar(

        sector_summary,

        x="broad_sector",

        y="Companies",

        color="Companies",

        text="Companies",

        color_continuous_scale="Greens",

        template="plotly_dark",

        title="Number of Companies"

    )

    fig.update_traces(

        textposition="outside"

    )

    fig.update_layout(

        height=450,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Companies",

        xaxis_tickangle=-30

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

st.write("")
st.write("")

# =====================================================
# ROE & ROCE COMPARISON
# =====================================================

st.markdown(
    '<div class="section">📈 Profitability Comparison</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# =====================================================
# AVG ROE
# =====================================================

with left:

    fig = px.bar(

        sector_summary,

        x="broad_sector",

        y="AvgROE",

        color="AvgROE",

        text="AvgROE",

        color_continuous_scale="Tealgrn",

        template="plotly_dark",

        title="Average ROE (%)"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}",

        textposition="outside"

    )

    fig.update_layout(

        height=450,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="ROE (%)",

        xaxis_tickangle=-30

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

# =====================================================
# AVG ROCE
# =====================================================

with right:

    fig = px.bar(

        sector_summary,

        x="broad_sector",

        y="AvgROCE",

        color="AvgROCE",

        text="AvgROCE",

        color_continuous_scale="Purples",

        template="plotly_dark",

        title="Average ROCE (%)"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}",

        textposition="outside"

    )

    fig.update_layout(

        height=450,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="ROCE (%)",

        xaxis_tickangle=-30

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

st.write("")
st.write("")

# =====================================================
# SECTION 3
# Market Capital + Treemap + Performance Matrix
# =====================================================

st.markdown(
    '<div class="section">💰 Market Capital & Sector Distribution</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# =====================================================
# MARKET CAP DONUT
# =====================================================

with left:

    fig = px.pie(

        sector_summary,

        names="broad_sector",

        values="MarketCap",

        hole=0.55,

        template="plotly_dark",

        title="Market Capital Distribution"

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    fig.update_layout(

        height=480,

        paper_bgcolor="#111827",

        legend_title="Sector"

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

# =====================================================
# TREEMAP
# =====================================================

with right:

    fig = px.treemap(

        sector_summary,

        path=["broad_sector"],

        values="MarketCap",

        color="AvgHealth",

        color_continuous_scale="RdYlGn",

        template="plotly_dark"

    )

    fig.update_layout(

        height=480,

        paper_bgcolor="#111827",

        margin=dict(

            t=35,

            l=5,

            r=5,

            b=5

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

st.write("")
st.write("")

# =====================================================
# PERFORMANCE MATRIX
# =====================================================

st.markdown(
    '<div class="section">📊 Sector Performance Matrix</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.35, 1])

# =====================================================
# BUBBLE CHART
# =====================================================

with left:

    fig = px.scatter(

        sector_summary,

        x="AvgROE",

        y="AvgROCE",

        size="MarketCap",

        color="AvgHealth",

        hover_name="broad_sector",

        text="broad_sector",

        color_continuous_scale="Viridis",

        template="plotly_dark",

        title="ROE vs ROCE by Sector"

    )

    fig.update_traces(

        textposition="top center"

    )

    fig.update_layout(

        height=520,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        xaxis_title="Average ROE (%)",

        yaxis_title="Average ROCE (%)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

with right:

    best_health = sector_summary.loc[
        sector_summary["AvgHealth"].idxmax(),
        "broad_sector"
    ]

    biggest = sector_summary.loc[
        sector_summary["MarketCap"].idxmax(),
        "broad_sector"
    ]

    highest_roe = sector_summary.loc[
        sector_summary["AvgROE"].idxmax(),
        "broad_sector"
    ]

    highest_roce = sector_summary.loc[
        sector_summary["AvgROCE"].idxmax(),
        "broad_sector"
    ]

    most_companies = sector_summary.loc[
        sector_summary["Companies"].idxmax(),
        "broad_sector"
    ]

    st.markdown(f"""

<div class="info-card">

<h2 style="color:#60A5FA;">
📋 Sector Insights
</h2>

<hr>

🏆 <b>Best Financial Health</b>

<br>

{best_health}

<hr>

💰 <b>Largest Market Cap</b>

<br>

{biggest}

<hr>

📈 <b>Highest Average ROE</b>

<br>

{highest_roe}

<hr>

📊 <b>Highest Average ROCE</b>

<br>

{highest_roce}

<hr>

🏢 <b>Most Companies</b>

<br>

{most_companies}

<hr>

The bubble size represents total market
capitalization, while color intensity reflects
the average financial health score of each
sector.

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Financial Intelligence Platform • Sector Analysis Dashboard • Built with Streamlit & Plotly"
)