import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Investment Screener",
    page_icon="🎯",
    layout="wide"
)

df = load_data()

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🎯 Investment Screener")
st.write("Filter companies using multiple financial metrics.")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Investment Filters")

preset = st.sidebar.selectbox(
    "Screening Preset",
    [
        "Custom",
        "Quality",
        "Growth",
        "Value",
        "Dividend",
        "Debt Free",
        "Turnaround"
    ]
)

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique())
)

company_search = st.sidebar.text_input(
    "Search Company"
)

health_band = st.sidebar.selectbox(
    "Health Band",
    [
        "All",
        "Excellent",
        "Good",
        "Average",
        "Weak",
        "Poor"
    ]
)

min_health = st.sidebar.slider(
    "Minimum Health Score",
    0,
    100,
    60
)

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    100,
    15
)

min_roce = st.sidebar.slider(
    "Minimum ROCE (%)",
    0,
    100,
    15
)

max_pe = st.sidebar.slider(
    "Maximum PE Ratio",
    0,
    200,
    40
)

max_debt = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    1.0
)

min_book = st.sidebar.number_input(
    "Minimum Book Value",
    value=0.0
)

min_market_cap = st.sidebar.number_input(
    "Minimum Market Cap (Crores)",
    value=0.0
)

sort_by = st.sidebar.selectbox(
    "Sort By",
    [
        "FinancialHealthScore",
        "roe_percentage",
        "roce_percentage",
        "market_cap_crore",
        "book_value",
        "pe_ratio"
    ]
)

ascending = st.sidebar.checkbox(
    "Ascending Order",
    value=False
)

top_n = st.sidebar.slider(
    "Top Companies",
    5,
    100,
    50
)

# =====================================================
# PRESETS
# =====================================================

if preset == "Quality":

    min_health = 80
    min_roe = 20
    min_roce = 20
    max_debt = 0.50

elif preset == "Growth":

    min_health = 70
    min_roe = 18
    min_roce = 18

elif preset == "Value":

    min_health = 60
    max_pe = 20

elif preset == "Dividend":

    min_health = 70
    max_debt = 0.50

elif preset == "Debt Free":

    max_debt = 0.20

elif preset == "Turnaround":

    min_health = 40
    max_debt = 2.0

# =====================================================
# FILTERING
# =====================================================

filtered = df.copy()

if sector != "All":

    filtered = filtered[
        filtered["broad_sector"] == sector
    ]

if company_search:

    filtered = filtered[
        filtered["company_name"]
        .str.contains(
            company_search,
            case=False,
            na=False
        )
    ]

filtered = filtered[

    (filtered["FinancialHealthScore"] >= min_health)

    &

    (filtered["roe_percentage"] >= min_roe)

    &

    (filtered["roce_percentage"] >= min_roce)

    &

    (filtered["pe_ratio"] <= max_pe)

    &

    (filtered["debt_to_equity"] <= max_debt)

    &

    (filtered["book_value"] >= min_book)

    &

    (filtered["market_cap_crore"] >= min_market_cap)

]

# =====================================================
# HEALTH BAND
# =====================================================

if health_band == "Excellent":

    filtered = filtered[
        filtered["FinancialHealthScore"] >= 80
    ]

elif health_band == "Good":

    filtered = filtered[
        (filtered["FinancialHealthScore"] >= 65)
        &
        (filtered["FinancialHealthScore"] < 80)
    ]

elif health_band == "Average":

    filtered = filtered[
        (filtered["FinancialHealthScore"] >= 50)
        &
        (filtered["FinancialHealthScore"] < 65)
    ]

elif health_band == "Weak":

    filtered = filtered[
        (filtered["FinancialHealthScore"] >= 35)
        &
        (filtered["FinancialHealthScore"] < 50)
    ]

elif health_band == "Poor":

    filtered = filtered[
        filtered["FinancialHealthScore"] < 35
    ]

filtered = (

    filtered

    .sort_values(
        sort_by,
        ascending=ascending
    )

    .drop_duplicates("company_name")

    .head(top_n)

)

# =====================================================
# KPI CARDS
# =====================================================

c1,c2,c3,c4=st.columns(4)

c1.metric(
    "Companies",
    len(filtered)
)

c2.metric(
    "Average Health",
    round(filtered["FinancialHealthScore"].mean(),2)
    if len(filtered) else 0
)

c3.metric(
    "Average ROE",
    round(filtered["roe_percentage"].mean(),2)
    if len(filtered) else 0
)

c4.metric(
    "Average ROCE",
    round(filtered["roce_percentage"].mean(),2)
    if len(filtered) else 0
)

st.write("")

# =====================================================
# RESULTS TABLE
# =====================================================

st.subheader("📋 Filtered Companies")

result = filtered[
    [
        "company_name",
        "broad_sector",
        "FinancialHealthScore",
        "roe_percentage",
        "roce_percentage",
        "pe_ratio",
        "book_value",
        "debt_to_equity",
        "market_cap_crore",
    ]
].copy()

result.columns = [
    "Company",
    "Sector",
    "Health Score",
    "ROE",
    "ROCE",
    "PE",
    "Book Value",
    "Debt/Equity",
    "Market Cap",
]

st.dataframe(
    result,
    use_container_width=True,
    hide_index=True,
    height=550,
)

# =====================================================
# EXPORTS
# =====================================================

st.write("")

left, right = st.columns(2)

csv = result.to_csv(index=False).encode("utf-8")

with left:

    st.download_button(
        "⬇ Download CSV",
        csv,
        "investment_screener.csv",
        "text/csv",
        use_container_width=True,
    )

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    result.to_excel(
        writer,
        index=False,
        sheet_name="Investment Screener"
    )

with right:

    st.download_button(
        "⬇ Download Excel",
        excel_buffer.getvalue(),
        "investment_screener.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.write("")

# =====================================================
# VISUALIZATIONS
# =====================================================

left, right = st.columns(2)

with left:

    fig = px.bar(
        filtered,
        x="FinancialHealthScore",
        y="company_name",
        orientation="h",
        color="FinancialHealthScore",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        title="Financial Health Ranking",
    )

    fig.update_layout(
        height=650,
        coloraxis_showscale=False,
        yaxis_title="",
        xaxis_title="Financial Health Score",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.scatter(
        filtered,
        x="roe_percentage",
        y="roce_percentage",
        size="market_cap_crore",
        color="FinancialHealthScore",
        hover_name="company_name",
        color_continuous_scale="Viridis",
        template="plotly_dark",
        title="ROE vs ROCE",
    )

    fig.update_layout(
        height=650,
        xaxis_title="ROE (%)",
        yaxis_title="ROCE (%)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.write("")

left, right = st.columns(2)

with left:

    fig = px.histogram(
        filtered,
        x="FinancialHealthScore",
        nbins=20,
        template="plotly_dark",
        title="Health Score Distribution",
        color_discrete_sequence=["#2563EB"],
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    sector_df = (
        filtered["broad_sector"]
        .value_counts()
        .reset_index()
    )

    sector_df.columns = [
        "Sector",
        "Companies"
    ]

    fig = px.pie(
        sector_df,
        names="Sector",
        values="Companies",
        hole=0.60,
        template="plotly_dark",
        title="Sector Distribution",
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("")

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("📌 Executive Insights")

if len(filtered) > 0:

    best_company = filtered.loc[
        filtered["FinancialHealthScore"].idxmax()
    ]

    highest_roe = filtered.loc[
        filtered["roe_percentage"].idxmax()
    ]

    highest_roce = filtered.loc[
        filtered["roce_percentage"].idxmax()
    ]

    lowest_debt = filtered.loc[
        filtered["debt_to_equity"].idxmin()
    ]

    largest_company = filtered.loc[
        filtered["market_cap_crore"].idxmax()
    ]

    c1, c2 = st.columns(2)

    with c1:

        st.success(f"""
### 🏆 Best Overall Company

**{best_company['company_name']}**

Health Score : **{best_company['FinancialHealthScore']:.2f}**

Sector : **{best_company['broad_sector']}**
""")

        st.info(f"""
### 📈 Highest ROE

**{highest_roe['company_name']}**

ROE : **{highest_roe['roe_percentage']:.2f}%**
""")

        st.warning(f"""
### 🏦 Largest Company

**{largest_company['company_name']}**

Market Cap :

₹ {largest_company['market_cap_crore']:,.0f} Cr
""")

    with c2:

        st.success(f"""
### 🏭 Highest ROCE

**{highest_roce['company_name']}**

ROCE : **{highest_roce['roce_percentage']:.2f}%**
""")

        st.info(f"""
### 🛡 Lowest Debt

**{lowest_debt['company_name']}**

Debt / Equity :

**{lowest_debt['debt_to_equity']:.2f}**
""")

        st.success(f"""
### 📊 Companies Matching Filters

**{len(filtered)}**
""")

else:

    st.error("No companies matched the selected filters.")

st.write("")
st.write("")

# =====================================================
# TOP 10 RESULTS
# =====================================================

if len(filtered) > 0:

    st.subheader("🏆 Top Screened Companies")

    top10 = filtered.head(10)[
        [
            "company_name",
            "FinancialHealthScore",
            "roe_percentage",
            "roce_percentage",
            "pe_ratio",
            "debt_to_equity",
            "market_cap_crore",
            "broad_sector",
        ]
    ].copy()

    top10.columns = [
        "Company",
        "Health Score",
        "ROE",
        "ROCE",
        "PE",
        "Debt/Equity",
        "Market Cap",
        "Sector",
    ]

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True,
        height=400,
    )

st.divider()

st.caption(
    "Financial Intelligence Platform • Investment Screener • Built with Streamlit & Plotly"
)