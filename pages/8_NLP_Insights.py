import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from collections import Counter
import re

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NLP Insights",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/processed/master_features.csv"
    )

df = load_data()

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

DESCRIPTION_COL = "about_company"

KEEP_COLUMNS = [

    "company_name",
    "company_logo",
    "broad_sector",
    DESCRIPTION_COL

]

df = df[KEEP_COLUMNS].drop_duplicates()

df = df.dropna(
    subset=[DESCRIPTION_COL]
)

df = df[
    df[DESCRIPTION_COL].str.strip() != ""
]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🧠 NLP Insights")

st.write(
    "Business language intelligence, keyword extraction and strategic communication analysis."
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("NLP Filters")

company = st.sidebar.selectbox(

    "Company",

    sorted(df["company_name"].unique())

)

max_words = st.sidebar.slider(

    "Maximum Keywords",

    10,

    100,

    40

)

minimum_frequency = st.sidebar.slider(

    "Minimum Frequency",

    1,

    5,

    1

)

chart_type = st.sidebar.radio(

    "Visualization",

    [

        "Word Cloud",
        "Bar Chart",
        "Bubble Chart"

    ]

)

search_keyword = st.sidebar.text_input(

    "Keyword Search"

)

# ==========================================================
# COMPANY DATA
# ==========================================================

company_df = df[
    df["company_name"] == company
]

description = company_df.iloc[0][DESCRIPTION_COL]

sector = company_df.iloc[0]["broad_sector"]

# ==========================================================
# COMPANY INFORMATION
# ==========================================================

st.subheader(company)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Sector",
        sector
    )

with col2:

    st.metric(
        "Description Length",
        f"{len(description):,} Characters"
    )

# ==========================================================
# BUSINESS STOPWORDS
# ==========================================================

BUSINESS_STOPWORDS = {

"the","and","for","are","with","that","this","from",
"into","its","their","our","your","his","her","was",
"were","has","have","had","been","being","will","shall",
"would","could","should","can","may","might","about",
"after","before","during","through","within","across",
"over","under","than","then","also","very","much",
"company","companies","business","corporation","corp",
"inc","limited","ltd","group","holding","holdings",
"private","public","india","indian","global","world",
"international","one","two","three","first","second",
"using","used","use","provides","provide","providing",
"services","service","products","product","solution",
"solutions","customer","customers","clients","client",
"market","markets","industry","industries","sector",
"operations","operates","operating","manufactures",
"manufacturing","leading","largest","major","primarily",
"across","among","including","include","includes",
"through","via","such","well","known","based","headquartered",
"approximately","nearly","almost","over","more","less",
"into","under","each","every","various","different",
"related","support","supports","develop","develops",
"development","years","year"

}

# ==========================================================
# TEXT CLEANING
# ==========================================================

clean_text = re.sub(

    r"[^a-zA-Z ]",

    " ",

    description.lower()

)

words = [

    word

    for word in clean_text.split()

    if len(word) > 2
    and word not in BUSINESS_STOPWORDS

]

word_counts = Counter(words)

freq_df = pd.DataFrame(

    word_counts.items(),

    columns=[

        "Keyword",
        "Frequency"

    ]

)

freq_df = freq_df[

    freq_df["Frequency"] >= minimum_frequency

]

freq_df = freq_df.sort_values(

    "Frequency",

    ascending=False

).head(max_words)

freq_df["Percentage"] = (

    freq_df["Frequency"]

    / freq_df["Frequency"].sum()

    * 100

).round(2)

freq_df["Rank"] = range(

    1,

    len(freq_df)+1

)

# ==========================================================
# ADVANCED KPIs
# ==========================================================

total_words = len(words)

unique_words = len(set(words))

reading_time = max(

    1,

    round(total_words / 200)

)

lexical_diversity = round(

    (unique_words / total_words) * 100,

    1

) if total_words else 0

avg_word_length = round(

    sum(len(i) for i in words) / total_words,

    2

) if total_words else 0

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(

    "Keywords",

    total_words

)

k2.metric(

    "Unique",

    unique_words

)

k3.metric(

    "Vocabulary",

    f"{lexical_diversity}%"

)

k4.metric(

    "Reading Time",

    f"{reading_time} min"

)

k5.metric(

    "Avg Word Length",

    avg_word_length
)

# ==========================================================
# PROFESSIONAL WORD CLOUD
# ==========================================================

st.write("")

st.subheader("☁️ Business Keyword Cloud")

if chart_type == "Word Cloud":

    wordcloud = WordCloud(

        width=1800,
        height=800,
        background_color="white",
        max_words=max_words,
        collocations=False,
        prefer_horizontal=0.9

    ).generate_from_frequencies(word_counts)

    fig, ax = plt.subplots(figsize=(18,8))

    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    st.pyplot(fig)

# ==========================================================
# TOP KEYWORDS
# ==========================================================

st.write("")

st.subheader("🏆 Top Business Keywords")

left, right = st.columns([1.2,1])

with left:

    st.dataframe(

        freq_df,

        use_container_width=True,

        hide_index=True,

        height=500

    )

with right:

    top10 = freq_df.head(10)

    fig = px.bar(

        top10,

        x="Frequency",

        y="Keyword",

        orientation="h",

        text="Frequency",

        color="Frequency",

        color_continuous_scale="Viridis",

        template="plotly_dark",

        title="Top 10 Keywords"

    )

    fig.update_layout(

        height=500,

        coloraxis_showscale=False,

        yaxis=dict(categoryorder="total ascending")

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# INTERACTIVE VISUALIZATION
# ==========================================================

st.write("")

st.subheader("📊 Keyword Visualization")

if chart_type == "Bar Chart":

    fig = px.bar(

        freq_df,

        x="Keyword",

        y="Frequency",

        color="Frequency",

        text="Frequency",

        template="plotly_dark",

        color_continuous_scale="Turbo",

        title="Keyword Frequency Distribution"

    )

    fig.update_layout(

        height=600,

        coloraxis_showscale=False,

        xaxis_tickangle=-45

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

elif chart_type == "Bubble Chart":

    fig = px.scatter(

        freq_df,

        x="Rank",

        y="Frequency",

        size="Frequency",

        color="Frequency",

        hover_name="Keyword",

        text="Keyword",

        size_max=70,

        color_continuous_scale="Turbo",

        template="plotly_dark",

        title="Business Keyword Bubble Chart"

    )

    fig.update_traces(

        textposition="top center"

    )

    fig.update_layout(

        height=650,

        coloraxis_showscale=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# KEYWORD SHARE
# ==========================================================

st.write("")

st.subheader("🥧 Keyword Share")

pie_df = freq_df.head(10)

fig = px.pie(

    pie_df,

    names="Keyword",

    values="Frequency",

    hole=0.45,

    template="plotly_dark"

)

fig.update_traces(

    textposition="inside",

    textinfo="percent+label"

)

fig.update_layout(

    height=600

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# KEYWORD SEARCH
# ==========================================================

st.write("")

st.subheader("🔍 Keyword Explorer")

if search_keyword:

    keyword = search_keyword.lower().strip()

    sentences = re.split(

        r'(?<=[.!?])\s+',

        description

    )

    matched = [

        s

        for s in sentences

        if keyword in s.lower()

    ]

    if matched:

        st.success(

            f'Keyword "{keyword}" found in {len(matched)} sentence(s).'

        )

        for i, sentence in enumerate(matched,1):

            highlighted = re.sub(

                keyword,

                f"**{keyword.upper()}**",

                sentence,

                flags=re.IGNORECASE

            )

            st.markdown(

                f"**Match {i}:** {highlighted}"

            )

    else:

        st.error(

            "Keyword not found."

        )

# ==========================================================
# BUSINESS INTELLIGENCE
# ==========================================================

st.write("")

st.subheader("🏢 Business Intelligence")

business_categories = {

    "Healthcare":[
        "pharma","pharmaceutical","medicine","medical",
        "health","hospital","diagnostic","nutrition",
        "drug","therapy","vaccine"
    ],

    "Technology":[
        "software","technology","digital","cloud",
        "ai","automation","analytics","platform",
        "cyber","data"
    ],

    "Finance":[
        "bank","finance","financial","insurance",
        "credit","loan","capital","asset","wealth"
    ],

    "Manufacturing":[
        "factory","plant","manufacture","production",
        "equipment","industrial","engineering",
        "machinery"
    ],

    "Energy":[
        "power","oil","gas","renewable","solar",
        "electric","energy"
    ],

    "Retail":[
        "consumer","retail","store","shopping",
        "brand","distribution","dealer"
    ]

}

category_scores = {}

for category, keywords in business_categories.items():

    score = sum(

        clean_text.count(word)

        for word in keywords

    )

    category_scores[category] = score

category_df = pd.DataFrame({

    "Business Area": category_scores.keys(),

    "Score": category_scores.values()

}).sort_values(

    "Score",

    ascending=False

)

left, right = st.columns([1.1,1])

with left:

    fig = px.bar(

        category_df,

        x="Business Area",

        y="Score",

        color="Score",

        text="Score",

        color_continuous_scale="Turbo",

        template="plotly_dark",

        title="Business Theme Detection"

    )

    fig.update_layout(

        height=500,

        coloraxis_showscale=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    st.dataframe(

        category_df,

        use_container_width=True,

        hide_index=True,

        height=500

    )

# ==========================================================
# VOCABULARY QUALITY
# ==========================================================

st.write("")

st.subheader("📚 Communication Quality")

technical_words = {

    "analytics","automation","cloud","research",
    "innovation","technology","engineering",
    "manufacturing","diagnostic","digital",
    "capital","financial","software","hardware",
    "pharmaceutical","healthcare","infrastructure",
    "renewable","logistics","telecom"

}

technical_count = len(

    [

        w

        for w in words

        if w in technical_words

    ]

)

technical_score = round(

    technical_count / total_words * 100,

    1

) if total_words else 0

long_words = len(

    [

        w

        for w in words

        if len(w) >= 8

    ]

)

long_word_score = round(

    long_words / total_words * 100,

    1

) if total_words else 0

communication_df = pd.DataFrame({

    "Metric":[

        "Vocabulary Richness",
        "Technical Language",
        "Long Words",
        "Unique Vocabulary"

    ],

    "Score":[

        lexical_diversity,
        technical_score,
        long_word_score,
        lexical_diversity

    ]

})

fig = go.Figure()

for _, row in communication_df.iterrows():

    fig.add_trace(

        go.Bar(

            x=[row["Metric"]],

            y=[row["Score"]],

            text=f'{row["Score"]}%',

            textposition="outside",

            name=row["Metric"]

        )

    )

fig.update_layout(

    template="plotly_dark",

    height=500,

    showlegend=False,

    yaxis_title="Score (%)",

    title="Communication Quality Score"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# LANGUAGE METRICS
# ==========================================================

st.write("")

st.subheader("📈 NLP Quality Metrics")

complexity = min(

    100,

    round(avg_word_length * 12,1)

)

content_density = min(

    100,

    round(long_word_score * 1.6,1)

)

professionalism = round(

    (technical_score + lexical_diversity) / 2,

    1

)

metrics_df = pd.DataFrame({

    "Metric":[

        "Vocabulary Richness",
        "Technical Language",
        "Communication Complexity",
        "Content Density",
        "Professionalism"

    ],

    "Score":[

        lexical_diversity,
        technical_score,
        complexity,
        content_density,
        professionalism

    ]

})

fig = px.bar(

    metrics_df,

    x="Metric",

    y="Score",

    color="Score",

    text="Score",

    template="plotly_dark",

    color_continuous_scale="Viridis",

    title="Overall NLP Quality Assessment"

)

fig.update_layout(

    height=600,

    coloraxis_showscale=False,

    xaxis_tickangle=-20

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# EXECUTIVE INTELLIGENCE
# ==========================================================

st.write("")

st.subheader("🧠 Executive Intelligence")

primary_theme = category_df.iloc[0]["Business Area"]
theme_score = category_df.iloc[0]["Score"]

top_keyword = freq_df.iloc[0]["Keyword"]
top_frequency = int(freq_df.iloc[0]["Frequency"])

innovation_words = {
    "innovation","research","technology","digital",
    "automation","ai","analytics","development",
    "engineering","advanced"
}

risk_words = {
    "risk","debt","loss","competition",
    "uncertain","volatile","litigation",
    "challenge","decline","crisis"
}

innovation_score = sum(

    clean_text.count(word)

    for word in innovation_words

)

risk_score = sum(

    clean_text.count(word)

    for word in risk_words

)

if professionalism >= 70:

    communication_grade = "Excellent"

elif professionalism >= 50:

    communication_grade = "Good"

elif professionalism >= 30:

    communication_grade = "Average"

else:

    communication_grade = "Basic"

business_focus = {

    "Healthcare":"Healthcare & Pharmaceuticals",

    "Technology":"Technology & Digital",

    "Finance":"Financial Services",

    "Manufacturing":"Manufacturing & Industrial",

    "Energy":"Energy & Utilities",

    "Retail":"Retail & Consumer"

}

focus = business_focus.get(

    primary_theme,

    "Diversified Business"

)

left, right = st.columns(2)

with left:

    st.success(f"""
### 🏢 Business Summary

**Primary Business**

{focus}

**Sector**

{sector}

**Top Keyword**

{top_keyword}

**Theme Score**

{theme_score}
""")

    st.info(f"""
### 📚 Communication Assessment

Vocabulary Richness

**{lexical_diversity}%**

Professionalism

**{professionalism}%**

Communication Grade

**{communication_grade}**
""")

with right:

    st.warning(f"""
### 🚀 Strategic Indicators

Innovation Score

**{innovation_score}**

Risk Language

**{risk_score}**

Reading Time

**{reading_time} minute(s)**
""")

    st.success(f"""
### 💡 Executive Observation

The company description mainly focuses on **{focus}** with emphasis on **{top_keyword}**.

The communication style is **{communication_grade.lower()}**, indicating a vocabulary richness of **{lexical_diversity}%** and technical language usage of **{technical_score}%**.
""")

# ==========================================================
# DESCRIPTION CARD
# ==========================================================

st.write("")

st.subheader("📄 Company Description")

with st.container(border=True):

    st.markdown(description)

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Word Count",
        total_words
    )

    c2.metric(
        "Reading Time",
        f"{reading_time} min"
    )

    c3.metric(
        "Top Keyword",
        top_keyword
    )

# ==========================================================
# FINAL NLP REPORT
# ==========================================================

st.write("")

st.subheader("📋 NLP Summary Report")

report = pd.DataFrame({

    "Metric":[

        "Company",
        "Sector",
        "Business Focus",
        "Primary Theme",
        "Top Keyword",
        "Keyword Frequency",
        "Vocabulary Richness (%)",
        "Technical Language (%)",
        "Professionalism (%)",
        "Reading Time (Minutes)",
        "Innovation Score",
        "Risk Score"

    ],

    "Value":[

        company,
        sector,
        focus,
        primary_theme,
        top_keyword,
        top_frequency,
        lexical_diversity,
        technical_score,
        professionalism,
        reading_time,
        innovation_score,
        risk_score

    ]

})

st.dataframe(

    report,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

csv = report.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇️ Download NLP Intelligence Report",

    csv,

    f"{company}_nlp_intelligence_report.csv",

    "text/csv",

    use_container_width=True

)

st.divider()

st.caption(
    "N100 Financial Intelligence Platform • NLP Intelligence Dashboard • Version 3.0"
)