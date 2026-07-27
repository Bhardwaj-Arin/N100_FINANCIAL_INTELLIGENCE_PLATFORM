import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_financial_ratios():
    return pd.read_excel("data/raw/financial_ratios.xlsx")

df = load_financial_ratios()

df["year"] = df["year"].astype(str)

# ==========================================================
# COMPANY MAPPING
# ==========================================================

company_master = pd.read_csv("data/processed/master_features.csv")

company_map = (
    company_master[
        ["company_id", "company_name"]
    ]
    .drop_duplicates()
)

df = df.merge(
    company_map,
    on="company_id",
    how="left"
)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📈 Trend Analysis")
st.write("Analyze historical financial trends of individual companies.")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Trend Filters")

company = st.sidebar.selectbox(
    "Select Company",
    sorted(df["company_name"].dropna().unique())
)

metric = st.sidebar.selectbox(
    "Financial Metric",
    [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr"
    ]
)

chart_type = st.sidebar.radio(
    "Chart Type",
    [
        "Line",
        "Area",
        "Bar"
    ]
)

show_markers = st.sidebar.checkbox(
    "Show Markers",
    value=True
)

show_average = st.sidebar.checkbox(
    "Show Average Line",
    value=True
)

# ==========================================================
# FILTER DATA
# ==========================================================

company_df = (
    df[df["company_name"] == company]
    .sort_values("year")
    .reset_index(drop=True)
)

latest = company_df.iloc[-1]

average_value = company_df[metric].mean()

highest_value = company_df[metric].max()

lowest_value = company_df[metric].min()

# ==========================================================
# KPI CARDS
# ==========================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Company",
    company
)

k2.metric(
    "Latest Value",
    f"{latest[metric]:,.2f}"
)

k3.metric(
    "Average",
    f"{average_value:,.2f}"
)

k4.metric(
    "Available Years",
    company_df["year"].nunique()
)

# ==========================================================
# HISTORICAL TREND
# ==========================================================

st.write("")

st.subheader(f"📊 {metric.replace('_',' ').title()} Trend")

if chart_type == "Line":

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=company_df["year"],

            y=company_df[metric],

            mode="lines+markers" if show_markers else "lines",

            line=dict(width=4),

            marker=dict(size=10),

            name=metric

        )

    )

elif chart_type == "Area":

    fig = px.area(

        company_df,

        x="year",

        y=metric

    )

else:

    fig = px.bar(

        company_df,

        x="year",

        y=metric,

        text_auto=".2f"

    )

# ----------------------------------------------------------
# Moving Average
# ----------------------------------------------------------

company_df["MovingAverage"] = (

    company_df[metric]

    .rolling(3)

    .mean()

)

fig.add_trace(

    go.Scatter(

        x=company_df["year"],

        y=company_df["MovingAverage"],

        mode="lines",

        line=dict(

            dash="dash",

            width=3,

            color="orange"

        ),

        name="3-Year Moving Average"

    )

)

# ----------------------------------------------------------
# Average Line
# ----------------------------------------------------------

if show_average:

    fig.add_hline(

        y=average_value,

        line_dash="dot",

        annotation_text="Average"

    )

fig.update_layout(

    template="plotly_dark",

    height=650,

    xaxis_title="Financial Year",

    yaxis_title=metric.replace("_"," ").title(),

    legend_title="Legend"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# TREND DATA
# ==========================================================

st.write("")

st.subheader("📋 Historical Financial Data")

display_df = company_df[
    [
        "year",
        metric
    ]
].copy()

display_df.columns = [
    "Financial Year",
    metric.replace("_"," ").title()
]

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True,

    height=400

)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Trend Data",

    csv,

    f"{company}_trend.csv",

    "text/csv",

    use_container_width=True

)

# ==========================================================
# GROWTH ANALYSIS
# ==========================================================

st.write("")

st.subheader("📈 Growth Analysis")

growth_df = company_df.copy()

growth_df["YoY Growth (%)"] = (
    growth_df[metric]
    .pct_change()
    * 100
)

growth_df["Absolute Change"] = (
    growth_df[metric]
    .diff()
)

# CAGR

start_value = growth_df[metric].iloc[0]
end_value = growth_df[metric].iloc[-1]
years = len(growth_df) - 1

if start_value > 0 and years > 0:

    cagr = (
        ((end_value / start_value) ** (1 / years) - 1)
        * 100
    )

else:

    cagr = None

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Highest",
    f"{highest_value:.2f}"
)

c2.metric(
    "Lowest",
    f"{lowest_value:.2f}"
)

c3.metric(
    "Net Change",
    f"{end_value-start_value:.2f}"
)

c4.metric(
    "CAGR",
    "N/A" if cagr is None else f"{cagr:.2f}%"
)

# ==========================================================
# GROWTH TABLE
# ==========================================================

st.write("")

st.subheader("📋 Growth Table")

growth_display = growth_df[
    [
        "year",
        metric,
        "Absolute Change",
        "YoY Growth (%)"
    ]
].copy()

growth_display.columns = [
    "Financial Year",
    metric.replace("_"," ").title(),
    "Absolute Change",
    "YoY Growth (%)"
]

st.dataframe(
    growth_display,
    use_container_width=True,
    hide_index=True,
    height=400
)

# ==========================================================
# GROWTH CHARTS
# ==========================================================

left, right = st.columns(2)

with left:

    fig = px.bar(
        growth_df,
        x="year",
        y="YoY Growth (%)",
        color="YoY Growth (%)",
        text_auto=".2f",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        title="Year-over-Year Growth"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.line(
        growth_df,
        x="year",
        y="Absolute Change",
        markers=True,
        template="plotly_dark",
        title="Absolute Change"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================================
# DISTRIBUTION ANALYSIS
# ==========================================================

st.write("")

st.subheader("📊 Distribution Analysis")

left, right = st.columns(2)

with left:

    fig = px.box(
        company_df,
        y=metric,
        points="all",
        template="plotly_dark",
        title="Box Plot"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.violin(
        company_df,
        y=metric,
        box=True,
        points="all",
        template="plotly_dark",
        title="Violin Plot"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# HISTOGRAM & DENSITY
# ==========================================================

st.write("")

left, right = st.columns(2)

with left:

    fig = px.histogram(
        company_df,
        x=metric,
        nbins=min(15, len(company_df)),
        text_auto=True,
        template="plotly_dark",
        title="Histogram"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.scatter(
        company_df,
        x="year",
        y=metric,
        size=metric,
        color=metric,
        template="plotly_dark",
        title="Bubble Trend"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Financial Year",
        yaxis_title=metric.replace("_", " ").title()
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

st.write("")

st.subheader("📋 Descriptive Statistics")

stats_df = pd.DataFrame({

    "Statistic": [
        "Count",
        "Mean",
        "Median",
        "Minimum",
        "Maximum",
        "Standard Deviation",
        "Variance",
        "Range",
        "25th Percentile",
        "75th Percentile"
    ],

    "Value": [

        company_df[metric].count(),

        company_df[metric].mean(),

        company_df[metric].median(),

        company_df[metric].min(),

        company_df[metric].max(),

        company_df[metric].std(),

        company_df[metric].var(),

        company_df[metric].max() - company_df[metric].min(),

        company_df[metric].quantile(0.25),

        company_df[metric].quantile(0.75)

    ]

})

st.dataframe(
    stats_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

# ==========================================================
# CORRELATION (SINGLE COMPANY)
# ==========================================================

st.write("")

st.subheader("📈 Financial Metrics Correlation")

corr_columns = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "earnings_per_share",
    "book_value_per_share"
]

corr_columns = [
    c for c in corr_columns
    if c in company_df.columns
]

corr = company_df[corr_columns].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    aspect="auto",
    template="plotly_dark",
    title="Correlation Heatmap"
)

fig.update_layout(
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.write("")

st.subheader("🧠 Executive Insights")

latest_value = company_df[metric].iloc[-1]
first_value = company_df[metric].iloc[0]

absolute_change = latest_value - first_value

growth_pct = (
    (absolute_change / first_value) * 100
    if first_value != 0 else 0
)

best_year = company_df.loc[
    company_df[metric].idxmax(),
    "year"
]

worst_year = company_df.loc[
    company_df[metric].idxmin(),
    "year"
]

volatility = company_df[metric].std()

trend = "Improving 📈" if absolute_change > 0 else "Declining 📉"

if growth_pct >= 20:
    recommendation = "🟢 Strong Positive Trend"
elif growth_pct >= 5:
    recommendation = "🟡 Stable Performance"
elif growth_pct >= -5:
    recommendation = "🟠 Flat Performance"
else:
    recommendation = "🔴 Needs Attention"

left, right = st.columns(2)

with left:

    st.success(f"""
### 📈 Performance Summary

• Latest Value : **{latest_value:.2f}**

• First Value : **{first_value:.2f}**

• Net Change : **{absolute_change:.2f}**

• Overall Growth : **{growth_pct:.2f}%**
""")

    st.info(f"""
### 🏆 Best Performance

Year : **{best_year}**

Value : **{highest_value:.2f}**
""")

with right:

    st.warning(f"""
### 📉 Lowest Performance

Year : **{worst_year}**

Value : **{lowest_value:.2f}**
""")

    st.success(f"""
### 📊 Business Insight

Trend : **{trend}**

Volatility : **{volatility:.2f}**

Recommendation :

**{recommendation}**
""")

# ==========================================================
# FINANCIAL HEALTH DASHBOARD
# ==========================================================

st.write("")

st.subheader("📌 Financial Snapshot")

snapshot_cols = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "earnings_per_share",
    "book_value_per_share",
    "free_cash_flow_cr",
    "cash_from_operations_cr",
    "dividend_payout_ratio_pct"
]

snapshot_cols = [
    c for c in snapshot_cols
    if c in company_df.columns
]

snapshot = company_df.iloc[-1][snapshot_cols]

snapshot = snapshot.reset_index()

snapshot.columns = [
    "Metric",
    "Value"
]

fig = px.bar(
    snapshot,
    x="Value",
    y="Metric",
    orientation="h",
    color="Value",
    color_continuous_scale="Viridis",
    template="plotly_dark",
    title="Latest Financial Snapshot"
)

fig.update_layout(
    height=650,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# DOWNLOADS
# ==========================================================

st.write("")

col1, col2 = st.columns(2)

with col1:

    csv = company_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Full Dataset (CSV)",
        csv,
        f"{company}_financial_history.csv",
        "text/csv",
        use_container_width=True
    )

with col2:

    from io import BytesIO

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        company_df.to_excel(
            writer,
            index=False,
            sheet_name="Trend Analysis"
        )

    st.download_button(
        "⬇ Download Full Dataset (Excel)",
        excel_buffer.getvalue(),
        f"{company}_financial_history.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()

st.caption(
    "N100 Financial Intelligence Platform • Trend Analysis Dashboard • Version 2.0"
)