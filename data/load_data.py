import pandas as pd
import streamlit as st

@st.cache_data
def load_monthly_sums():
    return pd.read_csv("data/processed/monthly_sums.csv")

@st.cache_data
def load_geo_data():
    return pd.read_csv("data/processed/cantons.csv")

@st.cache_data
def load_cleaned_dataset() -> pd.DataFrame:
    return pd.read_csv("data/processed/cleaned_dataset.csv")
