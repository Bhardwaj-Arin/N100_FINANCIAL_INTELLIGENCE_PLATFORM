import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Portfolio Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/processed/master_features.csv"
    )

    return df


df = load_data()

# ==========================================================
# KEEP LATEST RECORD OF EACH COMPANY
# ==========================================================

year_column = None

if "year_y" in df.columns:

    year_column = "year_y"

elif "year_x" in df.columns:

    year_column = "year_x"

if year_column:

    df = (

        df

        .sort_values(year_column)

        .drop_duplicates(

            subset="company_name",

            keep="last"

        )

    )

else:

    df = df.drop_duplicates(

        subset="company_name"

    )

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

required_columns = [

    "company_name",

    "broad_sector",

    "FinancialHealthScore",

    "roe_percentage",

    "roce_percentage",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "cash_from_operations_cr",

    "free_cash_flow_cr",

    "OverallRank",

    "SectorRankFinal"

]

missing = [

    c

    for c in required_columns

    if c not in df.columns

]

if missing:

    st.error(

        f"Missing Columns : {missing}"

    )

    st.stop()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📊 Portfolio Analytics")

st.markdown(

"""
Build your own investment portfolio from the Nifty 100 companies and evaluate it using profitability, cash flow, financial health, diversification and ranking metrics.
"""

)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Portfolio Builder")

portfolio_name = st.sidebar.text_input(

    "Portfolio Name",

    "My Portfolio"

)

all_companies = sorted(

    df["company_name"].unique()

)

selected_companies = st.sidebar.multiselect(

    "Select Companies",

    all_companies,

    default=all_companies[:5]

)

if len(selected_companies) == 0:

    st.warning(

        "Please select at least one company."

    )

    st.stop()

# ==========================================================
# PORTFOLIO DATA
# ==========================================================

portfolio_df = (

    df[

        df["company_name"].isin(

            selected_companies

        )

    ]

    .copy()

)

portfolio_df.reset_index(

    drop=True,

    inplace=True

)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

company_count = len(portfolio_df)

sector_count = portfolio_df["broad_sector"].nunique()

avg_health = portfolio_df["FinancialHealthScore"].mean()

avg_roe = portfolio_df["roe_percentage"].mean()

avg_roce = portfolio_df["roce_percentage"].mean()

avg_npm = portfolio_df["net_profit_margin_pct"].mean()

avg_ocf = portfolio_df["cash_from_operations_cr"].mean()

avg_fcf = portfolio_df["free_cash_flow_cr"].mean()

# ==========================================================
# PORTFOLIO KPIs
# ==========================================================

st.subheader(f"📁 {portfolio_name}")

k1, k2, k3, k4 = st.columns(4)

k1.metric(

    "Companies",

    company_count

)

k2.metric(

    "Sectors",

    sector_count

)

k3.metric(

    "Average Health",

    f"{avg_health:.2f}"

)

k4.metric(

    "Average ROE",

    f"{avg_roe:.2f}%"

)

k5, k6, k7, k8 = st.columns(4)

k5.metric(

    "Average ROCE",

    f"{avg_roce:.2f}%"

)

k6.metric(

    "Net Profit Margin",

    f"{avg_npm:.2f}%"

)

k7.metric(

    "Operating Cash Flow",

    f"{avg_ocf:,.0f} Cr"

)

k8.metric(

    "Free Cash Flow",

    f"{avg_fcf:,.0f} Cr"

)

st.divider()

# ==========================================================
# SECTOR DISTRIBUTION
# ==========================================================

st.subheader("🏭 Portfolio Sector Distribution")

sector_df = (

    portfolio_df

    .groupby(

        "broad_sector",

        as_index=False

    )

    .agg(

        Companies=("company_name", "count")

    )

)

fig_sector = px.pie(

    sector_df,

    names="broad_sector",

    values="Companies",

    hole=0.45,

    template="plotly_dark",

    title="Portfolio Allocation"

)

fig_sector.update_layout(

    height=550

)

st.plotly_chart(

    fig_sector,

    use_container_width=True,

    key="portfolio_sector_chart"

)

st.divider()

# ==========================================================
# PORTFOLIO TABLE
# ==========================================================

st.subheader("🏢 Selected Companies")

display_df = portfolio_df[

    [

        "company_name",

        "broad_sector",

        "FinancialHealthScore",

        "roe_percentage",

        "roce_percentage",

        "OverallRank"

    ]

].copy()

display_df.columns = [

    "Company",

    "Sector",

    "Health Score",

    "ROE (%)",

    "ROCE (%)",

    "Overall Rank"

]

display_df = display_df.sort_values(

    "Overall Rank"

)

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True,

    height=420

)

st.divider()

# ==========================================================
# SECTION 2 : PORTFOLIO PERFORMANCE ANALYSIS
# ==========================================================

st.header("📈 Portfolio Performance Analysis")

# ==========================================================
# PERFORMANCE KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

c2.metric(
    "Average ROCE",
    f"{avg_roce:.2f}%"
)

c3.metric(
    "Net Profit Margin",
    f"{avg_npm:.2f}%"
)

c4.metric(
    "Financial Health",
    f"{avg_health:.2f}"
)

st.divider()

# ==========================================================
# HEALTH SCORE COMPARISON
# ==========================================================

st.subheader("🏥 Financial Health Score")

health_df = portfolio_df.sort_values(
    "FinancialHealthScore",
    ascending=False
)

fig_health = px.bar(

    health_df,

    x="company_name",

    y="FinancialHealthScore",

    color="FinancialHealthScore",

    text="FinancialHealthScore",

    color_continuous_scale="Viridis",

    template="plotly_dark"

)

fig_health.update_layout(

    height=550,

    xaxis_title="",

    yaxis_title="Financial Health Score",

    xaxis_tickangle=-35,

    coloraxis_showscale=False

)

st.plotly_chart(

    fig_health,

    use_container_width=True,

    key="health_score_chart"

)

st.divider()

# ==========================================================
# ROE vs ROCE
# ==========================================================

st.subheader("📊 ROE vs ROCE Comparison")

comparison_df = portfolio_df.melt(

    id_vars="company_name",

    value_vars=[

        "roe_percentage",

        "roce_percentage"

    ],

    var_name="Metric",

    value_name="Value"

)

comparison_df["Metric"] = comparison_df["Metric"].replace({

    "roe_percentage":"ROE",

    "roce_percentage":"ROCE"

})

fig_roe = px.bar(

    comparison_df,

    x="company_name",

    y="Value",

    color="Metric",

    barmode="group",

    template="plotly_dark"

)

fig_roe.update_layout(

    height=550,

    xaxis_tickangle=-35,

    xaxis_title="",

    yaxis_title="Percentage (%)"

)

st.plotly_chart(

    fig_roe,

    use_container_width=True,

    key="roe_roce_chart"

)

st.divider()

# ==========================================================
# CASH FLOW COMPARISON
# ==========================================================

st.subheader("💰 Cash Flow Comparison")

cash_df = portfolio_df.melt(

    id_vars="company_name",

    value_vars=[

        "cash_from_operations_cr",

        "free_cash_flow_cr"

    ],

    var_name="Metric",

    value_name="Cash Flow"

)

cash_df["Metric"] = cash_df["Metric"].replace({

    "cash_from_operations_cr":"Operating Cash Flow",

    "free_cash_flow_cr":"Free Cash Flow"

})

fig_cash = px.bar(

    cash_df,

    x="company_name",

    y="Cash Flow",

    color="Metric",

    barmode="group",

    template="plotly_dark"

)

fig_cash.update_layout(

    height=550,

    xaxis_tickangle=-35,

    xaxis_title="",

    yaxis_title="₹ Crore"

)

st.plotly_chart(

    fig_cash,

    use_container_width=True,

    key="cash_flow_chart"

)

st.divider()

# ==========================================================
# PERFORMANCE DISTRIBUTION
# ==========================================================

st.subheader("📦 Portfolio Metric Distribution")

metric_choice = st.selectbox(

    "Select Metric",

    [

        "FinancialHealthScore",

        "roe_percentage",

        "roce_percentage",

        "net_profit_margin_pct",

        "operating_profit_margin_pct"

    ],

    key="distribution_metric"

)

fig_box = px.box(

    portfolio_df,

    y=metric_choice,

    points="all",

    template="plotly_dark"

)

fig_box.update_layout(

    height=500,

    title=f"{metric_choice} Distribution"

)

st.plotly_chart(

    fig_box,

    use_container_width=True,

    key="distribution_chart"

)

st.divider()

# ==========================================================
# PERFORMANCE TABLE
# ==========================================================

st.subheader("📋 Portfolio Performance Summary")

summary_df = portfolio_df[

    [

        "company_name",

        "FinancialHealthScore",

        "roe_percentage",

        "roce_percentage",

        "net_profit_margin_pct",

        "cash_from_operations_cr",

        "free_cash_flow_cr"

    ]

].copy()

summary_df.columns = [

    "Company",

    "Health Score",

    "ROE (%)",

    "ROCE (%)",

    "Net Profit Margin",

    "Operating Cash Flow",

    "Free Cash Flow"

]

summary_df = summary_df.sort_values(

    "Health Score",

    ascending=False

)

st.dataframe(

    summary_df,

    use_container_width=True,

    hide_index=True,

    height=450

)

st.divider()

# ==========================================================
# SECTION 3 : PORTFOLIO DIVERSIFICATION ANALYSIS
# ==========================================================

st.header("🌐 Portfolio Diversification Analysis")

# ==========================================================
# SECTOR SUMMARY
# ==========================================================

sector_summary = (

    portfolio_df

    .groupby("broad_sector", as_index=False)

    .agg(

        Companies=("company_name", "count"),

        AvgHealth=("FinancialHealthScore", "mean"),

        AvgROE=("roe_percentage", "mean"),

        AvgROCE=("roce_percentage", "mean"),

        AvgFCF=("free_cash_flow_cr", "mean")

    )

)

sector_summary["Allocation (%)"] = (

    sector_summary["Companies"]

    / sector_summary["Companies"].sum()

    * 100

).round(2)

# ==========================================================
# DIVERSIFICATION KPIs
# ==========================================================

largest_sector = sector_summary.loc[
    sector_summary["Allocation (%)"].idxmax()
]

largest_allocation = largest_sector["Allocation (%)"]

diversification_score = round(
    100 - largest_allocation,
    2
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Sectors",
    sector_summary.shape[0]
)

c2.metric(
    "Largest Sector",
    largest_sector["broad_sector"]
)

c3.metric(
    "Largest Allocation",
    f"{largest_allocation:.1f}%"
)

c4.metric(
    "Diversification Score",
    f"{diversification_score:.1f}"
)

st.divider()

# ==========================================================
# SECTOR ALLOCATION DONUT
# ==========================================================

st.subheader("🥧 Sector Allocation")

fig_sector = px.pie(

    sector_summary,

    names="broad_sector",

    values="Companies",

    hole=0.45,

    template="plotly_dark"

)

fig_sector.update_layout(height=550)

st.plotly_chart(

    fig_sector,

    use_container_width=True,

    key="diversification_pie"

)

st.divider()

# ==========================================================
# TREEMAP
# ==========================================================

st.subheader("🌳 Portfolio Treemap")

fig_tree = px.treemap(

    portfolio_df,

    path=["broad_sector", "company_name"],

    values="FinancialHealthScore",

    color="FinancialHealthScore",

    color_continuous_scale="Viridis"

)

fig_tree.update_layout(height=650)

st.plotly_chart(

    fig_tree,

    use_container_width=True,

    key="portfolio_treemap"

)

st.divider()

# ==========================================================
# SECTOR HEALTH
# ==========================================================

st.subheader("🏥 Average Financial Health by Sector")

fig_health_sector = px.bar(

    sector_summary.sort_values(

        "AvgHealth",

        ascending=False

    ),

    x="broad_sector",

    y="AvgHealth",

    color="AvgHealth",

    text="AvgHealth",

    template="plotly_dark",

    color_continuous_scale="Viridis"

)

fig_health_sector.update_layout(

    height=550,

    xaxis_title="",

    yaxis_title="Average Health Score",

    coloraxis_showscale=False,

    xaxis_tickangle=-30

)

st.plotly_chart(

    fig_health_sector,

    use_container_width=True,

    key="sector_health"

)

st.divider()

# ==========================================================
# ROE VS ROCE BY SECTOR
# ==========================================================

st.subheader("📊 Sector Profitability")

profit_df = sector_summary.melt(

    id_vars="broad_sector",

    value_vars=[

        "AvgROE",

        "AvgROCE"

    ],

    var_name="Metric",

    value_name="Value"

)

profit_df["Metric"] = profit_df["Metric"].replace({

    "AvgROE":"ROE",

    "AvgROCE":"ROCE"

})

fig_profit = px.bar(

    profit_df,

    x="broad_sector",

    y="Value",

    color="Metric",

    barmode="group",

    template="plotly_dark"

)

fig_profit.update_layout(

    height=550,

    xaxis_tickangle=-30,

    xaxis_title="",

    yaxis_title="Percentage (%)"

)

st.plotly_chart(

    fig_profit,

    use_container_width=True,

    key="sector_profitability"

)

st.divider()

# ==========================================================
# SECTOR ALLOCATION BAR
# ==========================================================

st.subheader("📦 Sector Allocation (%)")

fig_alloc = px.bar(

    sector_summary.sort_values(

        "Allocation (%)",

        ascending=False

    ),

    x="broad_sector",

    y="Allocation (%)",

    text="Allocation (%)",

    color="Allocation (%)",

    color_continuous_scale="Blues",

    template="plotly_dark"

)

fig_alloc.update_layout(

    height=550,

    coloraxis_showscale=False,

    xaxis_tickangle=-30,

    xaxis_title="",

    yaxis_title="Allocation (%)"

)

st.plotly_chart(

    fig_alloc,

    use_container_width=True,

    key="allocation_chart"

)

st.divider()

# ==========================================================
# SECTOR SUMMARY TABLE
# ==========================================================

st.subheader("📋 Sector Summary")

sector_display = sector_summary.copy()

sector_display.columns = [

    "Sector",

    "Companies",

    "Average Health",

    "Average ROE",

    "Average ROCE",

    "Average FCF",

    "Allocation (%)"

]

sector_display = sector_display.sort_values(

    "Allocation (%)",

    ascending=False

)

st.dataframe(

    sector_display,

    use_container_width=True,

    hide_index=True,

    height=420

)

st.divider()

# ==========================================================
# SECTION 4 : COMPANY RANKING & BENCHMARKING
# ==========================================================

st.header("🏆 Company Ranking & Benchmarking")

ranking_df = portfolio_df.copy()

# ==========================================================
# METRIC SELECTOR
# ==========================================================

metric_options = {

    "Financial Health Score": "FinancialHealthScore",

    "ROE (%)": "roe_percentage",

    "ROCE (%)": "roce_percentage",

    "Net Profit Margin": "net_profit_margin_pct",

    "Operating Margin": "operating_profit_margin_pct",

    "Operating Cash Flow": "cash_from_operations_cr",

    "Free Cash Flow": "free_cash_flow_cr",

    "Overall Rank": "OverallRank"

}

selected_metric = st.selectbox(

    "Ranking Metric",

    list(metric_options.keys()),

    key="ranking_metric"

)

metric = metric_options[selected_metric]

ascending = metric == "OverallRank"

ranking_df = ranking_df.sort_values(

    metric,

    ascending=ascending

).reset_index(drop=True)

ranking_df["Portfolio Rank"] = range(1, len(ranking_df)+1)

# ==========================================================
# KPI CARDS
# ==========================================================

best = ranking_df.iloc[0]

worst = ranking_df.iloc[-1]

k1, k2, k3, k4 = st.columns(4)

k1.metric(

    "🥇 Best Company",

    best["company_name"]

)

k2.metric(

    "📉 Worst Company",

    worst["company_name"]

)

k3.metric(

    "Metric",

    selected_metric

)

best_value = best[metric]

if metric == "OverallRank":

    best_value = int(best_value)

else:

    best_value = round(best_value,2)

k4.metric(

    "Best Value",

    best_value

)

st.divider()

# ==========================================================
# LEADERBOARD
# ==========================================================

st.subheader("🏅 Portfolio Leaderboard")

fig_rank = px.bar(

    ranking_df,

    x=metric,

    y="company_name",

    orientation="h",

    color="FinancialHealthScore",

    text=metric,

    color_continuous_scale="Viridis",

    template="plotly_dark"

)

fig_rank.update_layout(

    height=650,

    coloraxis_showscale=False,

    yaxis_title="",

    xaxis_title=selected_metric,

    yaxis=dict(categoryorder="total ascending")

)

st.plotly_chart(

    fig_rank,

    use_container_width=True,

    key="leaderboard_chart"

)

st.divider()

# ==========================================================
# TOP VS BOTTOM
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("🥇 Top 5 Companies")

    st.dataframe(

        ranking_df.head(5)[

            [

                "company_name",

                "FinancialHealthScore",

                "OverallRank"

            ]

        ],

        use_container_width=True,

        hide_index=True

    )

with right:

    st.subheader("📉 Bottom 5 Companies")

    st.dataframe(

        ranking_df.tail(5)[

            [

                "company_name",

                "FinancialHealthScore",

                "OverallRank"

            ]

        ],

        use_container_width=True,

        hide_index=True

    )

st.divider()

# ==========================================================
# PORTFOLIO POSITIONING
# ==========================================================

st.subheader("🎯 Portfolio Positioning")

scatter_df = ranking_df.copy()

fcf_abs = scatter_df["free_cash_flow_cr"].abs()

if fcf_abs.max() == 0:

    scatter_df["BubbleSize"] = 30

else:

    scatter_df["BubbleSize"] = (

        fcf_abs / fcf_abs.max()

    ) * 70 + 20

fig_scatter = px.scatter(

    scatter_df,

    x="roe_percentage",

    y="FinancialHealthScore",

    size="BubbleSize",

    color="broad_sector",

    hover_name="company_name",

    hover_data={

        "roce_percentage":True,

        "OverallRank":True,

        "free_cash_flow_cr":True,

        "BubbleSize":False

    },

    template="plotly_dark"

)

fig_scatter.update_layout(

    height=650,

    xaxis_title="ROE (%)",

    yaxis_title="Financial Health Score"

)

st.plotly_chart(

    fig_scatter,

    use_container_width=True,

    key="portfolio_position_chart"

)

st.divider()

# ==========================================================
# COMPLETE RANKING TABLE
# ==========================================================

st.subheader("📋 Complete Portfolio Ranking")

table = ranking_df[

    [

        "Portfolio Rank",

        "company_name",

        "broad_sector",

        "FinancialHealthScore",

        "roe_percentage",

        "roce_percentage",

        "OverallRank",

        "SectorRankFinal"

    ]

].copy()

table.columns = [

    "Portfolio Rank",

    "Company",

    "Sector",

    "Health Score",

    "ROE (%)",

    "ROCE (%)",

    "Overall Rank",

    "Sector Rank"

]

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True,

    height=500

)

st.divider()

# ==========================================================
# SECTION 5 : EXECUTIVE PORTFOLIO INTELLIGENCE
# ==========================================================

st.header("🧠 Executive Portfolio Intelligence")

# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================

portfolio_health = portfolio_df["FinancialHealthScore"].mean()

best_company = portfolio_df.loc[
    portfolio_df["FinancialHealthScore"].idxmax()
]

worst_company = portfolio_df.loc[
    portfolio_df["FinancialHealthScore"].idxmin()
]

avg_overall_rank = portfolio_df["OverallRank"].mean()

avg_sector_rank = portfolio_df["SectorRankFinal"].mean()

# ==========================================================
# INVESTMENT OUTLOOK
# ==========================================================

if portfolio_health >= 85:
    outlook = "🟢 Excellent"

elif portfolio_health >= 70:
    outlook = "🟢 Strong"

elif portfolio_health >= 55:
    outlook = "🟡 Moderate"

elif portfolio_health >= 40:
    outlook = "🟠 Needs Attention"

else:
    outlook = "🔴 High Risk"

# ==========================================================
# STRENGTHS
# ==========================================================

strengths = []

if avg_roe >= 15:
    strengths.append("Strong Return on Equity across the portfolio.")

if avg_roce >= 15:
    strengths.append("Efficient capital utilization (high ROCE).")

if avg_ocf > 0:
    strengths.append("Positive Operating Cash Flow.")

if avg_fcf > 0:
    strengths.append("Positive Free Cash Flow.")

if sector_count >= 5:
    strengths.append("Well diversified across multiple sectors.")

if avg_overall_rank <= 30:
    strengths.append("Portfolio contains highly ranked companies.")

# ==========================================================
# RISKS
# ==========================================================

risks = []

if avg_roe < 10:
    risks.append("ROE is below desirable levels.")

if avg_roce < 10:
    risks.append("ROCE indicates lower capital efficiency.")

if avg_ocf <= 0:
    risks.append("Operating Cash Flow is weak.")

if avg_fcf <= 0:
    risks.append("Free Cash Flow is negative.")

if sector_count <= 2:
    risks.append("Portfolio concentration risk is high.")

if avg_overall_rank > 50:
    risks.append("Portfolio contains relatively lower-ranked companies.")

# ==========================================================
# KPI DASHBOARD
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Portfolio Health",
    f"{portfolio_health:.2f}"
)

c2.metric(
    "Investment Outlook",
    outlook
)

c3.metric(
    "Average Overall Rank",
    f"{avg_overall_rank:.1f}"
)

c4.metric(
    "Average Sector Rank",
    f"{avg_sector_rank:.1f}"
)

st.divider()

# ==========================================================
# BEST & WORST COMPANY
# ==========================================================

left, right = st.columns(2)

with left:

    st.success("### 🏆 Best Company")

    st.write(f"**Company:** {best_company['company_name']}")

    st.write(
        f"**Financial Health Score:** {best_company['FinancialHealthScore']:.2f}"
    )

    st.write(
        f"**Overall Rank:** {int(best_company['OverallRank'])}"
    )

    st.write(
        f"**ROE:** {best_company['roe_percentage']:.2f}%"
    )

    st.write(
        f"**ROCE:** {best_company['roce_percentage']:.2f}%"
    )

with right:

    st.error("### 📉 Lowest Scoring Company")

    st.write(f"**Company:** {worst_company['company_name']}")

    st.write(
        f"**Financial Health Score:** {worst_company['FinancialHealthScore']:.2f}"
    )

    st.write(
        f"**Overall Rank:** {int(worst_company['OverallRank'])}"
    )

    st.write(
        f"**ROE:** {worst_company['roe_percentage']:.2f}%"
    )

    st.write(
        f"**ROCE:** {worst_company['roce_percentage']:.2f}%"
    )

st.divider()

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

left, right = st.columns(2)

with left:

    st.success("### ✅ Portfolio Strengths")

    if strengths:
        for item in strengths:
            st.write(f"• {item}")
    else:
        st.write("No significant strengths identified.")

with right:

    st.error("### ⚠ Portfolio Risks")

    if risks:
        for item in risks:
            st.write(f"• {item}")
    else:
        st.write("No significant risks identified.")

st.divider()

# ==========================================================
# EXECUTIVE REPORT
# ==========================================================

report_df = pd.DataFrame({

    "Metric":[

        "Portfolio Name",

        "Companies",

        "Sectors",

        "Average Financial Health",

        "Average ROE",

        "Average ROCE",

        "Average Operating Cash Flow",

        "Average Free Cash Flow",

        "Average Overall Rank",

        "Average Sector Rank",

        "Best Company",

        "Investment Outlook"

    ],

    "Value":[

        portfolio_name,

        company_count,

        sector_count,

        round(portfolio_health,2),

        round(avg_roe,2),

        round(avg_roce,2),

        round(avg_ocf,2),

        round(avg_fcf,2),

        round(avg_overall_rank,2),

        round(avg_sector_rank,2),

        best_company["company_name"],

        outlook

    ]

})

st.subheader("📋 Executive Report")

st.dataframe(

    report_df,

    use_container_width=True,

    hide_index=True,

    height=420

)

st.divider()

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

csv = report_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇️ Download Executive Report (CSV)",

    data=csv,

    file_name=f"{portfolio_name}_Executive_Report.csv",

    mime="text/csv",

    key="download_executive_report"

)

st.divider()

st.success("✅ Portfolio Analysis Completed Successfully!")