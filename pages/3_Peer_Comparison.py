import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="🤝",
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

.compare-card{

background:linear-gradient(135deg,#0F172A,#1E293B);

padding:22px;

border-radius:18px;

border:1px solid #243B53;

margin-bottom:20px;

}

.metric-card{

background:linear-gradient(135deg,#2563EB,#1D4ED8);

padding:18px;

border-radius:16px;

text-align:center;

box-shadow:0 8px 20px rgba(37,99,235,.30);

}

.metric-title{

color:white;

font-size:15px;

font-weight:500;

}

.metric-value{

color:white;

font-size:34px;

font-weight:800;

margin-top:8px;

}

.section{

font-size:30px;

font-weight:700;

margin-top:18px;

margin-bottom:18px;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("# 🤝 Peer Comparison")

st.markdown("""

Compare multiple companies side-by-side using their

financial health score, profitability,

valuation and leverage metrics.

""")

st.write("")

# =====================================================
# COMPANY SELECTION
# =====================================================

companies = sorted(df["company_name"].unique())

selected = st.multiselect(

    "Select up to 5 Companies",

    companies,

    max_selections=5

)

if len(selected) < 2:

    st.info("Please select at least two companies.")

    st.stop()

compare = (

    df[df["company_name"].isin(selected)]

    .sort_values(
        "FinancialHealthScore",
        ascending=False
    )

    .groupby(
        "company_name",
        as_index=False
    )

    .first()

)

# =====================================================
# QUICK SUMMARY
# =====================================================

highest = compare.iloc[0]

avg_score = compare["FinancialHealthScore"].mean()

left, center, right = st.columns(3)

with left:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Companies Selected
</div>

<div class="metric-value">
{len(compare)}
</div>

</div>
""", unsafe_allow_html=True)

with center:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Average Health Score
</div>

<div class="metric-value">
{avg_score:.1f}
</div>

</div>
""", unsafe_allow_html=True)

with right:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Top Performer
</div>

<div class="metric-value" style="font-size:20px;">
{highest["company_name"]}
</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# COMPARISON TABLE
# =====================================================

st.markdown(
    '<div class="section">📋 Company Comparison Table</div>',
    unsafe_allow_html=True
)

table = compare[
    [
        "company_name",
        "FinancialHealthScore",
        "roe_percentage",
        "roce_percentage",
        "market_cap_crore",
        "pe_ratio",
        "book_value",
        "debt_to_equity",
        "broad_sector"
    ]
].copy()

table.columns = [

    "Company",

    "Health Score",

    "ROE %",

    "ROCE %",

    "Market Cap",

    "P/E",

    "Book Value",

    "Debt/Equity",

    "Sector"

]

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True,

    height=320

)

st.write("")
st.write("")

# =====================================================
# SECTION 2
# Financial Performance Comparison
# =====================================================

st.markdown(
    '<div class="section">📊 Financial Performance Comparison</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# =====================================================
# FINANCIAL HEALTH
# =====================================================

with left:

    fig = px.bar(

        compare,

        x="company_name",

        y="FinancialHealthScore",

        color="FinancialHealthScore",

        text="FinancialHealthScore",

        color_continuous_scale="Blues",

        template="plotly_dark",

        title="Financial Health Score"

    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Score"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

# =====================================================
# ROE
# =====================================================

with right:

    fig = px.bar(

        compare,

        x="company_name",

        y="roe_percentage",

        color="roe_percentage",

        text="roe_percentage",

        color_continuous_scale="Greens",

        template="plotly_dark",

        title="Return on Equity (ROE %)"

    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="ROE (%)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

st.write("")
st.write("")

# =====================================================
# ROCE vs DEBT
# =====================================================

left, right = st.columns(2)

with left:

    fig = px.bar(

        compare,

        x="company_name",

        y="roce_percentage",

        color="roce_percentage",

        text="roce_percentage",

        color_continuous_scale="Purples",

        template="plotly_dark",

        title="Return on Capital Employed"

    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="ROCE (%)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

with right:

    fig = px.bar(

        compare,

        x="company_name",

        y="debt_to_equity",

        color="debt_to_equity",

        text="debt_to_equity",

        color_continuous_scale="Reds",

        template="plotly_dark",

        title="Debt to Equity Ratio"

    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Debt / Equity"

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
# Valuation & Market Comparison
# =====================================================

st.markdown(
    '<div class="section">💰 Valuation & Market Comparison</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# =====================================================
# MARKET CAP
# =====================================================

with left:

    fig = px.bar(

        compare,

        x="company_name",

        y="market_cap_crore",

        color="market_cap_crore",

        text="market_cap_crore",

        color_continuous_scale="Tealgrn",

        template="plotly_dark",

        title="Market Capitalization"

    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f} Cr",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Market Cap (Cr)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

# =====================================================
# BOOK VALUE
# =====================================================

with right:

    fig = px.bar(

        compare,

        x="company_name",

        y="book_value",

        color="book_value",

        text="book_value",

        color_continuous_scale="Viridis",

        template="plotly_dark",

        title="Book Value"

    )

    fig.update_traces(
        texttemplate="₹%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Book Value"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

st.write("")
st.write("")

# =====================================================
# P/E RATIO
# =====================================================

left, right = st.columns([1.25, 1])

with left:

    fig = px.bar(

        compare,

        x="company_name",

        y="pe_ratio",

        color="pe_ratio",

        text="pe_ratio",

        color_continuous_scale="Sunset",

        template="plotly_dark",

        title="Price to Earnings (P/E) Ratio"

    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(

        height=430,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="P/E Ratio"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

# =====================================================
# VALUATION INSIGHTS
# =====================================================

with right:

    highest_cap = compare.loc[
        compare["market_cap_crore"].idxmax(),
        "company_name"
    ]

    highest_pe = compare.loc[
        compare["pe_ratio"].idxmax(),
        "company_name"
    ]

    highest_book = compare.loc[
        compare["book_value"].idxmax(),
        "company_name"
    ]

    st.markdown(f"""

<div class="compare-card">

<h2 style="color:#60A5FA;">
📌 Valuation Highlights
</h2>

<hr>

### 🏦 Largest Company

**{highest_cap}**

<hr>

### 📈 Highest P/E Ratio

**{highest_pe}**

<hr>

### 💎 Highest Book Value

**{highest_book}**

<hr>

The charts compare company valuation,
market capitalization and intrinsic
book value, helping identify market
leaders and potentially undervalued
companies.

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# SECTION 4
# Radar Analysis + Winner Summary + Executive Insights
# =====================================================

st.markdown(
    '<div class="section">🎯 Overall Financial Comparison</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.25, 1])

# =====================================================
# RADAR CHART
# =====================================================

with left:

    radar = go.Figure()

    for _, row in compare.iterrows():

        radar.add_trace(

            go.Scatterpolar(

                r=[

                    min(row["FinancialHealthScore"],100),

                    min(row["roe_percentage"],100),

                    min(row["roce_percentage"],100),

                    min(row["book_value"],100),

                    min(row["pe_ratio"],100),

                    max(0,100-row["debt_to_equity"]*10)

                ],

                theta=[

                    "Health",

                    "ROE",

                    "ROCE",

                    "Book Value",

                    "P/E",

                    "Debt Strength"

                ],

                fill="toself",

                opacity=0.45,

                name=row["company_name"]

            )

        )

    radar.update_layout(

        template="plotly_dark",

        height=520,

        paper_bgcolor="#111827",

        polar=dict(

            bgcolor="#111827",

            radialaxis=dict(

                visible=True,

                range=[0,100]

            )

        ),

        legend=dict(

            orientation="h",

            y=-0.18

        )

    )

    st.plotly_chart(

        radar,

        use_container_width=True,

        config={"displayModeBar":False}

    )

# =====================================================
# WINNER ANALYSIS
# =====================================================

with right:

    winner_health = compare.loc[
        compare["FinancialHealthScore"].idxmax(),
        "company_name"
    ]

    winner_roe = compare.loc[
        compare["roe_percentage"].idxmax(),
        "company_name"
    ]

    winner_roce = compare.loc[
        compare["roce_percentage"].idxmax(),
        "company_name"
    ]

    winner_cap = compare.loc[
        compare["market_cap_crore"].idxmax(),
        "company_name"
    ]

    winner_book = compare.loc[
        compare["book_value"].idxmax(),
        "company_name"
    ]

    lowest_debt = compare.loc[
        compare["debt_to_equity"].idxmin(),
        "company_name"
    ]

    st.markdown(f"""

<div class="compare-card">

<h2 style="color:#60A5FA;">
🏆 Category Winners
</h2>

<hr>

🥇 <b>Best Financial Health</b>

<br>

{winner_health}

<hr>

📈 <b>Highest ROE</b>

<br>

{winner_roe}

<hr>

💹 <b>Highest ROCE</b>

<br>

{winner_roce}

<hr>

🏦 <b>Largest Market Cap</b>

<br>

{winner_cap}

<hr>

💎 <b>Highest Book Value</b>

<br>

{winner_book}

<hr>

🛡️ <b>Lowest Debt</b>

<br>

{lowest_debt}

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.markdown(
    '<div class="section">📋 Executive Summary</div>',
    unsafe_allow_html=True
)

leader = compare.iloc[0]

st.success(f"""

### Overall Best Performer

**{leader['company_name']}**

Financial Health Score:
**{leader['FinancialHealthScore']:.2f}**

ROE:
**{leader['roe_percentage']:.2f}%**

ROCE:
**{leader['roce_percentage']:.2f}%**

Market Capitalization:
**₹ {leader['market_cap_crore']:,.0f} Cr**

Sector:
**{leader['broad_sector']}**

This company currently ranks as the strongest among the selected peers based on
its Financial Health Score and overall financial indicators.

""")

st.divider()

st.caption(
    "Financial Intelligence Platform • Peer Comparison Dashboard • Built with Streamlit & Plotly"
)