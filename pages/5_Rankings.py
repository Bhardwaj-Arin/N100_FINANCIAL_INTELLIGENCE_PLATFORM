import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Rankings",
    page_icon="🏆",
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

st.markdown("# 🏆 Company Rankings")

st.markdown("""

Explore leaderboards based on Financial Health,
Profitability, Valuation and Market Capitalization.

Compare the strongest companies across every sector.

""")

st.write("")

# =====================================================
# LOAD DATA
# =====================================================

total_companies = df["company_name"].nunique()

avg_score = df["FinancialHealthScore"].mean()

elite_companies = (

    df[
        df["FinancialHealthScore"] >= 80
    ]["company_name"]

    .nunique()

)

aplus_companies = (

    df[
        df["FinancialHealthScore"] >= 90
    ]["company_name"]

    .nunique()

)

# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Companies
</div>

<div class="metric-value">
{total_companies}
</div>

</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Average Score
</div>

<div class="metric-value">
{avg_score:.1f}
</div>

</div>
""", unsafe_allow_html=True)

with c3:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Elite Companies
</div>

<div class="metric-value">
{elite_companies}
</div>

</div>
""", unsafe_allow_html=True)

with c4:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
A+ Rated
</div>

<div class="metric-value">
{aplus_companies}
</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# FILTERS
# =====================================================

st.markdown(
    '<div class="section">🎯 Ranking Filters</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

sector_options = sorted(
    df["broad_sector"].dropna().unique()
)

selected_sector = col1.selectbox(
    "Sector",
    ["All"] + sector_options
)

min_score = col2.slider(
    "Minimum Financial Health Score",
    0,
    100,
    0
)

filtered_df = df.copy()

if selected_sector != "All":

    filtered_df = filtered_df[
        filtered_df["broad_sector"] == selected_sector
    ]

filtered_df = filtered_df[
    filtered_df["FinancialHealthScore"] >= min_score
]

st.write("")

# =====================================================
# RANKING TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏆 Financial Health",
        "📈 Profitability",
        "💰 Valuation",
        "🏦 Market Leaders"
    ]
)

# ============================================================
# TAB 1 : FINANCIAL HEALTH
# ============================================================

with tab1:

    st.markdown(
        '<div class="section">🏆 Financial Health Rankings</div>',
        unsafe_allow_html=True
    )

    top10 = (

        filtered_df

        .sort_values(
            "FinancialHealthScore",
            ascending=False
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    bottom10 = (

        filtered_df

        .sort_values(
            "FinancialHealthScore"
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    left, right = st.columns(2)

    # =====================================================
    # TOP COMPANIES
    # =====================================================

    with left:

        st.subheader("🥇 Top 10 Companies")

        st.dataframe(

            top10[
                [
                    "company_name",
                    "FinancialHealthScore",
                    "roe_percentage",
                    "roce_percentage",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            top10,

            x="FinancialHealthScore",

            y="company_name",

            orientation="h",

            text="FinancialHealthScore",

            color="FinancialHealthScore",

            color_continuous_scale="Greens",

            template="plotly_dark"

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

            xaxis_title="Health Score",

            yaxis_title=""

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

    # =====================================================
    # BOTTOM COMPANIES
    # =====================================================

    with right:

        st.subheader("📉 Bottom 10 Companies")

        st.dataframe(

            bottom10[
                [
                    "company_name",
                    "FinancialHealthScore",
                    "roe_percentage",
                    "roce_percentage",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            bottom10,

            x="FinancialHealthScore",

            y="company_name",

            orientation="h",

            text="FinancialHealthScore",

            color="FinancialHealthScore",

            color_continuous_scale="Reds",

            template="plotly_dark"

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

            xaxis_title="Health Score",

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
    # EXECUTIVE INSIGHTS
    # =====================================================

    winner = top10.iloc[0]

    st.success(f"""

### 🏆 Financial Health Leader

**{winner['company_name']}**

**Financial Health Score:** {winner['FinancialHealthScore']:.2f}

**ROE:** {winner['roe_percentage']:.2f}%

**ROCE:** {winner['roce_percentage']:.2f}%

**Sector:** {winner['broad_sector']}

This company currently ranks first among the filtered companies based on
its overall Financial Health Score and financial strength.

""")

# ============================================================
# TAB 2 : PROFITABILITY
# ============================================================

with tab2:

    st.markdown(
        '<div class="section">📈 Profitability Rankings</div>',
        unsafe_allow_html=True
    )

    top_roe = (

        filtered_df

        .sort_values(
            "roe_percentage",
            ascending=False
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    top_roce = (

        filtered_df

        .sort_values(
            "roce_percentage",
            ascending=False
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    left, right = st.columns(2)

    # =====================================================
    # TOP ROE
    # =====================================================

    with left:

        st.subheader("🥇 Top ROE Companies")

        st.dataframe(

            top_roe[
                [
                    "company_name",
                    "roe_percentage",
                    "FinancialHealthScore",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            top_roe,

            x="roe_percentage",

            y="company_name",

            orientation="h",

            text="roe_percentage",

            color="roe_percentage",

            color_continuous_scale="Blues",

            template="plotly_dark"

        )

        fig.update_traces(

            texttemplate="%{text:.2f}",

            textposition="outside"

        )

        fig.update_layout(

            height=450,

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            coloraxis_showscale=False,

            xaxis_title="ROE (%)",

            yaxis_title=""

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

    # =====================================================
    # TOP ROCE
    # =====================================================

    with right:

        st.subheader("🏭 Top ROCE Companies")

        st.dataframe(

            top_roce[
                [
                    "company_name",
                    "roce_percentage",
                    "FinancialHealthScore",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            top_roce,

            x="roce_percentage",

            y="company_name",

            orientation="h",

            text="roce_percentage",

            color="roce_percentage",

            color_continuous_scale="Oranges",

            template="plotly_dark"

        )

        fig.update_traces(

            texttemplate="%{text:.2f}",

            textposition="outside"

        )

        fig.update_layout(

            height=450,

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            coloraxis_showscale=False,

            xaxis_title="ROCE (%)",

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
    # PROFITABILITY INSIGHTS
    # =====================================================

    best_roe = top_roe.iloc[0]

    best_roce = top_roce.iloc[0]

    c1, c2 = st.columns(2)

    with c1:

        st.success(f"""

### 📈 Highest ROE

**Company:** {best_roe['company_name']}

**ROE:** {best_roe['roe_percentage']:.2f}%

**Financial Health:** {best_roe['FinancialHealthScore']:.2f}

**Sector:** {best_roe['broad_sector']}

""")

    with c2:

        st.success(f"""

### 🏭 Highest ROCE

**Company:** {best_roce['company_name']}

**ROCE:** {best_roce['roce_percentage']:.2f}%

**Financial Health:** {best_roce['FinancialHealthScore']:.2f}

**Sector:** {best_roce['broad_sector']}

""")

# ============================================================
# TAB 3 : VALUATION
# ============================================================

with tab3:

    st.markdown(
        '<div class="section">💰 Valuation Rankings</div>',
        unsafe_allow_html=True
    )

    pe_df = (

        filtered_df

        .dropna(subset=["pe_ratio"])

        .sort_values(
            "pe_ratio"
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    bv_df = (

        filtered_df

        .dropna(subset=["book_value"])

        .sort_values(
            "book_value",
            ascending=False
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    left, right = st.columns(2)

    # =====================================================
    # LOWEST PE
    # =====================================================

    with left:

        st.subheader("💰 Lowest P/E Ratio")

        st.dataframe(

            pe_df[
                [
                    "company_name",
                    "pe_ratio",
                    "FinancialHealthScore",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            pe_df,

            x="pe_ratio",

            y="company_name",

            orientation="h",

            text="pe_ratio",

            color="pe_ratio",

            color_continuous_scale="Greens",

            template="plotly_dark"

        )

        fig.update_traces(

            texttemplate="%{text:.2f}",

            textposition="outside"

        )

        fig.update_layout(

            height=450,

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            coloraxis_showscale=False,

            xaxis_title="P/E Ratio",

            yaxis_title=""

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

        st.subheader("🏦 Highest Book Value")

        st.dataframe(

            bv_df[
                [
                    "company_name",
                    "book_value",
                    "FinancialHealthScore",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            bv_df,

            x="book_value",

            y="company_name",

            orientation="h",

            text="book_value",

            color="book_value",

            color_continuous_scale="Purples",

            template="plotly_dark"

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

            xaxis_title="Book Value",

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
    # VALUATION INSIGHTS
    # =====================================================

    lowest_pe = pe_df.iloc[0]

    highest_bv = bv_df.iloc[0]

    c1, c2 = st.columns(2)

    with c1:

        st.success(f"""

### 💰 Lowest P/E Company

**Company:** {lowest_pe['company_name']}

**P/E Ratio:** {lowest_pe['pe_ratio']:.2f}

**Financial Health:** {lowest_pe['FinancialHealthScore']:.2f}

**Sector:** {lowest_pe['broad_sector']}

""")

    with c2:

        st.success(f"""

### 🏦 Highest Book Value

**Company:** {highest_bv['company_name']}

**Book Value:** {highest_bv['book_value']:.2f}

**Financial Health:** {highest_bv['FinancialHealthScore']:.2f}

**Sector:** {highest_bv['broad_sector']}

""")

# ============================================================
# TAB 4 : MARKET LEADERS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section">🏦 Market Leaders</div>',
        unsafe_allow_html=True
    )

    market_df = (

        filtered_df

        .dropna(subset=["market_cap_crore"])

        .sort_values(
            "market_cap_crore",
            ascending=False
        )

        .drop_duplicates("company_name")

        .head(10)

    )

    sector_leaders = (

        filtered_df

        .dropna(subset=["market_cap_crore"])

        .sort_values(
            "market_cap_crore",
            ascending=False
        )

        .groupby("broad_sector")

        .head(1)

        .sort_values(
            "market_cap_crore",
            ascending=False
        )

    )

    left, right = st.columns(2)

    # =====================================================
    # TOP MARKET CAP
    # =====================================================

    with left:

        st.subheader("🏛 Top Market Cap Companies")

        st.dataframe(

            market_df[
                [
                    "company_name",
                    "market_cap_crore",
                    "FinancialHealthScore",
                    "broad_sector"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            market_df,

            x="market_cap_crore",

            y="company_name",

            orientation="h",

            text="market_cap_crore",

            color="market_cap_crore",

            color_continuous_scale="Blues",

            template="plotly_dark"

        )

        fig.update_traces(

            texttemplate="%{text:,.0f}",

            textposition="outside"

        )

        fig.update_layout(

            height=450,

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            coloraxis_showscale=False,

            xaxis_title="Market Cap (Cr)",

            yaxis_title=""

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

    # =====================================================
    # SECTOR LEADERS
    # =====================================================

    with right:

        st.subheader("🏭 Largest Company in Each Sector")

        st.dataframe(

            sector_leaders[
                [
                    "broad_sector",
                    "company_name",
                    "market_cap_crore",
                    "FinancialHealthScore"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=350

        )

        fig = px.bar(

            sector_leaders,

            x="market_cap_crore",

            y="broad_sector",

            orientation="h",

            text="company_name",

            color="FinancialHealthScore",

            color_continuous_scale="Viridis",

            template="plotly_dark"

        )

        fig.update_traces(

            textposition="outside"

        )

        fig.update_layout(

            height=450,

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            xaxis_title="Market Cap (Cr)",

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
    # TREEMAP & DONUT
    # =====================================================

    left, right = st.columns(2)

    with left:

        fig = px.treemap(

            market_df,

            path=["broad_sector","company_name"],

            values="market_cap_crore",

            color="FinancialHealthScore",

            color_continuous_scale="RdYlGn",

            template="plotly_dark"

        )

        fig.update_layout(

            height=500,

            paper_bgcolor="#111827"

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

    with right:

        sector_market = (

            filtered_df

            .groupby(
                "broad_sector",
                as_index=False
            )["market_cap_crore"]

            .sum()

        )

        fig = px.pie(

            sector_market,

            names="broad_sector",

            values="market_cap_crore",

            hole=0.55,

            template="plotly_dark"

        )

        fig.update_traces(

            textinfo="percent+label"

        )

        fig.update_layout(

            height=500,

            paper_bgcolor="#111827"

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

    st.write("")
    st.write("")

    # =====================================================
    # ELITE COMPANIES
    # =====================================================

    elite = (

        filtered_df[

            (filtered_df["FinancialHealthScore"] >= 80)

            & (filtered_df["roe_percentage"] >= 20)

            & (filtered_df["roce_percentage"] >= 20)

            & (filtered_df["debt_to_equity"] <= 0.50)

        ]

        .sort_values(
            "FinancialHealthScore",
            ascending=False
        )

        .drop_duplicates("company_name")

    )

    st.subheader("⭐ Elite Companies")

    st.metric(
        "Elite Companies Found",
        len(elite)
    )

    st.dataframe(

        elite[
            [
                "company_name",
                "FinancialHealthScore",
                "roe_percentage",
                "roce_percentage",
                "debt_to_equity",
                "market_cap_crore",
                "broad_sector"
            ]
        ],

        use_container_width=True,

        hide_index=True,

        height=320

    )

    st.write("")
    st.write("")

    # =====================================================
    # EXECUTIVE LEADERBOARD
    # =====================================================

    leaderboard = (

        filtered_df

        .sort_values(

            [

                "FinancialHealthScore",

                "market_cap_crore"

            ],

            ascending=False

        )

        .drop_duplicates("company_name")

        .head(20)

        .reset_index(drop=True)

    )

    leaderboard.insert(
        0,
        "Rank",
        leaderboard.index + 1
    )

    st.subheader("👑 Executive Leaderboard")

    st.dataframe(

        leaderboard[
            [
                "Rank",
                "company_name",
                "FinancialHealthScore",
                "market_cap_crore",
                "roe_percentage",
                "roce_percentage",
                "broad_sector"
            ]
        ],

        use_container_width=True,

        hide_index=True,

        height=450

    )

    st.divider()

    st.caption(
        "Financial Intelligence Platform • Rankings Dashboard • Built with Streamlit & Plotly"
    )
