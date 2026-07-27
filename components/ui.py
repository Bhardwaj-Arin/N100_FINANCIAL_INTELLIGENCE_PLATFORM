# ================================
# STEP 1
# Create a new file:
#
# components/ui.py
#
# Paste EVERYTHING below into it.
# ================================

import streamlit as st


def load_css():

    st.markdown(
        """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{

background:#090D14;

}

/* Hide Streamlit Default */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* Remove top padding */

.block-container{

padding-top:1.5rem;
padding-left:2rem;
padding-right:2rem;
padding-bottom:2rem;

}

/* Hero */

.hero{

background:linear-gradient(135deg,#0F172A,#111827);

padding:35px;

border-radius:24px;

border:1px solid #1F2937;

margin-bottom:30px;

box-shadow:0 0 30px rgba(37,99,235,.15);

}

.hero-title{

font-size:58px;

font-weight:800;

color:white;

margin-bottom:5px;

}

.hero-title span{

color:#3B82F6;

}

.hero-sub{

font-size:24px;

color:#CBD5E1;

margin-bottom:15px;

}

.hero-tag{

font-size:19px;

color:#94A3B8;

}

/* Metric Card */

.metric-card{

background:linear-gradient(135deg,#1D4ED8,#2563EB);

padding:25px;

border-radius:22px;

text-align:center;

transition:0.3s;

box-shadow:0 10px 30px rgba(37,99,235,.25);

}

.metric-card:hover{

transform:translateY(-6px);

box-shadow:0 18px 45px rgba(37,99,235,.40);

}

.metric-number{

font-size:42px;

font-weight:800;

color:white;

}

.metric-label{

font-size:18px;

color:#E5E7EB;

margin-top:8px;

}

/* Section */

.section{

font-size:38px;

font-weight:800;

color:white;

margin-top:45px;

margin-bottom:25px;

}

.section span{

color:#3B82F6;

}

/* Glass Card */

.glass{

background:#111827;

border:1px solid #23314F;

border-radius:22px;

padding:28px;

transition:.3s;

height:100%;

}

.glass:hover{

transform:translateY(-6px);

border:1px solid #3B82F6;

box-shadow:0 0 30px rgba(59,130,246,.18);

}

/* Feature */

.feature-title{

font-size:30px;

font-weight:700;

color:white;

margin-bottom:12px;

}

.feature-text{

font-size:18px;

color:#CBD5E1;

margin-bottom:18px;

}

.feature-list{

font-size:17px;

line-height:2.0;

color:white;

}

/* Info Card */

.info{

background:#10243D;

padding:25px;

border-radius:20px;

border:1px solid #234C84;

height:100%;

}

/* Footer */

.footer{

margin-top:60px;

padding:25px;

text-align:center;

color:#94A3B8;

font-size:15px;

}

/* Divider */

hr{

border:0;

height:1px;

background:#1E293B;

margin-top:35px;

margin-bottom:35px;

}

</style>

""",
        unsafe_allow_html=True,
    )


def hero():

    st.markdown(
        """
<div class="hero">

<div class="hero-title">

📊 Financial Intelligence <span>Platform</span>

</div>

<div class="hero-sub">

Intelligent Financial Analytics for Indian Listed Companies

</div>

<div class="hero-tag">

📊 Analyze &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
👥 Compare &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
🔍 Discover &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
🏆 Rank

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def metric_card(title, value):

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-number">

{value}

</div>

<div class="metric-label">

{title}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def section(icon, title):

    st.markdown(
        f"""
<div class="section">

{icon}
<span>{title}</span>

</div>
""",
        unsafe_allow_html=True,
    )


def feature_card(icon, title, desc, items):

    bullets = ""

    for item in items:

        bullets += f"<li>{item}</li>"

    st.markdown(
        f"""
<div class="glass">

<div class="feature-title">

{icon} {title}

</div>

<div class="feature-text">

{desc}

</div>

<ul class="feature-list">

{bullets}

</ul>

</div>
""",
        unsafe_allow_html=True,
    )


def info_card(title, body):

    st.markdown(
        f"""
<div class="info">

<h2 style="color:#60A5FA;">{title}</h2>

{body}

</div>
""",
        unsafe_allow_html=True,
    )


def footer():

    st.markdown(
        """
<div class="footer">

<hr>

Financial Intelligence Platform

<br><br>

Built using ❤️ Python • Pandas • Plotly • Streamlit

</div>
""",
        unsafe_allow_html=True,
    )