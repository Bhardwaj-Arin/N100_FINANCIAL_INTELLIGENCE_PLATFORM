import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from dashboards.loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
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

.company-card{

background:linear-gradient(135deg,#0F172A,#1E293B);

padding:25px;

border-radius:20px;

border:1px solid #23314F;

margin-bottom:20px;

}

.metric-card{

background:linear-gradient(135deg,#1D4ED8,#2563EB);

padding:20px;

border-radius:18px;

text-align:center;

box-shadow:0 10px 25px rgba(37,99,235,.25);

}

.metric-title{

font-size:16px;

color:white;

font-weight:500;

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

margin-bottom:15px;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE TITLE
# =====================================================

st.markdown("# 🏢 Company Profile")
st.write("")

# =====================================================
# COMPANY SELECTOR
# =====================================================

companies = sorted(df["company_name"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = (
    df[df["company_name"] == selected_company]
    .sort_values(
        "FinancialHealthScore",
        ascending=False
    )
    .iloc[0]
)

# =====================================================
# COMPANY HEADER
# =====================================================

left,right=st.columns([1,4])

with left:

    logo=company["company_logo"]

    if isinstance(logo,str) and logo.startswith("http"):

        st.image(
            logo,
            width=130
        )

    else:

        st.info("No Logo")

with right:

    st.markdown(f"""
<div class="company-card">

<h1 style="color:white;">
{company['company_name']}
</h1>

<h4 style="color:#60A5FA;">
{company['broad_sector']}
</h4>

<p style="font-size:17px;color:#CBD5E1;">
{company['about_company']}
</p>

</div>
""",unsafe_allow_html=True)

# =====================================================
# LINKS
# =====================================================

b1,b2,b3=st.columns(3)

with b1:

    st.link_button(
        "🌐 Official Website",
        company["website"],
        use_container_width=True
    )

with b2:

    st.link_button(
        "NSE Profile",
        company["nse_profile"],
        use_container_width=True
    )

with b3:

    st.link_button(
        "BSE Profile",
        company["bse_profile"],
        use_container_width=True
    )

st.write("")

# =====================================================
# KPI CARDS
# =====================================================

k1,k2,k3,k4=st.columns(4)

with k1:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Financial Health
</div>

<div class="metric-value">
{company['FinancialHealthScore']:.2f}
</div>

</div>
""",unsafe_allow_html=True)

with k2:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
ROE
</div>

<div class="metric-value">
{company['roe_percentage']:.2f}%
</div>

</div>
""",unsafe_allow_html=True)

with k3:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
ROCE
</div>

<div class="metric-value">
{company['roce_percentage']:.2f}%
</div>

</div>
""",unsafe_allow_html=True)

with k4:

    st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
Book Value
</div>

<div class="metric-value">
₹{company['book_value']:.2f}
</div>

</div>
""",unsafe_allow_html=True)

st.write("")

k5,k6,k7=st.columns(3)

with k5:

    st.metric(
        "Market Cap",
        f"₹{company['market_cap_crore']:,.0f} Cr"
    )

with k6:

    st.metric(
        "P/E Ratio",
        f"{company['pe_ratio']:.2f}"
    )

with k7:

    st.metric(
        "Debt / Equity",
        f"{company['debt_to_equity']:.2f}"
    )

st.write("")

# =====================================================
# SECTION 2
# Financial Health Gauge + Company Snapshot
# =====================================================

st.markdown(
    '<div class="section">📊 Financial Health Overview</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.2, 1])

# =====================================================
# GAUGE
# =====================================================

with left:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=company["FinancialHealthScore"],
            number={
                "font": {"size": 46}
            },
            title={
                "text": "<b>Financial Health Score</b>",
                "font": {"size": 24}
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#2563EB",
                    "thickness": 0.35
                },
                "steps": [

                    {
                        "range":[0,40],
                        "color":"#7F1D1D"
                    },

                    {
                        "range":[40,60],
                        "color":"#92400E"
                    },

                    {
                        "range":[60,80],
                        "color":"#365314"
                    },

                    {
                        "range":[80,100],
                        "color":"#14532D"
                    }

                ],

                "threshold":{

                    "line":{
                        "color":"white",
                        "width":5
                    },

                    "value":company["FinancialHealthScore"]

                }

            }
        )
    )

    gauge.update_layout(

        template="plotly_dark",

        height=450,

        paper_bgcolor="#111827",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )

    )

    st.plotly_chart(
        gauge,
        use_container_width=True,
        config={"displayModeBar":False}
    )

# =====================================================
# SNAPSHOT
# =====================================================

with right:

    score=company["FinancialHealthScore"]

    if score>=80:
        badge="🟢 Excellent"

    elif score>=60:
        badge="🟡 Good"

    elif score>=40:
        badge="🟠 Average"

    else:
        badge="🔴 Weak"

    st.markdown(f"""

<div class="company-card">

<h2 style="color:#60A5FA;">
Company Snapshot
</h2>

<hr>

<h3>
Financial Rating
</h3>

<h2>
{badge}
</h2>

<hr>

<b>Sector</b>

<br>

{company["broad_sector"]}

<br><br>

<b>Market Capitalization</b>

<br>

₹ {company["market_cap_crore"]:,.0f} Crore

<br><br>

<b>Book Value</b>

<br>

₹ {company["book_value"]:.2f}

<br><br>

<b>P/E Ratio</b>

<br>

{company["pe_ratio"]:.2f}

<br><br>

<b>Debt / Equity</b>

<br>

{company["debt_to_equity"]:.2f}

</div>

""",unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# FUNDAMENTAL ANALYSIS
# =====================================================

st.markdown(
    '<div class="section">📈 Fundamental Analysis</div>',
    unsafe_allow_html=True
)

a,b,c=st.columns(3)

with a:

    st.info(f"""

### 💰 Profitability

ROE

**{company['roe_percentage']:.2f}%**

ROCE

**{company['roce_percentage']:.2f}%**

""")

with b:

    st.warning(f"""

### 📊 Valuation

Book Value

**₹ {company['book_value']:.2f}**

P/E Ratio

**{company['pe_ratio']:.2f}**

""")

with c:

    st.success(f"""

### 🏦 Financial Strength

Debt / Equity

**{company['debt_to_equity']:.2f}**

Health Score

**{company['FinancialHealthScore']:.2f}**

""")

st.write("")
st.write("")

# =====================================================
# SECTION 3
# Radar Chart + Financial Ratio Comparison
# =====================================================

st.markdown(
    '<div class="section">📊 Financial Ratio Analysis</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.1, 1])

# =====================================================
# RADAR CHART
# =====================================================

with left:

    radar_metrics = {
        "ROE": min(company["roe_percentage"], 100),
        "ROCE": min(company["roce_percentage"], 100),
        "Health": company["FinancialHealthScore"],
        "Book Value": min(company["book_value"], 100),
        "P/E": min(company["pe_ratio"], 100),
        "Debt": max(0, 100 - company["debt_to_equity"] * 10)
    }

    categories = list(radar_metrics.keys())
    values = list(radar_metrics.values())

    values += values[:1]
    categories += categories[:1]

    radar = go.Figure()

    radar.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line=dict(color="#3B82F6", width=3),
            fillcolor="rgba(59,130,246,0.35)",
            name=company["company_name"]
        )
    )

    radar.update_layout(

        template="plotly_dark",

        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,100]
            )
        ),

        showlegend=False,

        height=500,

        paper_bgcolor="#111827"
    )

    st.plotly_chart(
        radar,
        use_container_width=True,
        config={"displayModeBar":False}
    )

# =====================================================
# BAR COMPARISON
# =====================================================

with right:

    comparison = px.bar(

        x=[
            "ROE",
            "ROCE",
            "Book Value",
            "P/E",
            "Debt/Equity",
            "Health Score"
        ],

        y=[
            company["roe_percentage"],
            company["roce_percentage"],
            company["book_value"],
            company["pe_ratio"],
            company["debt_to_equity"],
            company["FinancialHealthScore"]
        ],

        color=[
            company["roe_percentage"],
            company["roce_percentage"],
            company["book_value"],
            company["pe_ratio"],
            company["debt_to_equity"],
            company["FinancialHealthScore"]
        ],

        color_continuous_scale="Blues",

        template="plotly_dark",

        title="Financial Metrics"
    )

    comparison.update_layout(

        height=500,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        coloraxis_showscale=False
    )

    st.plotly_chart(
        comparison,
        use_container_width=True,
        config={"displayModeBar":False}
    )

st.write("")
st.write("")

# =====================================================
# SCORE BREAKDOWN
# =====================================================

st.markdown(
    '<div class="section">🧠 Financial Score Breakdown</div>',
    unsafe_allow_html=True
)

score = company["FinancialHealthScore"]

if score >= 80:

    score_text = """
    🟢 Excellent Financial Position

    • Strong profitability

    • Healthy balance sheet

    • Attractive long-term investment
    """

elif score >= 60:

    score_text = """
    🟡 Good Financial Position

    • Stable business

    • Moderate financial strength

    • Positive long-term outlook
    """

elif score >= 40:

    score_text = """
    🟠 Average Financial Position

    • Mixed fundamentals

    • Requires detailed analysis

    • Moderate investment risk
    """

else:

    score_text = """
    🔴 Weak Financial Position

    • Financial concerns

    • Higher leverage/risk

    • Requires careful evaluation
    """

st.info(score_text)

st.write("")
st.write("")

# =====================================================
# SECTION 4
# Peer Companies + Sector Ranking + Footer
# =====================================================

st.markdown(
    '<div class="section">🤝 Similar Companies</div>',
    unsafe_allow_html=True
)

sector_df = (
    df[df["broad_sector"] == company["broad_sector"]]
    .copy()
)

sector_df = sector_df.sort_values(
    "FinancialHealthScore",
    ascending=False
)

sector_df = sector_df[
    [
        "company_name",
        "FinancialHealthScore",
        "roe_percentage",
        "roce_percentage",
        "market_cap_crore",
        "pe_ratio",
        "debt_to_equity",
    ]
]

sector_df.columns = [
    "Company",
    "Health Score",
    "ROE %",
    "ROCE %",
    "Market Cap",
    "P/E",
    "Debt/Equity",
]

st.dataframe(
    sector_df,
    use_container_width=True,
    hide_index=True,
    height=350,
)

st.write("")
st.write("")

# =====================================================
# COMPANY RANK
# =====================================================

st.markdown(
    '<div class="section">🏆 Sector Ranking</div>',
    unsafe_allow_html=True
)

ranking = (
    df[df["broad_sector"] == company["broad_sector"]]
    .sort_values(
        "FinancialHealthScore",
        ascending=False
    )
    .reset_index(drop=True)
)

rank = (
    ranking[
        ranking["company_name"] == company["company_name"]
    ].index[0]
    + 1
)

total = len(ranking)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Sector Rank",
        f"#{rank}"
    )

with c2:

    st.metric(
        "Companies",
        total
    )

with c3:

    percentile = (1 - (rank - 1) / total) * 100

    st.metric(
        "Percentile",
        f"{percentile:.1f}%"
    )

st.write("")
st.write("")

# =====================================================
# FINANCIAL SUMMARY
# =====================================================

st.markdown(
    '<div class="section">📋 Executive Summary</div>',
    unsafe_allow_html=True
)

summary = f"""

### {company['company_name']}

• Sector : **{company['broad_sector']}**

• Financial Health Score : **{company['FinancialHealthScore']:.2f}**

• ROE : **{company['roe_percentage']:.2f}%**

• ROCE : **{company['roce_percentage']:.2f}%**

• Market Capitalization : **₹ {company['market_cap_crore']:,.0f} Crore**

• Book Value : **₹ {company['book_value']:.2f}**

• P/E Ratio : **{company['pe_ratio']:.2f}**

• Debt / Equity : **{company['debt_to_equity']:.2f}**

"""

st.success(summary)

st.divider()

st.caption(
    "Financial Intelligence Platform • Company Profile • Built with Streamlit & Plotly"
)