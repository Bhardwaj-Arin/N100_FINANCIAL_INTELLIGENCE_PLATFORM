import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Cash Flow Intelligence",
    page_icon="💰",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    ratios = pd.read_excel(
        "data/raw/financial_ratios.xlsx"
    )

    master = pd.read_csv(
        "data/processed/master_features.csv"
    )

    companies = (

        master[
            [
                "company_id",
                "company_name",
                "broad_sector"
            ]
        ]

        .drop_duplicates()

    )

    ratios = ratios.merge(

        companies,

        on="company_id",

        how="left"

    )

    return ratios

df = load_data()

# ==========================================================
# DATA CLEANING
# ==========================================================

df = df.dropna(
    subset=[
        "company_name",
        "year"
    ]
)

df["year"] = df["year"].astype(str)

# ----------------------------------------------------------
# Remove duplicate company-year records
# ----------------------------------------------------------

df = (

    df.groupby(

        [
            "company_name",
            "broad_sector",
            "year"
        ],

        as_index=False

    )

    .agg({

        "cash_from_operations_cr":"mean",

        "free_cash_flow_cr":"mean",

        "capex_cr":"mean"

    })

)

# ----------------------------------------------------------
# Numeric conversion
# ----------------------------------------------------------

numeric_cols = [

    "cash_from_operations_cr",

    "free_cash_flow_cr",

    "capex_cr"

]

for col in numeric_cols:

    df[col] = pd.to_numeric(

        df[col],

        errors="coerce"

    )

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("💰 Cash Flow Intelligence")

st.write(
    "Analyze operating cash flow, free cash flow and capital expenditure across multiple financial years."
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Cash Flow Filters")

company = st.sidebar.selectbox(

    "Select Company",

    sorted(

        df["company_name"].unique()

    )

)

compare_sector = st.sidebar.checkbox(

    "Compare with Sector Average",

    value=True

)

# ==========================================================
# COMPANY DATA
# ==========================================================

company_df = (

    df[
        df["company_name"] == company
    ]

    .sort_values("year")

    .reset_index(drop=True)

)

latest = company_df.iloc[-1]

sector = latest["broad_sector"]

# ==========================================================
# CALCULATIONS
# ==========================================================

latest_ocf = latest["cash_from_operations_cr"]

latest_fcf = latest["free_cash_flow_cr"]

latest_capex = latest["capex_cr"]

cash_conversion = (

    latest_fcf

    /

    latest_ocf

    *100

    if latest_ocf != 0

    else 0

)

years_available = len(company_df)

# ==========================================================
# KPI CARDS
# ==========================================================

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric(

    "Operating Cash Flow",

    f"{latest_ocf:,.0f} Cr"

)

k2.metric(

    "Free Cash Flow",

    f"{latest_fcf:,.0f} Cr"

)

k3.metric(

    "Capital Expenditure",

    f"{latest_capex:,.0f} Cr"

)

k4.metric(

    "Cash Conversion",

    f"{cash_conversion:.1f}%"

)

k5.metric(

    "Years Available",

    years_available

)

st.divider()

# ==========================================================
# CASH FLOW TRENDS
# ==========================================================

st.subheader("📈 Cash Flow Trends")

tab1, tab2, tab3 = st.tabs(

    [

        "Operating Cash Flow",

        "Free Cash Flow",

        "Capital Expenditure"

    ]

)

# ==========================================================
# OPERATING CASH FLOW
# ==========================================================

with tab1:

    fig = px.line(

        company_df,

        x="year",

        y="cash_from_operations_cr",

        markers=True,

        text="cash_from_operations_cr",

        template="plotly_dark",

        title="Operating Cash Flow Trend"

    )

    fig.update_traces(

        line=dict(width=4),

        marker=dict(size=10),

        textposition="top center"

    )

    fig.update_layout(

        height=550,

        xaxis_title="Financial Year",

        yaxis_title="Cash From Operations (Cr)",

        hovermode="x unified"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# FREE CASH FLOW
# ==========================================================

with tab2:

    colors = [

        "green"

        if value >= 0

        else "crimson"

        for value in company_df["free_cash_flow_cr"]

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=company_df["year"],

            y=company_df["free_cash_flow_cr"],

            text=company_df["free_cash_flow_cr"],

            textposition="outside",

            marker_color=colors

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=550,

        title="Free Cash Flow Trend",

        xaxis_title="Financial Year",

        yaxis_title="Free Cash Flow (Cr)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# CAPEX
# ==========================================================

with tab3:

    fig = px.area(

        company_df,

        x="year",

        y="capex_cr",

        markers=True,

        template="plotly_dark",

        title="Capital Expenditure Trend"

    )

    fig.update_traces(

        line=dict(width=3)

    )

    fig.update_layout(

        height=550,

        xaxis_title="Financial Year",

        yaxis_title="CapEx (Cr)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# COMBINED CASH FLOW ANALYSIS
# ==========================================================

st.write("")

st.subheader("📊 Combined Cash Flow Analysis")

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=company_df["year"],

        y=company_df["cash_from_operations_cr"],

        mode="lines+markers",

        name="Operating Cash Flow",

        line=dict(width=4)

    )

)

fig.add_trace(

    go.Scatter(

        x=company_df["year"],

        y=company_df["free_cash_flow_cr"],

        mode="lines+markers",

        name="Free Cash Flow",

        line=dict(width=4)

    )

)

fig.add_trace(

    go.Scatter(

        x=company_df["year"],

        y=company_df["capex_cr"],

        mode="lines+markers",

        name="Capital Expenditure",

        line=dict(width=4)

    )

)

fig.update_layout(

    template="plotly_dark",

    height=650,

    hovermode="x unified",

    title="Operating Cash Flow vs Free Cash Flow vs Capital Expenditure",

    xaxis_title="Financial Year",

    yaxis_title="Amount (Cr)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# YEAR OVER YEAR KPI
# ==========================================================

st.write("")

st.subheader("📈 Year-over-Year Performance")

ocf_growth = (

    company_df["cash_from_operations_cr"]

    .pct_change()

    *100

)

fcf_growth = (

    company_df["free_cash_flow_cr"]

    .pct_change()

    *100

)

capex_growth = (

    company_df["capex_cr"]

    .pct_change()

    *100

)

c1, c2, c3 = st.columns(3)

c1.metric(

    "Latest OCF Growth",

    f"{ocf_growth.iloc[-1]:.2f}%"

    if pd.notna(ocf_growth.iloc[-1])

    else "N/A"

)

c2.metric(

    "Latest FCF Growth",

    f"{fcf_growth.iloc[-1]:.2f}%"

    if pd.notna(fcf_growth.iloc[-1])

    else "N/A"

)

c3.metric(

    "Latest CapEx Growth",

    f"{capex_growth.iloc[-1]:.2f}%"

    if pd.notna(capex_growth.iloc[-1])

    else "N/A"

)

# ==========================================================
# SECTOR COMPARISON
# ==========================================================

if compare_sector:

    st.write("")

    st.subheader("🏭 Company vs Sector Average")

    sector_df = (

        df[

            df["broad_sector"] == sector

        ]

        .groupby(

            "year",

            as_index=False

        )

        .agg({

            "cash_from_operations_cr":"mean"

        })

        .sort_values("year")

    )

    comparison_df = company_df.merge(

        sector_df,

        on="year",

        suffixes=(

            "_company",

            "_sector"

        )

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=comparison_df["year"],

            y=comparison_df["cash_from_operations_cr_company"],

            mode="lines+markers",

            name=company,

            line=dict(width=4)

        )

    )

    fig.add_trace(

        go.Scatter(

            x=comparison_df["year"],

            y=comparison_df["cash_from_operations_cr_sector"],

            mode="lines+markers",

            name="Sector Average",

            line=dict(

                dash="dash",

                width=3

            )

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=600,

        hovermode="x unified",

        title="Operating Cash Flow vs Sector Average",

        xaxis_title="Financial Year",

        yaxis_title="Operating Cash Flow (Cr)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# CASH FLOW HEALTH ANALYSIS
# ==========================================================

st.subheader("💹 Cash Flow Health Analysis")

left, right = st.columns(2)

with left:

    fig = px.bar(

        company_df,

        x="year",

        y="cash_from_operations_cr",

        text="cash_from_operations_cr",

        color="cash_from_operations_cr",

        color_continuous_scale="Greens",

        template="plotly_dark",

        title="Operating Cash Flow"

    )

    fig.update_layout(

        height=500,

        coloraxis_showscale=False,

        xaxis_title="Financial Year",

        yaxis_title="₹ Crore"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    colors = [

        "green"

        if x >= 0

        else "crimson"

        for x in company_df["free_cash_flow_cr"]

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=company_df["year"],

            y=company_df["free_cash_flow_cr"],

            text=company_df["free_cash_flow_cr"],

            textposition="outside",

            marker_color=colors

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=500,

        title="Free Cash Flow",

        xaxis_title="Financial Year",

        yaxis_title="₹ Crore"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# OPERATING CASH FLOW VS CAPEX
# ==========================================================

st.write("")

st.subheader("💰 Operating Cash Flow vs Capital Expenditure")

scatter_df = company_df.copy()

scatter_df["BubbleSize"] = (

    scatter_df["free_cash_flow_cr"]

    .abs()

    + 50

)

fig = px.scatter(

    scatter_df,

    x="capex_cr",

    y="cash_from_operations_cr",

    size="BubbleSize",

    color="free_cash_flow_cr",

    hover_name="year",

    color_continuous_scale="RdYlGn",

    template="plotly_dark",

    title="Cash Generation vs Capital Investment"

)

fig.update_layout(

    height=650,

    xaxis_title="Capital Expenditure (₹ Cr)",

    yaxis_title="Operating Cash Flow (₹ Cr)",

    coloraxis_colorbar_title="FCF"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# CASH FLOW DISTRIBUTION
# ==========================================================

st.write("")

st.subheader("📦 Distribution Analysis")

c1, c2 = st.columns(2)

with c1:

    fig = px.box(

        company_df,

        y="cash_from_operations_cr",

        points="all",

        template="plotly_dark",

        title="Operating Cash Flow Distribution"

    )

    fig.update_layout(height=500)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with c2:

    fig = px.box(

        company_df,

        y="free_cash_flow_cr",

        points="all",

        template="plotly_dark",

        title="Free Cash Flow Distribution"

    )

    fig.update_layout(height=500)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# CASH FLOW HEALTH SCORE
# ==========================================================

st.write("")

st.subheader("🩺 Cash Flow Health Score")

score = 0

if latest_ocf > 0:
    score += 35

if latest_fcf > 0:
    score += 35

if latest_capex < latest_ocf:
    score += 15

if cash_conversion > 20:
    score += 15

if score >= 85:

    status = "🟢 Excellent"

elif score >= 70:

    status = "🟢 Strong"

elif score >= 55:

    status = "🟡 Stable"

elif score >= 40:

    status = "🟠 Weak"

else:

    status = "🔴 Critical"

progress = score / 100

left, right = st.columns([1,2])

with left:

    st.metric(

        "Health Score",

        f"{score}/100"

    )

    st.metric(

        "Rating",

        status

    )

with right:

    st.progress(progress)

    st.write(f"Overall Cash Flow Health : **{status}**")

# ==========================================================
# HISTORICAL SUMMARY
# ==========================================================

st.write("")

st.subheader("📋 Historical Cash Flow Summary")

summary = company_df[

    [

        "year",

        "cash_from_operations_cr",

        "free_cash_flow_cr",

        "capex_cr"

    ]

].copy()

summary.columns = [

    "Financial Year",

    "Operating Cash Flow",

    "Free Cash Flow",

    "Capital Expenditure"

]

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True,

    height=420

)

st.divider()

# ==========================================================
# COMPANY & SECTOR BENCHMARKING
# ==========================================================

st.subheader("🏆 Company & Sector Benchmarking")

latest_year = company_df["year"].iloc[-1]

benchmark_df = (

    df[
        df["year"] == latest_year
    ]

    .copy()

)

benchmark_df = benchmark_df.dropna(

    subset=[

        "cash_from_operations_cr"

    ]

)

benchmark_df = benchmark_df.sort_values(

    "cash_from_operations_cr",

    ascending=False

)

# ==========================================================
# COMPANY RANK
# ==========================================================

benchmark_df["OCF Rank"] = (

    benchmark_df["cash_from_operations_cr"]

    .rank(

        ascending=False,

        method="dense"

    )

)

benchmark_df["FCF Rank"] = (

    benchmark_df["free_cash_flow_cr"]

    .rank(

        ascending=False,

        method="dense"

    )

)

benchmark_df["CapEx Rank"] = (

    benchmark_df["capex_cr"]

    .rank(

        ascending=True,

        method="dense"

    )

)

current_company = benchmark_df[
    benchmark_df["company_name"] == company
].iloc[0]

c1, c2, c3 = st.columns(3)

c1.metric(

    "OCF Rank",

    f"#{int(current_company['OCF Rank'])}"

)

c2.metric(

    "FCF Rank",

    f"#{int(current_company['FCF Rank'])}"

)

c3.metric(

    "CapEx Efficiency Rank",

    f"#{int(current_company['CapEx Rank'])}"

)

# ==========================================================
# TOP 10 OPERATING CASH FLOW
# ==========================================================

st.write("")

st.subheader("🥇 Top 10 Companies by Operating Cash Flow")

top10 = benchmark_df.head(10)

fig = px.bar(

    top10,

    x="cash_from_operations_cr",

    y="company_name",

    orientation="h",

    color="cash_from_operations_cr",

    text="cash_from_operations_cr",

    template="plotly_dark",

    color_continuous_scale="Greens",

    title=f"Financial Year : {latest_year}"

)

fig.update_layout(

    height=600,

    coloraxis_showscale=False,

    yaxis=dict(

        categoryorder="total ascending"

    ),

    xaxis_title="Operating Cash Flow (₹ Cr)",

    yaxis_title=""

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# SECTOR AVERAGE
# ==========================================================

st.write("")

st.subheader("🏭 Sector Cash Flow Comparison")

sector_summary = (

    benchmark_df

    .groupby(

        "broad_sector",

        as_index=False

    )

    .agg({

        "cash_from_operations_cr":"mean",

        "free_cash_flow_cr":"mean",

        "capex_cr":"mean"

    })

)

metric = st.selectbox(

    "Select Benchmark Metric",

    [

        "cash_from_operations_cr",

        "free_cash_flow_cr",

        "capex_cr"

    ],

    key="benchmark_metric"

)

metric_name = {

    "cash_from_operations_cr":"Operating Cash Flow",

    "free_cash_flow_cr":"Free Cash Flow",

    "capex_cr":"Capital Expenditure"

}

fig = px.bar(

    sector_summary,

    x="broad_sector",

    y=metric,

    color=metric,

    text=metric,

    template="plotly_dark",

    color_continuous_scale="Turbo",

    title=f"Average {metric_name[metric]} by Sector"

)

fig.update_layout(

    height=600,

    xaxis_tickangle=-30,

    coloraxis_showscale=False,

    xaxis_title="Sector",

    yaxis_title="Average (₹ Cr)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# CASH FLOW TREEMAP
# ==========================================================

st.write("")

st.subheader("🌳 Cash Flow Treemap")

treemap = benchmark_df.head(30)

fig = px.treemap(

    treemap,

    path=[

        "broad_sector",

        "company_name"

    ],

    values="cash_from_operations_cr",

    color="cash_from_operations_cr",

    color_continuous_scale="Greens"

)

fig.update_layout(

    height=700

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# LEADERBOARD
# ==========================================================

st.write("")

st.subheader("🏅 Cash Flow Leaderboard")

leaderboard = benchmark_df[

    [

        "company_name",

        "broad_sector",

        "cash_from_operations_cr",

        "free_cash_flow_cr",

        "capex_cr",

        "OCF Rank",

        "FCF Rank"

    ]

].copy()

leaderboard.columns = [

    "Company",

    "Sector",

    "Operating Cash Flow",

    "Free Cash Flow",

    "Capital Expenditure",

    "OCF Rank",

    "FCF Rank"

]

st.dataframe(

    leaderboard,

    use_container_width=True,

    hide_index=True,

    height=550

)

st.divider()

# ==========================================================
# EXECUTIVE CASH FLOW INTELLIGENCE
# ==========================================================

st.subheader("🧠 Executive Cash Flow Intelligence")

# ----------------------------------------------------------
# Historical Statistics
# ----------------------------------------------------------

avg_ocf = company_df["cash_from_operations_cr"].mean()
avg_fcf = company_df["free_cash_flow_cr"].mean()
avg_capex = company_df["capex_cr"].mean()

max_ocf = company_df["cash_from_operations_cr"].max()
min_ocf = company_df["cash_from_operations_cr"].min()

max_fcf = company_df["free_cash_flow_cr"].max()
min_fcf = company_df["free_cash_flow_cr"].min()

# ----------------------------------------------------------
# Growth Since First Year
# ----------------------------------------------------------

first_ocf = company_df.iloc[0]["cash_from_operations_cr"]
first_fcf = company_df.iloc[0]["free_cash_flow_cr"]

ocf_growth = 0
fcf_growth = 0

if first_ocf != 0:
    ocf_growth = ((latest_ocf - first_ocf) / abs(first_ocf)) * 100

if first_fcf != 0:
    fcf_growth = ((latest_fcf - first_fcf) / abs(first_fcf)) * 100

# ----------------------------------------------------------
# Investment Outlook
# ----------------------------------------------------------

if score >= 85:

    outlook = "🟢 Very Strong"

elif score >= 70:

    outlook = "🟢 Strong"

elif score >= 55:

    outlook = "🟡 Stable"

elif score >= 40:

    outlook = "🟠 Watch Closely"

else:

    outlook = "🔴 High Risk"

# ----------------------------------------------------------
# Strengths & Risks
# ----------------------------------------------------------

strengths = []
risks = []

if latest_ocf > 0:
    strengths.append("Strong positive Operating Cash Flow.")
else:
    risks.append("Operating Cash Flow is negative.")

if latest_fcf > 0:
    strengths.append("Positive Free Cash Flow after investments.")
else:
    risks.append("Negative Free Cash Flow.")

if latest_capex < latest_ocf:
    strengths.append("CapEx is comfortably funded by operations.")
else:
    risks.append("CapEx exceeds Operating Cash Flow.")

if cash_conversion >= 70:
    strengths.append("Excellent Cash Conversion Ratio.")
elif cash_conversion >= 40:
    strengths.append("Healthy Cash Conversion Ratio.")
else:
    risks.append("Weak Cash Conversion Ratio.")

if ocf_growth > 0:
    strengths.append("Operating Cash Flow has improved over time.")
else:
    risks.append("Operating Cash Flow has declined historically.")

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

left, right = st.columns(2)

with left:

    st.success("### 💰 Financial Summary")

    st.metric("Operating Cash Flow", f"{latest_ocf:,.2f} Cr")
    st.metric("Free Cash Flow", f"{latest_fcf:,.2f} Cr")
    st.metric("Capital Expenditure", f"{latest_capex:,.2f} Cr")
    st.metric("Cash Conversion", f"{cash_conversion:.2f}%")

with right:

    st.info("### 📊 Business Insights")

    st.metric("Health Score", f"{score}/100")
    st.metric("Investment Outlook", outlook)
    st.metric("OCF Rank", f"#{int(current_company['OCF Rank'])}")
    st.metric("FCF Rank", f"#{int(current_company['FCF Rank'])}")

# ==========================================================
# BUSINESS INTERPRETATION
# ==========================================================

st.write("")

col1, col2 = st.columns(2)

with col1:

    st.success("### ✅ Strengths")

    if strengths:

        for item in strengths:
            st.write(f"• {item}")

    else:

        st.write("No major strengths detected.")

with col2:

    st.error("### ⚠ Risks")

    if risks:

        for item in risks:
            st.write(f"• {item}")

    else:

        st.write("No significant risks detected.")

# ==========================================================
# EXECUTIVE REPORT
# ==========================================================

st.write("")
st.subheader("📋 Executive Cash Flow Report")

report = pd.DataFrame({

    "Metric":[

        "Company",
        "Sector",
        "Years Analysed",
        "Operating Cash Flow",
        "Free Cash Flow",
        "Capital Expenditure",
        "Average Operating Cash Flow",
        "Average Free Cash Flow",
        "Average CapEx",
        "Cash Conversion (%)",
        "Health Score",
        "Investment Outlook",
        "OCF Rank",
        "FCF Rank"

    ],

    "Value":[

        company,
        sector,
        years_available,
        round(latest_ocf,2),
        round(latest_fcf,2),
        round(latest_capex,2),
        round(avg_ocf,2),
        round(avg_fcf,2),
        round(avg_capex,2),
        round(cash_conversion,2),
        f"{score}/100",
        outlook,
        int(current_company["OCF Rank"]),
        int(current_company["FCF Rank"])

    ]

})

st.dataframe(
    report,
    use_container_width=True,
    hide_index=True,
    height=420
)

# ==========================================================
# DOWNLOADS
# ==========================================================

st.write("")

csv = report.to_csv(index=False).encode("utf-8")

col1, col2 = st.columns(2)

with col1:

    st.download_button(

        "⬇ Download CSV",

        csv,

        file_name=f"{company}_cashflow_report.csv",

        mime="text/csv",

        use_container_width=True

    )

with col2:

    from io import BytesIO

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        report.to_excel(
            writer,
            index=False,
            sheet_name="Cash Flow Report"
        )

    st.download_button(

        "⬇ Download Excel",

        excel_buffer.getvalue(),

        file_name=f"{company}_cashflow_report.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        use_container_width=True

    )

st.divider()

st.caption(
    "N100 Financial Intelligence Platform • Cash Flow Intelligence Dashboard"
)