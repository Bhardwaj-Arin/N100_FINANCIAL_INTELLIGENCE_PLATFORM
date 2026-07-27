import streamlit as st
from dashboards.loader import load_data
from components.ui import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# LOAD CSS
# ==========================================================

load_css()

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# HERO
# ==========================================================

hero()

# ==========================================================
# KPI CARDS
# ==========================================================

companies = df["company_name"].nunique()
sectors = df["broad_sector"].nunique()
avg_score = df["FinancialHealthScore"].mean()
highest_score = df["FinancialHealthScore"].max()

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Companies", companies)

with c2:
    metric_card("Sectors", sectors)

with c3:
    metric_card("Average Score", f"{avg_score:.2f}")

with c4:
    metric_card("Highest Score", f"{highest_score:.2f}")

st.write("")

# ==========================================================
# ABOUT
# ==========================================================

section("📖", "About Platform")

left, right = st.columns([2.2, 1])

with left:

    st.markdown(
        """
The **Financial Intelligence Platform** is a modern analytics solution for evaluating
Indian listed companies using a custom **Financial Health Score**.

The platform combines profitability, valuation, leverage, capital efficiency,
market capitalization and financial ratios into one interactive application.

It allows investors, analysts, researchers and students to compare companies,
discover sector leaders and explore financial insights through interactive
visualizations.
"""
    )

with right:

    info_card(
        "Platform Objectives",
        """
<ul style="line-height:2;font-size:17px;">
<li>Company Analysis</li>
<li>Peer Comparison</li>
<li>Sector Analytics</li>
<li>Financial Rankings</li>
<li>Interactive Dashboards</li>
</ul>
""",
    )

st.write("")

# ==========================================================
# PLATFORM MODULES
# ==========================================================

section("🚀", "Platform Modules")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:

    feature_card(
        "📈",
        "Dashboard",
        "Executive overview of financial performance.",
        [
            "Financial KPIs",
            "Interactive Charts",
            "Health Distribution",
            "Top & Bottom Companies",
        ],
    )

with row1_col2:

    feature_card(
        "🏢",
        "Company Profile",
        "Detailed financial analysis of individual companies.",
        [
            "Company Overview",
            "Financial Ratios",
            "Health Gauge",
            "Company Information",
        ],
    )

st.write("")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:

    feature_card(
        "🤝",
        "Peer Comparison",
        "Compare companies side-by-side.",
        [
            "Comparison Table",
            "Radar Chart",
            "Financial Metrics",
            "Market Capitalization",
        ],
    )

with row2_col2:

    feature_card(
        "🏭",
        "Sector Analysis",
        "Industry level financial analysis.",
        [
            "Sector Summary",
            "Treemap",
            "Performance Matrix",
            "Market Distribution",
        ],
    )

st.write("")

feature_card(
    "🏆",
    "Rankings",
    "Discover the best and worst performing companies.",
    [
        "Financial Health Rankings",
        "Profitability Leaders",
        "Market Leaders",
        "Executive Leaderboard",
    ],
)

st.write("")

# ==========================================================
# FINANCIAL HEALTH SCORE
# ==========================================================

section("🧠", "Financial Health Score")

left, right = st.columns([2, 1])

with left:

    st.markdown(
        """
The **Financial Health Score** is a composite indicator developed to measure the
overall financial strength of a company.

It combines:

- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Debt to Equity
- Price to Earnings Ratio
- Book Value
- Market Capitalization

Higher scores represent financially stronger companies.
"""
    )

with right:

    info_card(
        "Score Guide",
        """
<h3>🟢 80 - 100</h3>
Excellent

<br><br>

<h3>🟡 60 - 80</h3>
Good

<br><br>

<h3>🟠 40 - 60</h3>
Average

<br><br>

<h3>🔴 Below 40</h3>
Weak
""",
    )

st.write("")

# ==========================================================
# QUICK INSIGHTS
# ==========================================================

section("📌", "Quick Insights")

@st.cache_data
def get_summary(df):
    return {
        "best": df.loc[df["FinancialHealthScore"].idxmax()],
        "worst": df.loc[df["FinancialHealthScore"].idxmin()],
        "largest_sector": df["broad_sector"].value_counts().idxmax(),
        "largest_company": df.loc[df["market_cap_crore"].idxmax()],
    }

summary = get_summary(df)

best = summary["best"]
worst = summary["worst"]
largest_sector = summary["largest_sector"]
largest_company = summary["largest_company"]

c1, c2 = st.columns(2)

with c1:

    info_card(
        "🏆 Strongest Company",
        f"""
<h2>{best['company_name']}</h2>

Financial Health Score

<h1>{best['FinancialHealthScore']:.2f}</h1>
""",
    )

    st.write("")

    info_card(
        "🏭 Largest Sector",
        f"""
<h2>{largest_sector}</h2>
""",
    )

with c2:

    info_card(
        "📉 Lowest Score",
        f"""
<h2>{worst['company_name']}</h2>

Financial Health Score

<h1>{worst['FinancialHealthScore']:.2f}</h1>
""",
    )

    st.write("")

    info_card(
        "💰 Highest Market Cap",
        f"""
<h2>{largest_company['company_name']}</h2>
""",
    )

st.write("")

# ==========================================================
# TECHNOLOGY STACK
# ==========================================================

section("🛠", "Technology Stack")

c1, c2, c3 = st.columns(3)

with c1:

    info_card(
        "Programming",
        """
🐍 Python

<br><br>

🐼 Pandas

<br><br>

🔢 NumPy
""",
    )

with c2:

    info_card(
        "Visualization",
        """
📊 Plotly

<br><br>

⚡ Streamlit

<br><br>

📈 Interactive Charts
""",
    )

with c3:

    info_card(
        "Analytics",
        """
🏦 Financial Ratios

<br><br>

📉 Financial Analysis

<br><br>

📊 Business Intelligence
""",
    )

footer()