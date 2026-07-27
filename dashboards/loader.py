from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "master_features.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)